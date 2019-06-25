
from elasticsearch import Elasticsearch
from esfrm.es_class import HjEsIO
import itertools
import pysnooper

wind_index = 'wind_wss_index'
pdf_jindi_index = 'jindi_wss_index'
ignore_list = ['trade_code', 'announce_date', 'final_announce_date', 'end_date', 'sheet_type', 'company_type', 'table_type', 'file_id', 'short_company_name', 'report_season']
msg_1 = "键在jindi,wind里面所对应的值不一样。"
msg_2 = "键在wind中而不在jindi中"
msg_3 = '键在jindi中而不在wind中'
error_pdf_index = 'error_compare_result_2'


class TableCompare:
    """数据对比"""
    def __init__(self, es_bhv):
        self.es_bhv = es_bhv
        self.trade_code = None
        self.sheet_type = None
        self.table_type = None
        self.end_date = None
        pass

    def get_dict(self, index_name, trade_code, end_date, sheet_type, table_type):
        """
        根据不同index_name获取不同的dict数据
        :param index_name: 数据所在的index
        :param trade_code: 交易代码，如600548
        :param end_date: 报告期末，20171231
        :param sheet_type: 报告类型，合并报表
        :param table_type: 表格类型，资产负债表
        :return:
        """
        res_list = self.es_bhv.es.search(index=index_name, doc_type='d_type',
                                         body={'query': {'bool': {'must': [{'term': {'trade_code.keyword':trade_code}},
                                                                           {'term': {'end_date.keyword': end_date}},
                                                                           {'term': {'sheet_type.keyword':sheet_type}},
                                                                           {'term': {'table_type.keyword': table_type}}]}}},
                                         size=10)['hits']['hits']
        if res_list:
            tushare_dict = res_list[0]['_source']
            return tushare_dict
        else:
            return {}
        pass

    # @pysnooper.snoop()
    def dict_compare(self, target_dict, pdf_dict, source):
        """
        将两个dict进行对比
        :param target_dict: wind数据
        :param pdf_dict: 鱼意自己的pdf数据
        :return:
        """
        if not pdf_dict:
            print('msg', "pdf_dict不存在。")
            print('--------------------------')
            return
        self.trade_code = pdf_dict['trade_code']
        self.table_type = pdf_dict['table_type']
        self.sheet_type = pdf_dict['sheet_type']
        self.end_date = pdf_dict['end_date']

        for i in ignore_list:
            if i in target_dict:
                target_dict.pop(i)
            if i in pdf_dict:
                pdf_dict.pop(i)

        for i in target_dict:
            content = self.compare_value(i, target_dict, pdf_dict, source)
            if content:
                print(content)
                self.es_bhv.update_row(error_pdf_index, content)
                self.es_bhv.es.indices.refresh(error_pdf_index)
                # return content
        for i in pdf_dict:
            content = self.compare_value_2(i, target_dict, pdf_dict, source)
            if content:
                self.es_bhv.update_row(error_pdf_index,content)
                self.es_bhv.es.indices.refresh(error_pdf_index)
                # print(content)
        return '------对比结束------'

    def compare_value(self, i, target_dict, pdf_dict, source):
        """
        比对单个值
        :param i: target_dict的某个键
        :param target_dict:wind或者tushare数据
        :param pdf_dict: 鱼意自己的pdf数据
        :return:
        """
        target_value = target_dict[i]
        if target_value != 'None':
            return self.compare_value_by_wind_not_none(i, target_value, pdf_dict, source)

        else:
            return self.compare_value_by_wind_none(i, target_value, pdf_dict, source)

    def compare_value_by_wind_not_none(self, i, target_value, pdf_dict, source):
        """此种情况代表wind数据值不为None"""
        exist, flag_none, pdf_value = self.achieve_value(i, pdf_dict)
        if exist == 0:  # 说明在pdf_dict里面不存在该键
            return self.compare_result('two', source, i, pdf_dict, target_value, pdf_value)
            
        elif exist == 1 and flag_none == 1:  # 说明在pdf_dict里面存在该键，但value为None
            return self.compare_result('one', source, i, pdf_dict, target_value, pdf_value)
            
        elif exist == 1 and flag_none == 0:  # 说明pdf_dict里面存在该键，且value不为None
            if abs(float(target_value) - float(pdf_value)) > 0.01:
                # 说明键都有(且都不为None)，但值出现误差
                return self.compare_result('one', source, i, pdf_dict, target_value, pdf_value)
                
    def compare_value_by_wind_none(self, i, target_value, pdf_dict, source):
        """此种情况代表wind数据值为None"""
        exist, flag_none, pdf_value = self.achieve_value(i, pdf_dict)
        if exist == 0:  # 说明在pdf_dict里面不存在该键
            return self.compare_result('two', source, i, pdf_dict, target_value, pdf_value)
            
        elif exist == 1 and flag_none == 0:  # 此时代表从pdf_dict里面读出的数据不为None
            return self.compare_result('one', source, i, pdf_dict, target_value, pdf_value)
            

    def compare_value_2(self, i, target_dict, pdf_dict, source):
        if i not in target_dict:
            # 此键在jindi里面，而wind里面却没有该键
            print('msg', msg_3, '正在存入es...')
            return self.compare_result('three', source, i, pdf_dict)
            # return {'compare_source': source,
            #         'msg': msg_3,
            #         'wind_key': 'None',
            #         'pdf_value': pdf_dict[i],
            #         'pdf_key': i,
            #         'trade_code': self.trade_code,
            #         'sheet_type': self.sheet_type,
            #         'table_type': self.table_type,
            #         'end_date': self.end_date}

    def compare_result(self, key, source, i, pdf_dict, target_value='None', pdf_value='None'):
        if key == 'one':
            return {'compare_source': source,
                    'msg': msg_1,
                    'wind_key': i,
                    'wind_value': target_value,
                    'pdf_value': pdf_value,
                    'trade_code': self.trade_code,
                    'sheet_type': self.sheet_type,
                    'table_type': self.table_type,
                    'end_date': self.end_date}
        if key == 'two':
            return {'compare_source': source,
                    'msg': msg_2,
                    'wind_key': i,
                    'wind_value': target_value,
                    'pdf_key': 'None',
                    'trade_code': self.trade_code,
                    'sheet_type': self.sheet_type,
                    'table_type': self.table_type,
                    'end_date': self.end_date}
        if key == 'three':
            return {'compare_source': source,
                      'msg': msg_3,
                      'wind_key': 'None',
                      'pdf_value': pdf_dict[i],
                      'pdf_key': i,
                      'trade_code': self.trade_code,
                      'sheet_type': self.sheet_type,
                      'table_type': self.table_type,
                      'end_date': self.end_date}



    def achieve_value(self, i, a_dict):
        exist = 0
        flag_none = 0
        if i in a_dict:
            exist = 1
            if a_dict[i] != 'None':
                return exist, flag_none, a_dict[i]
            else:
                flag_none = 1
                return exist, flag_none, a_dict[i]
        else:
            return exist, flag_none, 0



def test_compare_function():
    es = Elasticsearch(hosts=['127.0.0.1:9200'])
    es_bhv = HjEsIO(es)
    table_compare = TableCompare(es_bhv)
    # 为了便于测试：先删除该index,再建立该index,若成功删除,则{'acknowledged': True}，
    # 若index原本就不存在，则response_result['status'] = 404
    es.indices.delete(index=error_pdf_index, ignore=[400, 404])
    # 创建一个空白的index
    es.indices.create(index=error_pdf_index, ignore=400)
    end_date_list = ['20171231']
    trade_code_list = ['600383']
    sheet_type_list = ['合并报表', '合并报表（调整）', '母公司报表', '母公司报表（调整）']
    table_type_list = ['资产负债表', '利润表', '现金流量表']

    for end_date, ori_trade_code, sheet_type, table_type in itertools.product(end_date_list, trade_code_list, sheet_type_list,table_type_list):
        print(end_date, ori_trade_code, sheet_type, table_type)

        trade_code = ori_trade_code

        jindi_pdf_dict = table_compare.get_dict(pdf_jindi_index,trade_code,end_date,sheet_type,table_type)
        wind_dict = table_compare.get_dict(wind_index,trade_code,end_date,sheet_type,table_type)

        a = table_compare.dict_compare(wind_dict, jindi_pdf_dict, source='wind')
        print(a)
        print('完成对 -- {} -- {} -- 的对比'.format(sheet_type, table_type))




def test_fix_row_data5():
    pdf_id = '1010120180418876561'
    table_name = '合并资产负债表'
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('table_list', table_name, pdf_id)
    table_list = local_bhv.read_pickle(pkl_path)
    all_fixed_rows_0 = {}  # 未调整
    all_fixed_rows_1 = {}  # 调整

    for table in table_list:
        fix_row_jindi = FixDataJindi(table_name[2:], table)
        data0, data1 = fix_row_jindi.execute_function()
        all_fixed_rows_0.update(data0)
        all_fixed_rows_1.update(data1)
    all_fixed_rows = {'未调整': all_fixed_rows_0, '调整': all_fixed_rows_1}
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('all_fixed_rows', table_name, pdf_id)
    local_bhv.to_pickle(all_fixed_rows, pkl_path)


def test_fix_row_data6():
    pdf_id = '1010120180418876561'
    table_name = '母公司资产负债表'
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('table_list', table_name, pdf_id)
    table_list = local_bhv.read_pickle(pkl_path)
    all_fixed_rows_0 = {}  # 未调整
    all_fixed_rows_1 = {}  # 调整
    for table in table_list:
        fix_row_jindi = FixDataJindi(table_name[3:], table)
        data0, data1 = fix_row_jindi.execute_function()
        all_fixed_rows_0.update(data0)
        all_fixed_rows_1.update(data1)
    all_fixed_rows = {'未调整': all_fixed_rows_0, '调整': all_fixed_rows_1}
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('all_fixed_rows', table_name, pdf_id)
    local_bhv.to_pickle(all_fixed_rows, pkl_path)


def test_fix_row_data7():
    pdf_id = '1010120180418876561'
    table_name = '合并利润表'
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('table_list', table_name, pdf_id)
    table_list = local_bhv.read_pickle(pkl_path)
    all_fixed_rows_0 = {}  # 未调整
    all_fixed_rows_1 = {}  # 调整
    for table in table_list:
        fix_row_jindi = FixDataJindi(table_name[2:], table)
        data0, data1 = fix_row_jindi.execute_function()
        all_fixed_rows_0.update(data0)
        all_fixed_rows_1.update(data1)
    all_fixed_rows = {'未调整': all_fixed_rows_0, '调整': all_fixed_rows_1}
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('all_fixed_rows', table_name, pdf_id)
    local_bhv.to_pickle(all_fixed_rows, pkl_path)


def test_fix_row_data8():
    pdf_id = '1010120180418876561'
    table_name = '母公司利润表'
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('table_list', table_name, pdf_id)
    table_list = local_bhv.read_pickle(pkl_path)
    all_fixed_rows_0 = {}  # 未调整
    all_fixed_rows_1 = {}  # 调整
    for table in table_list:
        fix_row_jindi = FixDataJindi(table_name[3:], table)
        data0, data1 = fix_row_jindi.execute_function()
        all_fixed_rows_0.update(data0)
        all_fixed_rows_1.update(data1)
    all_fixed_rows = {'未调整': all_fixed_rows_0, '调整': all_fixed_rows_1}
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('all_fixed_rows', table_name, pdf_id)
    local_bhv.to_pickle(all_fixed_rows, pkl_path)


def test_fix_row_data9():
    pdf_id = '1010120180418876561'
    table_name = '合并现金流量表'
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('table_list', table_name, pdf_id)
    table_list = local_bhv.read_pickle(pkl_path)
    all_fixed_rows_0 = {}  # 未调整
    all_fixed_rows_1 = {}  # 调整
    for table in table_list:
        fix_row_jindi = FixDataJindi(table_name[2:], table)
        data0, data1 = fix_row_jindi.execute_function()
        all_fixed_rows_0.update(data0)
        all_fixed_rows_1.update(data1)
    all_fixed_rows = {'未调整': all_fixed_rows_0, '调整': all_fixed_rows_1}
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('all_fixed_rows', table_name, pdf_id)
    local_bhv.to_pickle(all_fixed_rows, pkl_path)


def test_fix_row_data10():
    pdf_id = '1010120180418876561'
    table_name = '母公司现金流量表'
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('table_list', table_name, pdf_id)
    table_list = local_bhv.read_pickle(pkl_path)
    all_fixed_rows_0 = {}  # 未调整
    all_fixed_rows_1 = {}  # 调整
    for table in table_list:
        fix_row_jindi = FixDataJindi(table_name[3:], table)
        data0, data1 = fix_row_jindi.execute_function()
        all_fixed_rows_0.update(data0)
        all_fixed_rows_1.update(data1)
    all_fixed_rows = {'未调整': all_fixed_rows_0, '调整': all_fixed_rows_1}
    pkl_path = '.\process_file\{}_{}_{}.pkl'.format('all_fixed_rows', table_name, pdf_id)
    local_bhv.to_pickle(all_fixed_rows, pkl_path)




def test_save_jindi_to_es():

    # 为了便于测试：先删除该index,再建立该index,若成功删除,则{'acknowledged': True}，
    # 若index原本就不存在，则response_result['status'] = 404
    es.indices.delete(index=TO_INDEX, ignore=[400, 404])
    # 创建一个空白的index
    es.indices.create(index=TO_INDEX, ignore=400)
    trade_code = '600383'
    pdf_id = '1010120180418876561'  # 可在test_find_table中获得
    end_date = '20171231'  # 可在test_find_table中获得
    report_season = '年报'
    table_name_list = ['合并资产负债表', '母公司资产负债表', '合并利润表', '母公司利润表', '合并现金流量表', '母公司现金流量表']
    for table_name in table_name_list:
        pkl_path = '.\process_file\{}_{}_{}.pkl'.format('all_fixed_rows', table_name, pdf_id)
        file = local_bhv.read_pickle(pkl_path)
        sheet_type, table_type = sheet_table_type[table_name]
        sheet_type_1 = sheet_type + '（调整）'
        data0, data1 = file['未调整'], file['调整']
        data0.update({'end_date': end_date, 'report_seasion': report_season,
                      'sheet_type': sheet_type, 'table_type': table_type,
                      'trade_code': trade_code})
        data1.update({'end_date': end_date, 'report_seasion': report_season,
                      'sheet_type': sheet_type_1, 'table_type': table_type,
                      'trade_code': trade_code})
        es.index(index=TO_INDEX, doc_type='d_type', body=data0)
        es.index(index=TO_INDEX, doc_type='d_type', body=data1)
        print('--------------')







































