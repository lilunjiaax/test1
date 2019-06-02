from elasticsearch import Elasticsearch
from esfrm.es_class import HjEsIO
import itertools

ignore_list = ['trade_code', 'announce_date', 'final_announce_date', 'end_date', 'sheet_type', 'company_type','table_type','file_id','short_company_name','report_season']
pdf_index = 'pdf_index'
tushare_index = 'tushare_index'
wind_index = 'wind_wss_index'
error_pdf_index = 'error_compare_pdf_index'
error_pdf_index = 'error_compare_pdf_index_security'
msg_1 = "这个数值在在tushare或者wind里面的值不一样。"
msg_2 = "这个数值在tushare或者wind里面有且不为0，但metric_table_index的表中没有这个数据。"

class TableCompare:
    """数据对比"""
    def __init__(self,es_bhv):
        self.es_bhv = es_bhv
        pass

        # 根据传入的index_name,trade_code,end_date,sheet_type,table_type在elasticsearch数据库里面寻找
    def get_dict(self,index_name,trade_code,end_date,sheet_type,table_type):
        """
        根据不同index_name获取不同的dict数据
        :param index_name: 数据所在的index
        :param trade_code: 交易代码，如600548
        :param end_date: 报告期末，20171231
        :param sheet_type: 报告类型，合并报表
        :param table_type: 表格类型，资产负债表
        :return:
        """
        # 查询语句，self.es_bhv有es的所有执行函数
        res_list = self.es_bhv.es.search(index=index_name, doc_type='d_type',
                                         body={'query':{'bool':{'must':[{'term':{'trade_code.keyword':trade_code}},
                                                                        {'term': {'end_date.keyword': end_date}},
                                                                        {'term': {'sheet_type.keyword':sheet_type}},
                                                                        {'term': {'table_type.keyword': table_type}}]}}},
                                         size=10)['hits']['hits']
        # 对查找返回的结果进行判断，取值
        if res_list:
            tushare_dict = res_list[0]['_source']
            return tushare_dict
        else:
            return {}
        pass

    def dict_compare(self,target_dict,pdf_dict,source):
        """
        将两个dict进行对比
        :param target_dict: wind或者tushare数据
        :param pdf_dict: 鱼意自己的pdf数据
        :return:
        """
        if not pdf_dict:
            print('msg', "pdf_dict不存在。")
            print('--------------------------')
            return
        for i in ignore_list:
            try:
                target_dict.pop(i)
            except:
                continue
        for i in target_dict:
            content = self.compare_value(i,target_dict,pdf_dict,source)
            if content:
                self.es_bhv.update_row(error_pdf_index,content)
                self.es_bhv.es.indices.refresh(error_pdf_index)
                print(content)
                print('--------------------------')
                return content

    def compare_value(self,i,target_dict,pdf_dict,source):
        """
        比对单个值
        :param i: target_dict的某个键
        :param target_dict:wind或者tushare数据
        :param pdf_dict: 鱼意自己的pdf数据
        :return:
        """
        target_value = target_dict[i]
        if target_value != 'None':
            try:
                pdf_value = pdf_dict[i]
                if abs(float(target_value)-float(pdf_value)) >0.01:
                    print('msg',msg_1,'正在存入es...')
                    return {'category': 'metric_not_equal','pdf_id':pdf_dict['pdf_id'],'table_id':pdf_dict['table_id'],
                        'compare_source': source,'msg': msg_1,'wind_or_tushare_field':i,'wind_or_tushare_value':target_value,'pdf_value':pdf_value,'trade_code':pdf_dict['trade_code'],'sheet_type':pdf_dict['sheet_type'],'table_type':pdf_dict['table_type'],'end_date':pdf_dict['end_date']}
            except:
                print('msg', msg_2, '正在存入es...')
                return {'category': 'metric_not_found','pdf_id':pdf_dict['pdf_id'],'table_id':pdf_dict['table_id'],
                        'compare_source': source,'msg': msg_2,'wind_or_tushare_field':i,'wind_or_tushare_value':target_value,'pdf_value':None,'trade_code':pdf_dict['trade_code'],'sheet_type':pdf_dict['sheet_type'],'table_type':pdf_dict['table_type'],'end_date':pdf_dict['end_date']}

        pass


if __name__ == '__main__':
    table_compare = TableCompare(HjEsIO(Elasticsearch(hosts=['192.168.31.99:9200'])))
    end_date_list = ['20170331', '20170630', '20170930', '20171231', '20180331', '20180630', '20180930']
    trade_code_list = ['001965.SZ', '600377.SH', '600350.SH', '600548.SH', '200429.SZ', '000429.SZ', '600269.SH',
                       '601107.SH', '600020.SH', '600012.SH', '600033.SH', '000828.SZ', '000900.SZ', '600035.SH',
                       '601188.SH', '600368.SH', '601518.SH', '600106.SH', '000548.SZ', '601318.SH', '601601.SH',
                       '601319.SH', '601628.SH', '601336.SH', '000627.SZ', '600291.SH', '600030.SH', '601211.SH',
                       '601688.SH', '600837.SH', '000166.SZ', '000776.SZ', '600999.SH', '002736.SZ', '601066.SH',
                       '300059.SZ', '601881.SH', '600958.SH', '601901.SH', '601788.SH', '600061.SH', '601377.SH',
                       '002939.SZ', '601162.SH', '000783.SZ', '002673.SZ', '601108.SH', '601198.SH', '601878.SH',
                       '601990.SH', '000728.SZ', '002926.SZ', '600109.SH', '000987.SZ', '600369.SH', '601555.SH',
                       '002670.SZ', '002797.SZ', '601099.SH', '000750.SZ', '600909.SH', '002500.SZ', '000686.SZ',
                       '600155.SH', '601375.SH', '600621.SH', '600864.SH', '000712.SZ', '601398.SH', '601939.SH',
                       '601288.SH', '601988.SH', '600036.SH', '601328.SH', '601166.SH', '600000.SH', '600016.SH',
                       '601998.SH', '601818.SH', '000001.SZ', '600015.SH', '601169.SH', '601229.SH', '002142.SZ',
                       '600919.SH', '601009.SH', '600926.SH', '601838.SH', '601577.SH', '002936.SZ', '601997.SH',
                       '601128.SH', '600908.SH', '002839.SZ', '002807.SZ', '603323.SH']
    trade_code_list = ['600030.SH', '601211.SH', '601688.SH', '600837.SH', '000166.SZ', '000776.SZ', '600999.SH',
                      '002736.SZ', '601066.SH', '300059.SZ', '601881.SH', '600958.SH', '601901.SH', '601788.SH',
                      '600061.SH', '601377.SH', '002939.SZ', '601162.SH', '000783.SZ', '002673.SZ', '601108.SH',
                      '601198.SH', '601878.SH', '601990.SH', '000728.SZ', '002926.SZ', '600109.SH', '000987.SZ',
                      '600369.SH', '601555.SH', '002670.SZ', '002797.SZ', '601099.SH', '000750.SZ', '600909.SH',
                      '002500.SZ', '000686.SZ', '600155.SH', '601375.SH', '600621.SH', '600864.SH', '000712.SZ']
    sheet_type_list = ['合并报表', '合并报表（调整）', '母公司报表', '母公司报表（调整）']
    table_type_list = ['资产负债表', '利润表', '现金流量表']

                                                            # 生成参数的笛卡尔积
    for end_date, ori_trade_code, sheet_type, table_type in itertools.product(end_date_list, trade_code_list, sheet_type_list,table_type_list):
        print(end_date, ori_trade_code, sheet_type, table_type)
        trade_code = ori_trade_code[0:6]
        pdf_dict = table_compare.get_dict(pdf_index,trade_code,end_date,sheet_type,table_type)
        tushare_dict = table_compare.get_dict(tushare_index,trade_code,end_date,sheet_type,table_type)
        wind_dict = table_compare.get_dict(wind_index,trade_code,end_date,sheet_type,table_type)
        a = table_compare.dict_compare(tushare_dict,pdf_dict,source='tushare')
        b = table_compare.dict_compare(wind_dict,pdf_dict,source='wind')

























# balance_index_name = 'balance_std'
# profit_cash_index_name = 'profit_cash_std'
# unknown_field_index = 'unknown_field'
# phtml_index = 'phtml_base'
# final_tables_index = 'final_tables'
# tushare_index = 'tushare'
# diff_data = 'diff_data'
# host = '192.168.31.99:9200'
# host2 = '192.168.31.7:9200'
# es1 = Elasticsearch(hosts=[host])
# es2 = Elasticsearch(hosts=[host2])
#
# is_hebing = '1'
# is_adjust = '0'
# periods = ['20161231','20170331','20170630','20170930','20171231','20180331','20180630','20180930']
# trade_code_list = ['001965.SZ', '600377.SH', '600350.SH', '600548.SH', '200429.SZ', '000429.SZ', '600269.SH', '601107.SH', '600020.SH', '600012.SH', '600033.SH', '000828.SZ', '000900.SZ', '600035.SH', '601188.SH', '600368.SH', '601518.SH', '600106.SH', '000548.SZ', '601318.SH', '601601.SH', '601319.SH', '601628.SH', '601336.SH', '000627.SZ', '600291.SH', '600030.SH', '601211.SH', '601688.SH', '600837.SH', '000166.SZ', '000776.SZ', '600999.SH', '002736.SZ', '601066.SH', '300059.SZ', '601881.SH', '600958.SH', '601901.SH', '601788.SH', '600061.SH', '601377.SH', '002939.SZ', '601162.SH', '000783.SZ', '002673.SZ', '601108.SH', '601198.SH', '601878.SH', '601990.SH', '000728.SZ', '002926.SZ', '600109.SH', '000987.SZ', '600369.SH', '601555.SH', '002670.SZ', '002797.SZ', '601099.SH', '000750.SZ', '600909.SH', '002500.SZ', '000686.SZ', '600155.SH', '601375.SH', '600621.SH', '600864.SH', '000712.SZ', '601398.SH', '601939.SH', '601288.SH', '601988.SH', '600036.SH', '601328.SH', '601166.SH', '600000.SH', '600016.SH', '601998.SH', '601818.SH', '000001.SZ', '600015.SH', '601169.SH', '601229.SH', '002142.SZ', '600919.SH', '601009.SH', '600926.SH', '601838.SH', '601577.SH', '002936.SZ', '601997.SH', '601128.SH', '600908.SH', '002839.SZ', '002807.SZ', '603323.SH']
# for trade_code in trade_code_list:
#     trade_code = trade_code.split('.')[0]
#     for period in periods:
#         pdf_query = {'query':{'bool':{'must':[{'term':{'trade_code.keyword':trade_code}}, {'term':{'aggregate.keyword':is_hebing}}, {'term':{'adjust.keyword':is_adjust}}, {'term':{'type.keyword': 'balance'}}, {'term':{'period.keyword':period}}]}}}#{'term':{'status.keyword':'1'}},
#         pdf_res =es1.search(index=final_tables_index, body=pdf_query, size=100)
#         if not pdf_res['hits']['hits']:
#             continue
#         pdf_data = pdf_res['hits']['hits'][0]['_source']['data']
#         print(pdf_res['hits']['hits'][0]['_source']['title'])
#         pdf_data_list = []
#         for col in pdf_data:
#             try:
#                 pdf_data_list.append({col: float(pdf_data[col])})
#             except:
#                 pdf_data_list.append({col: pdf_data[col]})
#
#
#
#
#         tushare_query = {'query':{'bool':{'must':[{'term':{'trade_code.keyword':trade_code}}, {'term':{'aggregate.keyword':is_hebing}},  {'term':{'type.keyword': 'balance'}}, {'term':{'period.keyword':period}}]}}}
#         tushare_res = es1.search(index=tushare_index,body =tushare_query,size=100)
#         if not tushare_res:
#             continue
#         tushare_data = tushare_res['hits']['hits'][0]['_source']['data']
#         for i in ['ts_code', 'ann_date', 'f_ann_date', 'end_date', 'report_type', 'comp_type']:
#             tushare_data.pop(i)
#         tushare_data_list = []
#         for col in tushare_data:
#             tushare_data_list.append({col: tushare_data[col][0]})
#
#
#         def std_data(es, index_name, data_list, source, doc_type='d_type'):
#             new_data_dict = {}
#             unknown_data_list = []
#             for data in data_list:
#                 data_tuple = list(data.items())[0]
#                 query = {"query": {"bool": {"must": [{"term": {"alias.name.keyword": data_tuple[0]}},
#                                                      {"term": {"alias.source.keyword": source}}]}}}
#                 res = es.search(index=index_name, doc_type=doc_type, body=query, size=10000)
#                 if res['hits']['hits']:
#                     std_field = res['hits']['hits'][0]['_source']['alias']
#                     for field in std_field:
#                         if field['source'] == 'yuyi':
#                             try:
#                                 field_name = field['name'][0]
#                             except:
#                                 field_name = ''
#                             break
#                     if field_name == '':
#                         unknown_data_list.append(data)
#                         continue
#                     try:
#                         float(str(data_tuple[1]).replace(',', '').replace('，', ''))
#                         new_data_dict[field_name] = str(data_tuple[1]).replace(',', '').replace('，', '')
#                     except:
#                         new_data_dict[field_name] = str(data_tuple[1])
#                 else:
#                     unknown_data_list.append(data)
#             return new_data_dict, unknown_data_list
#         new_tushare_data = std_data(es1, balance_index_name, tushare_data_list, 'pdf')[0]
#         new_tushare_data_list = []
#         for item in new_tushare_data:
#             try:
#                 new_tushare_data_list.append({item[0]:float(item[1])})
#             except:
#                 new_tushare_data_list.append({item[0]: item[1]})
#
#
#         def compare( pdf_data_list, source_data_list):
#             res = pd.Series(source_data_list) - pd.Series(pdf_data_list)
#             compare_res = res[res.abs() > 0.1].dropna().to_dict()
#             return compare_res
#
#
#
#         compare_res =compare(pdf_data_list, new_tushare_data)
#         if compare_res:
#             print(compare_res)
#             body = {}
#             body['type'] = 'balance'
#             body['aggregate'] = is_hebing
#             body['adust'] = is_adjust
#             body['source'] = 'tushare'
#             body['title'] = pdf_res['hits']['hits'][0]['_source']['title']
#             body['pdf_id'] = pdf_res['hits']['hits'][0]['_source']['table']['pdf_id']
#             body['table_id'] = pdf_res['hits']['hits'][0]['_source']['table']['table'][0]['table_id']
#             body['diff_data'] = compare_res
#             body['add_date'] = datetime.datetime.now()
#             id =  tushare_res['hits']['hits'][0]['_id']+'_'+body['source']
#             es1.index(diff_data, doc_type='d_type', body=body)
#             es1.indices.refresh(index=diff_data)
