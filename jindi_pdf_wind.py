# coding = utf-8
from elasticsearch import Elasticsearch

# 首先尝试实现对2017金地年报数据的获取
# 存储的目标index:jindi_wss_index

# 首先获取pdf_id，从其他模块获得，此处为了方便，进行自定义
# 此pdf_id为金地集团年报的pdf,其中有很多页，包含我们需要的三大报表
host = '192.168.31.99:9200'
es = Elasticsearch(hosts=host)

# 内容读取的index和内容写入的index
from_index = 'jindi_test_table'
to_index = 'jindi_wss_index'

# 金地2017年报的pdf_id
pdf_id = "1010120180418876561"

# 确定查询条件
query_list = ['*资产负债表', '*利润表', '*现金流量表']

# 每一项存储一个字典，{pdf_id,query_list_item} 用于指出是哪个pdf_id的哪类表出现了问题
abnormal_record = []

# to_index里面每个document的id构成条件
'''"sheet_type": "母公司报表","table_type": "资产负债表",     pdf-id_sheet-type_table-type_(未调整，调整)    '''
sheet_type_dict = {'母公司报表': '0', '合并报表': '1'}
table_type_dict = {'资产负债表': '0', '利润表': '1', '现金流量表': '2'}
adjust_type_dict = {'未调整': '0', '调整': '1'}

"""
{
"_index": "wind_wss_index",
"_type": "d_type",
"_id": "6011072017033121",
"_version": 1,
"_score": 1,
"_source": {
    "end_date": "20170331",
    "sheet_type": "母公司报表",
    "report_season": "一季报",
    "table_type": "资产负债表",
    "trade_code": "601107",
    '...':'.......' }
}
"""


# 定义一个函数，传入report_name,新建两条document（未调整，调整）
def create_index_by_name(report_name, to_index, pdf_id):
    """
    传入的值有多种，示例如下：
        已经完成对 1010120180418876561 资产负债表的读取:   3
        母公司资产负债表
        合并资产负债表
        合并资产负债表
        已经完成对 1010120180418876561 利润表的读取:   2
        母公司利润表
        合并利润表
        已经完成对 1010120180418876561 现金流量表的读取:   2
        合并现金流量表
        母公司现金流量表
    """
    # 在这边有一个问题，是不是金地集团所有的报表的report_name都是这样的，若不是，则会出现问题，
    if report_name == '母公司资产负债表':
        '''建立两条document：（未调整0，调整1）,并插入基本的数据'''

        id0 = pdf_id + '_' + sheet_type_dict['母公司报表'] + '_' + table_type_dict['资产负债表'] + '_' + adjust_type_dict['未调整']
        id1 = pdf_id + '_' + sheet_type_dict['母公司报表'] + '_' + table_type_dict['资产负债表'] + '_' + adjust_type_dict['调整']

        data = {'end_date': '20171231', 'sheet_type': '母公司报表', 'report_season': '年报', 'table_type': '资产负债表'}
        try:
            es.create(index=to_index, doc_type='d_type', id=id0, body=data)
            # 如果可以顺利执行，说明暂时没有断表问题，或暂时还没有遇到，可以直接向下执行即可
        except Exception as e:
            # 说明有断表问题,已经建立过
            print(e)
            return (id0, id1)

        data['sheet_type'] = '母公司报表(调整)'  # 关于数据库里面的括号是中文括号还是应为括号先留待后面验证解决
        es.create(index=to_index, doc_type='d_type', id=id1, body=data)
        return (id0, id1)

    elif report_name == '合并资产负债表':
        id0 = pdf_id + '_' + sheet_type_dict['合并报表'] + '_' + table_type_dict['资产负债表'] + '_' + adjust_type_dict['未调整']
        id1 = pdf_id + '_' + sheet_type_dict['合并报表'] + '_' + table_type_dict['资产负债表'] + '_' + adjust_type_dict['调整']
        data = {'end_date': '20171231', 'sheet_type': '合并报表', 'report_season': '年报', 'table_type': '资产负债表'}
        try:
            es.create(index=to_index, doc_type='d_type', id=id0, body=data)
        except Exception as e:
            print(e)
            return (id0, id1)

        data['sheet_type'] = '合并报表(调整)'  # 关于数据库里面的括号是中文括号还是应为括号先留待后面验证解决
        es.create(index=to_index, doc_type='d_type', id=id1, body=data)
        return (id0, id1)
    elif report_name == '母公司利润表':
        id0 = pdf_id + '_' + sheet_type_dict['母公司报表'] + '_' + table_type_dict['利润表'] + '_' + adjust_type_dict['未调整']
        id1 = pdf_id + '_' + sheet_type_dict['母公司报表'] + '_' + table_type_dict['利润表'] + '_' + adjust_type_dict['调整']
        pass
    elif report_name == '合并利润表':
        id0 = pdf_id + '_' + sheet_type_dict['合并报表'] + '_' + table_type_dict['利润表'] + '_' + adjust_type_dict['未调整']
        id1 = pdf_id + '_' + sheet_type_dict['合并报表'] + '_' + table_type_dict['利润表'] + '_' + adjust_type_dict['调整']
        pass
    elif report_name == '合并现金流量表':
        id0 = pdf_id + '_' + sheet_type_dict['合并报表'] + '_' + table_type_dict['现金流量表'] + '_' + adjust_type_dict['未调整']
        id1 = pdf_id + '_' + sheet_type_dict['合并报表'] + '_' + table_type_dict['现金流量表'] + '_' + adjust_type_dict['调整']
        pass
    elif report_name == '母公司现金流量表':
        id0 = pdf_id + '_' + sheet_type_dict['母公司报表'] + '_' + table_type_dict['现金流量表'] + '_' + adjust_type_dict['未调整']
        id1 = pdf_id + '_' + sheet_type_dict['母公司报表'] + '_' + table_type_dict['现金流量表'] + '_' + adjust_type_dict['调整']
        pass
    else:
        print('------未匹配到符合条件，无法创建document,请检查------')


def read_from_index(items):
    data0 = {}
    data1 = {}
    # 我需要遍历的是segment部分,首先我需要取到segment部分
    results = items['_source']['segments']
    # 得到的results是一个列表，里面存放着的每一个元素为字典，
    for result in results:
        row_list = result['rows']
        for line in row_list:
            # 此时的line是一个字典
            if line['tds'][0]['value'] == '项目' or line['tds'][0]['value'] == '':
                # 判断出表格中的这一行是第一行或者空行
                continue
            else:
                '''每一行都包含未调整，调整的值'''
                key = line['tds'][0]['value']
                value0 = line['tds'][2]['value']
                value1 = line['tds'][3]['value']
                if value0 == '-':
                    value0 = 'None'
                if value1 == '-':
                    value1 = 'None'
                data0.update({key: value0})
                data1.update({key: value1})

    return data0, data1


def main():
    # 为了便于测试：先删除该index,再建立该index,若成功删除,则{'acknowledged': True}，
    # 若index原本就不存在，则response_result['status'] = 404
    es.indices.delete(index=to_index, ignore=[400, 404])

    # 创建一个空白的index
    es.indices.create(index=to_index, ignore=400)

    for i in query_list:
        # result包含中资产负债表的全部内容，
        result = es.search(from_index,
                           doc_type="d_type",
                           body={"query": {"bool": {"must": [{"term": {"pdf_id.keyword": pdf_id}},
                                                             {"wildcard": {"table_info.text_list.keyword": i}}],
                                                    "must_not": [], "should": []}}, "from": 0, "size": 10, "sort": [],
                                 "aggs": {}})['hits']['hits']
        # 一般值都是2，当出现>2的时候，就是表被分割了，不可能小于2的，若出现小于2的，则需要记录下来
        print('已经完成对 {0} {1}的读取:   '.format(pdf_id, i[1:]), end='')
        print(len(result))
        if len(result) < 2:
            print('对 {0} {1} 的读取出现异常，记录完毕'.format(pdf_id, i[1:]))
            abnormal_record.append({pdf_id: i})

        # 我已经读取到了该pdf_id的资产负债表，下面进行读写
        # 首先需要明确要存储的格式需要哪些数据
        """
        {
            "_index": "wind_wss_index",
            "_type": "d_type",
            "_id": "6011072017033121",
            "_version": 1,
            "_score": 1,
            "_source": { 
                "end_date": "20170331",
                "sheet_type": "母公司报表",
                "report_season": "一季报",
                "table_type": "资产负债表",
                "trade_code": "601107",

                # 下面的所有属性都可以从from_index里面读取，上面的这几行属性都需要自己去确定

                "所有者权益": "None",
                "补充资料": "None",
                "oth_rcv_tot": "1537278495.51",
                '...':'.......' }
        }
        """

        # 下面需要对result进行遍历，每对result中的一项进行遍历，都是同时在读取两张表的内容（合并资产负债表，合并资产负债表调整）
        # 解决一个潜在的bug：针对有断表问题而没有id0,id1的返回值，但是却需要利用id0,id1来更新数据库，此时会有错误,在功能函数处修改
        for items in result:
            # 每一项items就是之前看的a[0],a[1],a[2]的数据存储格式
            # 先对items读取到 items['_source']['table_info'][0]['text_list'][0]--> '合并资产负债表',来判断这是哪个表
            report_name = items['_source']['table_info'][0]['text_list'][0]
            print('-------------------------------')
            print(report_name)
            print('开始执行对 {} 的读写'.format(report_name))

            # 每个document的id是该文档的唯一标识，所以，当我需要插入数据时，可以利用id这个唯一标识来插入数据
            # 所以我需要确定构成每个id的标准是什么： pdf-id_sheet-type_table-type_(未调整，调整)
            id0, id1 = create_index_by_name(report_name, to_index, pdf_id)
            # 其中id0为：未调整表的记录id,其中id1为：调整表的记录id

            # 其中data0为未调整表的数据，data1为调整表的记录
            data0, data1 = read_from_index(items)

            # 下面需要对data0，data1进行追加写入到对应的id的记录中
            # 此更新是增量更新，而不是覆盖更新
            es.update(index=to_index, doc_type='d_type', body={'doc': data0}, id=id0, ignore=400)
            es.update(index=to_index, doc_type='d_type', body={'doc': data1}, id=id1, ignore=400)

        break  # 暂时只测试资产负债表的数据


if __name__ == '__main__':
    main()

































