
class FixRowJindi:
    def __init__(self):
        self.fix_dict_yuyi = {}

    # 需要获取的值有：需要修补的数据(字典),修补的依据字典({'jindi_value':'yuyi_value'})
    # 需要注意的问题是：有的jindi_value对应的yuyi_value数据不在，需要对不在的数据进行判断，
    # 并进行动态补充yuyi数据.

    def fix_finance_col_value(self, table_name, jindi_data):

        data0, data1 = self.change_to_dict(jindi_data)
        data0, data1 = self.fixed_dict(data0, data1)
        data0, data1 = self.fix_key_by_yuyi(data0, data1)
        self.update_yuyi_index(table_name)
        return data0, data1

    def change_to_dict(self, jindi_data):
        # 将数据读取到字典中，并作初步的fix:
        # 不读取空行
        data0 = {}
        data1 = {}
        results = jindi_data['segments']
        # 得到的results是一个列表，里面存放着的每一个元素为字典，
        for result in results:
            try:
                info = result['inforow']
            except Exception as e:
                print('------->出现缺少inforow的情况<--------')
                print('该字典无 inforow ')
                info = '备注'
            row_list = result['rows']
            for line in row_list:
                # 此时的line是一个字典
                if line['tds'][0]['value'] == '项目' or line['tds'][0]['value'] == '':
                    # 判断出表格中的这一行是第一行或者空行
                    continue

                else:
                    '''每一行都包含未调整，调整的值'''
                    if line['tds'][0]['value'] == '其中：优先股':
                        key = info + '-' + line['tds'][2]['value'][3:]
                    if line['tds'][0]['value'] == '永续债':
                        key = info + '-' + line['tds'][2]['value']
                    else:
                        key = line['tds'][0]['value']

                    value0 = line['tds'][2]['value']
                    value1 = line['tds'][3]['value']
                    data0.update({key: value0})
                    data1.update({key: value1})

        return data0, data1

    def fixed_dict(self, data0, data1):
        # 很显然这两个字典的键是一样的
        for keys in data0:
            if data0[keys] == '-':
                data0[keys] = 'None'
            else:
                data0[keys] = data0[keys].replace(',', '')

            if data1[keys] == '-':
                data1[keys] = 'None'
            else:
                data1[keys] = data1[keys].replace(',', '')
        return data0, data1

    def fix_key_by_yuyi(self, data0, data1):

        # 有的是列表形式，检测以下查询结果为：是否可以正确反馈
        # 当为列表时，也是可以正确查找的
        for old_key in data0:
            results = es.search(FINANCE_MATCH_INDEX,
                    doc_type='d_type',
                    body={"query": {"bool": {"must": [{"term": {"alias.name.keyword": old_key}}], "must_not": [], "should": []}},
                                                "from": 0, "size": 10, "sort": [], "aggs": {}})['hits']['hits']

            if results:
                # 存在我们检索到的值
                new_key = results[0]['_source']['alias'][1]['name'][0]

            else:
                print('{} 在yuyi数据库中不存在'.format(old_key))
                new_key = input('请手动输入对应的yuyi数据:')
                self.fix_dict_yuyi.update({new_key, old_key})

            data0[new_key], data1[new_key] = data0.pop(old_key), data1.pop(old_key)

        return data0, data1

    def update_yuyi_index(self, table_name):
        for yuyi_name in self.fix_dict_yuyi:
            # 构造出带插入的字典
            # 插入一条document,id自定
            # 由于现在elasticsearch连接不上，错误在网上也没查到，只好暂定
            # 2019/05/29 21:59:43 [W] [visitor.go:139] [secret_es_visitor106] start new visitor connection error: custom listener for [secret_es] doesn't exist
            pass



a_str = '（12,42,34.34）'
print(a_str.replace(',','').replace('（','').replace('）',''))






























