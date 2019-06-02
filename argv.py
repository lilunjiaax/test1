
# {"query":{"bool":{"must":[{"term":{"pdf_id.keyword":"1010120180418876561"}},{"wildcard":{"table_info.text_list.keyword":"*资产负债表"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}
result = es.search('jindi_test_table',doc_type="d_type",body={"query":{"bool":{"must":[{"term":{"pdf_id.keyword":"1010120180418876561"}},{"wildcard":{"table_info.text_list.keyword":"*资产负债表"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}})

a = result['hits']['hits']
# 此时已经得到一个查询结果列表，列表中的每一项是一个字典，
# 开始考虑表被pdf页分段的问题，根据每一个查询结果看，一般我们会得到两个字典，（合并资产负债表字典（包含未调整，调整），母公司资产负债表字典（包含未调整，调整））
# 若得到的是多个字典，3个字典，考虑有一张表被分割了，4个字典，考虑有两张表被分割，或一张表被两次分割，对此我们采取的解决办法是同一通过每个字典table_info信息来判断这一张表为何？？
# 所以执行逻辑是：对于查询结果进行遍历，先读取这个字典里面的table_info信息，对这个字典的操作是：a['_source']['table_info'][0]['text_list'][0]--> '合并资产负债表'
# 先对


# 获取利润表的查询语句
# {"query":{"bool":{"must":[{"term":{"pdf_id.keyword":"1010120180418876561"}},{"wildcard":{"table_info.text_list.keyword":"*利润表"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}

# 获取现金流量表的查询语句
# {"query":{"bool":{"must":[{"term":{"pdf_id.keyword":"1010120180418876561"}},{"wildcard":{"table_info.text_list.keyword":"*现金流量表"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}

# 通过pdf_id来获取相应的trade_code,origin_title(能不能用来作为判断报告时间的依据)
# {"query":{"bool":{"must":[{"term":{"file_id.keyword":"1010120180418876561"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}


# 数据的写入需要对elasticsearch的每条记录进行多次更新,案例如下：
data = {'trade_code': '000002.SZ', 'sheet_type': '母公司报表'}
data3 = {'trade_code': '000002.SZ', 'sheet_type': '母公司报表','table_type':'资产负债表'}

# 先插入data数据
result = es.create(index='jvlunl_jindi_test', doc_type='d_type', id=10001, body=data)

# 再进行更新
result = es.update(index='jvlunl_jindi_test', doc_type='d_type', body={'doc':data3}, id=10001,ignore=400)
# 通过测试：的确是增量更新，不是覆盖更新
data4 = {'editor':'jvlunl'}
result = es.update(index='jvlunl_jindi_test', doc_type='d_type', body={'doc':data4}, id=10001,ignore=400)
# 通过验证得知：当插入_sources时键的值相同时(值的值也是相同的时候：数据并不改变,且_version的值也不改变，当值的值不相同时，会修改_sources里面的值，且_version增加1)





"""
流程思路：
1. 先根据pdf_id通过查询语句来获取相应的表的类型的数据：如资产负债表的数据，利润表的数据，现金流量表的数据，
2. 对获取到的数据进行处理，需要遍历，在遍历时需要处理好字典之间的嵌套关系，对便利到的数据挨个存储到wind_index类似的数据库中（数据结构要求相同）
注意存储时需要注意：哪些是调整表的数据，需要存储到调整表里面
3. 对于存储时的需要包含trade_code,end_date问题
trade_code:可以在stock_index_0922里面查找到trade_code(根据pdf_id)
end_date问题:
report_type:根据end_date确定（20170331，20170630，20170930，20171231）---> （一季报，中报，三季报，年报）



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
    "所有者权益": "None",
    "补充资料": "None",
    "oth_rcv_tot": "1537278495.51",
    '...':'.......' }
}


# 各种数据指标可以通过遍历获得，但每个index的发布报告时间和股票代码如何获取：通过pdf_id ???
# 对于上述的时间和trade_code问题：可以对每一个pdf-id在stock_index_0922中作查询得到origin_title和trade_code,
# 利用对origin_title的名称总结（年度报告，半年度报告，一季报，三季报等，利用模块）来确定生成数据的时间
# 查询语句为：{"query":{"bool":{"must":[{"term":{"file_id.keyword":"1010120180418876561"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}

# jindi_test_table的index名称为：pdf-id_table-id,所以是不是没有table的pdf页面就没有作识别数据处理



# a[1]和a[2]是合并资产负债表的部分，由于在pdf上此表在两个页面上，所以这两个部分存放在a[1]和a[2]中


# a[2]部分
{'_index': 'jindi_test_table', 
'_type': 'd_type', 
'_id': '1010120180418876561_62', 
'_score': 2.2764795, 
'_source': 
{'table_id': 62, 
'segments': 
[
{'rows':
[{'row_id': 0, 'tds': [{'col_name': '项目', 'value': '项目'}, {'col_name': '附注', 'value': '附注'}, {'col_name': '年末余额', 'value': '年末余额'}, {'col_name': '年初余额', 'value': '年初余额'}]}]},

# 资产的流动资产部分作为一个字典信息
{'rows': 
[
{'row_id': 2, 'tds': [{'col_name': '项目', 'value': '货币资金'}, {'col_name': '附注', 'value': '(五)1'}, {'col_name': '年末余额', 'value': '27,406,030,533.77'}, {'col_name': '年初余额', 'value': '21,564,986,458.13'}]}, 
{'row_id': 3, 'tds': [{'col_name': '项目', 'value': '结算备付金'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 4,'tds': [{'col_name': '项目', 'value': '拆出资金'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 5, 'tds': [{'col_name': '项目', 'value': '以公允价值计量且其变动计入当期损益的金融资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 6, 'tds': [{'col_name': '项目', 'value': '衍生金融资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 7, 'tds': [{'col_name': '项目', 'value': '应收票据'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 8, 'tds': [{'col_name': '项目', 'value': '应收账款'}, {'col_name': '附注', 'value': '(五)2'}, {'col_name': '年末余额', 'value': '62,107,124.92'}, {'col_name': '年初余额', 'value': '61,154,986.63'}]}, 
{'row_id': 9, 'tds': [{'col_name': '项目', 'value': '预付款项'}, {'col_name': '附注', 'value': '(五)3'}, {'col_name': '年末余额', 'value': '3,469,476,069.23'}, {'col_name': '年初余额', 'value': '3,871,387,617.25'}]},
{'row_id': 10, 'tds': [{'col_name': '项目', 'value': '应收保费'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 11, 'tds': [{'col_name': '项目', 'value': '应收分保账款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 12, 'tds': [{'col_name': '项目', 'value': '应收分保合同准备金'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 13, 'tds': [{'col_name': '项目', 'value': '应收利息'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 14, 'tds':[{'col_name': '项目', 'value': '应收股利'}, {'col_name': '附注', 'value': '(五)4'}, {'col_name': '年末余额', 'value': '35,000,000.00'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 15, 'tds': [{'col_name': '项目', 'value': '其他应收款'}, {'col_name': '附注', 'value': '(五)5'}, {'col_name': '年末余额', 'value': '49,681,122,300.09'}, {'col_name': '年初余额', 'value': '20,696,960,201.73'}]}, 
{'row_id': 16, 'tds': [{'col_name': '项目', 'value': '买入返售金融资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 17, 'tds': [{'col_name': '项目', 'value': '存货'}, {'col_name': '附注', 'value': '(五)6'}, {'col_name': '年末余额', 'value': '84,183,097,866.10'}, {'col_name': '年初余额', 'value': '71,776,661,992.42'}]}, 
{'row_id': 18, 'tds': [{'col_name': '项目', 'value': '持有待售资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 19, 'tds': [{'col_name': '项目', 'value': '一年内到期的非流动资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 20, 'tds': [{'col_name': '项目', 'value': '其他流动资产'}, {'col_name': '附注', 'value': '(五)7'}, {'col_name': '年末余额', 'value': '5,139,636,957.44'}, {'col_name': '年初余额', 'value': '6,773,981,164.49'}]}, 
{'row_id': 21, 'tds': [{'col_name': '项目', 'value': '流动资产合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '169,976,470,851.55'}, {'col_name': '年初余额', 'value': '124,745,132,420.65'}]}
], 
'inforow': '流动资产：'}, 


# 资产表的非流动资产部分作为表的一部分
{'rows': 
[
{'row_id': 23, 'tds': [{'col_name': '项目', 'value': '发放贷款及垫款'}, {'col_name': '附注', 'value': '(五)8'}, {'col_name': '年末余额', 'value': '1,473,358,811.91'}, {'col_name': '年初余额', 'value': '924,019,497.33'}]}, 
{'row_id': 24, 'tds': [{'col_name': '项目', 'value': '可供出售金融资产'}, {'col_name': '附注', 'value': '(五)9'}, {'col_name': '年末余额', 'value': '203,531,544.60'}, {'col_name': '年初余额', 'value': '192,857,485.90'}]}, 
{'row_id': 25, 'tds': [{'col_name': '项目', 'value': '持有至到期投资'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 26, 'tds': [{'col_name': '项目', 'value': '长期应收款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 27, 'tds': [{'col_name': '项目', 'value': '长期股权投资'}, {'col_name': '附注', 'value': '(五)10'}, {'col_name': '年末余额', 'value': '15,406,356,064.42'}, {'col_name': '年初余额', 'value': '9,882,742,980.77'}]}, 
{'row_id': 28, 'tds': [{'col_name': '项目', 'value': '投资性房地产'}, {'col_name': '附注', 'value': '(五)11'}, {'col_name': '年末余额', 'value': '16,317,595,007.00'}, {'col_name': '年初余额', 'value': '14,773,540,740.00'}]}, 
{'row_id': 29, 'tds': [{'col_name': '项目', 'value': '固定资产'}, {'col_name': '附注', 'value': '(五)12'}, {'col_name': '年末余额', 'value': '1,123,163,641.16'}, {'col_name': '年初余额', 'value': '1,195,196,652.04'}]}, 
{'row_id': 30, 'tds': [{'col_name': '项目', 'value': '在建工程'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 31, 'tds': [{'col_name': '项目', 'value': '工程物资'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 32, 'tds': [{'col_name': '项目', 'value': '固定资产清理'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value':'-'}]}, 
{'row_id': 33, 'tds': [{'col_name': '项目', 'value': '生产性生物资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 34, 'tds': [{'col_name': '项目', 'value': '油气资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 35, 'tds': [{'col_name': '项目', 'value': '无形资产'}, {'col_name': '附注', 'value': '(五)13'}, {'col_name': '年末余额', 'value': '48,075,569.71'}, {'col_name': '年初余额', 'value': '38,949,751.89'}]}, 
{'row_id': 36, 'tds': [{'col_name': '项目', 'value': '开发支出'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 37, 'tds': [{'col_name': '项目', 'value': '项目'}, {'col_name': '附注', 'value': '附注'}, {'col_name': '年末余额', 'value': '年末余额'}, {'col_name': '年初余额', 'value': '年初余额'}]}
], 
'inforow': '非流动资产：'}, 


# 负债表的流动负债部分作为一个字典
{'rows': 
[
{'row_id': 39, 'tds': [{'col_name': '项目', 'value': '短期借款'}, {'col_name': '附注', 'value': '(五)17'}, {'col_name': '年末余额', 'value': '2,350,969,617.41'}, {'col_name': '年初余额', 'value': '861,368,165.77'}]}, 
{'row_id': 40, 'tds': [{'col_name': '项目', 'value': '向中央银行借款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 41, 'tds': [{'col_name': '项目', 'value': '吸收存款及同业存放'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 42, 'tds': [{'col_name': '项目', 'value': '拆入资金'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 43, 'tds': [{'col_name': '项目', 'value': '以公允价值计量且其变动计入当期损益的金融负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 44, 'tds': [{'col_name': '项目', 'value': '衍生金融负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 45, 'tds': [{'col_name': '项目', 'value': '应付票据'}, {'col_name': '附注', 'value': '(五)18'}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '12,291,671.40'}]}, 
{'row_id': 46, 'tds': [{'col_name': '项目', 'value': '应付账款'}, {'col_name': '附注', 'value': '(五)19'}, {'col_name': '年末余额', 'value': '9,954,085,901.55'}, {'col_name': '年初余额', 'value': '13,394,774,936.84'}]}, 
{'row_id': 47, 'tds': [{'col_name': '项目', 'value': '预收款项'}, {'col_name': '附注', 'value': '(五)20'}, {'col_name': '年末余额', 'value': '57,948,241,014.05'}, {'col_name': '年初余额', 'value': '27,485,605,543.53'}]}, 
{'row_id': 48, 'tds': [{'col_name': '项目', 'value': '卖出回购金融资产款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 49, 'tds': [{'col_name': '项目', 'value': '应付手续费及佣金'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 50, 'tds': [{'col_name': '项目', 'value': '应付职工薪酬'}, {'col_name': '附注', 'value': '(五)21'}, {'col_name': '年末余额', 'value': '1,476,925,009.19'}, {'col_name': '年初余额', 'value': '875,589,128.73'}]}, 
{'row_id': 51, 'tds': [{'col_name': '项目', 'value': '应交税费'}, {'col_name': '附注', 'value': '(五)22'}, {'col_name': '年末余额', 'value': '2,046,082,803.08'}, {'col_name': '年初余额', 'value': '2,442,414,754.27'}]}, 
{'row_id': 52, 'tds': [{'col_name': '项目', 'value': '应付利息'}, {'col_name': '附注', 'value': '(五)23'}, {'col_name': '年末余额', 'value': '541,625,449.45'}, {'col_name': '年初余额', 'value': '400,576,233.59'}]}, 
{'row_id': 53, 'tds': [{'col_name': '项目', 'value': '应付股利'}, {'col_name': '附注', 'value': '(五)24'}, {'col_name': '年末余额', 'value': '30,505,421.60'}, {'col_name': '年初余额', 'value': '46,918,652.93'}]},
{'row_id': 54, 'tds': [{'col_name': '项目', 'value': '其他应付款'}, {'col_name': '附注', 'value': '(五)25'}, {'col_name': '年末余额', 'value': '19,086,417,248.64'}, {'col_name': '年初余额', 'value': '15,850,250,947.81'}]}, 
{'row_id': 55, 'tds': [{'col_name': '项目', 'value': '应付分保账款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 56, 'tds': [{'col_name': '项目', 'value': '保险合同准备金'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 57, 'tds': [{'col_name': '项目', 'value': '代理买卖证券款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 58, 'tds': [{'col_name': '项目', 'value': '代理承销证券款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 59, 'tds': [{'col_name': '项目', 'value': '持有待售负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 60, 'tds': [{'col_name': '项目', 'value': '一年内到期的非流动负债'}, {'col_name': '附注', 'value': '(五)26'}, {'col_name': '年末余额', 'value': '11,059,211,960.90'}, {'col_name': '年初余额', 'value': '7,246,382,077.30'}]}, 
{'row_id': 61, 'tds': [{'col_name': '项目', 'value': '其他流动负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 62, 'tds': [{'col_name': '项目', 'value': '流动负债合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '104,494,064,425.87'}, {'col_name': '年初余额', 'value': '68,616,172,112.17'}]}
], 
'inforow': '流动负债：'}, 



{'rows': 
[
{'row_id': 64, 'tds': [{'col_name': '项目', 'value': '长期借款'}, {'col_name': '附注', 'value': '(五)27'}, {'col_name': '年末余额', 'value': '17,362,836,326.52'}, {'col_name': '年初余额', 'value': '10,108,690,389.32'}]}, 
{'row_id': 65, 'tds': [{'col_name': '项目', 'value': '应付债券'}, {'col_name':'附注', 'value': '(五)28'}, {'col_name': '年末余额', 'value': '22,039,610,313.28'}, {'col_name': '年初余额', 'value': '18,417,982,920.89'}]}, 
{'row_id': 66, 'tds': [{'col_name': '项目', 'value':'其中：优先股'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 67, 'tds': [{'col_name': '项目', 'value': '永续债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 68, 'tds': [{'col_name': '项目', 'value': '长期应付款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 69, 'tds': [{'col_name': '项目', 'value': '长期应付职工薪酬'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 70, 'tds': [{'col_name': '项目', 'value': '专项应付款'}, {'col_name': '附注','value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 71, 'tds': [{'col_name': '项目', 'value': '预计负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 72, 'tds': [{'col_name': '项目', 'value': '递延收益'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 73, 'tds': [{'col_name': '项目', 'value': '递延所得税负债'}, {'col_name': '附注', 'value': '(五)15'}, {'col_name': '年末余额', 'value': '3,548,090,493.50'}, {'col_name': '年初余额', 'value': '3,387,541,847.86'}]}
], 
'inforow': '非流动负债：'}], 

'table_info': [{'row_id': 1877, 'text_list': ['合并资产负债表']}, {'row_id': 1878, 'text_list': ['单位：人民币元']}], 
'table_unit': [['单位', '人民币元']], 
'pdf_id': '1010120180418876561'
 }
 }




# a[1]部分：作为资产负债表的下一页的续表，注意：他可能没有第一个rows字典

a1 = {
'_index': 'jindi_test_table', 
'_type': 'd_type', 
'_id': '1010120180418876561_63', 
'_score': 2.3317354, 
'_source': 
{
'table_id': 63, 
'segments': 
[

{'rows': 
[
{'row_id': 0, 'tds': [{'col_name': '项目', 'value': '项目'}, {'col_name': '附注', 'value': '附注'}, {'col_name': '年末余额', 'value': '年末余额'}, {'col_name': '年初余额', 'value': '年初余额'}]}, 
{'row_id': 1, 'tds': [{'col_name': '项目', 'value': '商誉'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 2, 'tds': [{'col_name': '项目', 'value': '长期待摊费用'}, {'col_name': '附注', 'value': '(五)14'}, {'col_name': '年末余额', 'value': '65,313,970.16'}, {'col_name': '年初余额', 'value': '77,207,132.42'}]}, 
{'row_id': 3, 'tds': [{'col_name': '项目', 'value': '递延所得税资产'}, {'col_name': '附注', 'value': '(五)15'}, {'col_name': '年末余额', 'value': '2,241,350,996.94'}, {'col_name': '年初余额', 'value': '1,639,354,376.78'}]}, 
{'row_id': 4, 'tds': [{'col_name': '项目', 'value': '其他非流动资产'}, {'col_name': '附注', 'value': '(五)16'}, {'col_name': '年末余额', 'value': '1,086,850,000.00'}, {'col_name': '年初余额', 'value':'165,257,899.47'}]}, 
{'row_id': 5, 'tds': [{'col_name': '项目', 'value': '非流动资产合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '37,965,595,605.90'}, {'col_name': '年初余额', 'value': '28,889,126,516.60'}]}, 
{'row_id': 6, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 7, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 8, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 9, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 10, 'tds': [{'col_name': '项目','value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 11, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 12, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value':''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 13, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 14, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''},{'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 15, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 16, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 17, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 18, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]}, 
{'row_id': 19, 'tds': [{'col_name': '项目', 'value': '资产总计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '207,942,066,457.45'}, {'col_name': '年初余额', 'value': '153,634,258,937.25'}]}, 
{'row_id': 20, 'tds': [{'col_name': '项目', 'value': '项目'}, {'col_name': '附注', 'value': '附注'}, {'col_name': '年末余额', 'value': '年末余额'}, {'col_name': '年初余额', 'value': '年初余额'}]}, 
{'row_id': 21, 'tds':[{'col_name': '项目', 'value': '其他非流动负债'}, {'col_name': '附注', 'value': '(五)29'}, {'col_name': '年末余额', 'value': '2,541,500,000.00'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 22, 'tds': [{'col_name': '项目', 'value': '非流动负债合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '45,492,037,133.30'}, {'col_name': '年初余额', 'value': '31,914,215,158.07'}]}, 
{'row_id': 23, 'tds': [{'col_name': '项目', 'value': '负债合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '149,986,101,559.17'}, {'col_name': '年初余额', 'value': '100,530,387,270.24'}]}
]
}, 

{'rows': 
[
{'row_id': 25, 'tds': [{'col_name': '项目', 'value': '股本'}, {'col_name': '附注', 'value': '(五)30'}, {'col_name': '年末余额', 'value': '4,514,583,572.00'}, {'col_name': '年初余额', 'value': '4,513,631,772.00'}]}, 
{'row_id': 26, 'tds': [{'col_name': '项目', 'value': '其他权益工具'}, {'col_name': '附注', 'value': '(五)31'}, {'col_name': '年末余额', 'value': '84,635,169.54'}, {'col_name': '年初余额', 'value': '95,325,455.65'}]}, 
{'row_id': 27, 'tds': [{'col_name': '项目', 'value': '其中：优先股'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 28, 'tds': [{'col_name': '项目', 'value': '永续债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 29, 'tds': [{'col_name': '项目', 'value': '资本公积'}, {'col_name': '附注', 'value': '(五)32'}, {'col_name':'年末余额', 'value': '3,455,701,136.44'}, {'col_name': '年初余额', 'value': '3,615,861,962.43'}]}, 
{'row_id': 30, 'tds': [{'col_name': '项目', 'value': '减：库存股'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 31, 'tds': [{'col_name': '项目', 'value': '其他综合收益'}, {'col_name': '附注', 'value': '(五)33'}, {'col_name': '年末余额', 'value': '263,665,481.00'}, {'col_name': '年初余额', 'value': '443,748,762.50'}]}, 
{'row_id': 32, 'tds': [{'col_name': '项目', 'value': '专项储备'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 33, 'tds': [{'col_name': '项目', 'value': '盈余公积'}, {'col_name': '附注', 'value': '(五)34'}, {'col_name': '年末余额', 'value': '2,174,040,296.18'}, {'col_name': '年初余额', 'value': '1,875,472,664.24'}]}, 
{'row_id': 34, 'tds': [{'col_name': '项目', 'value': '一般风险准备'},{'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]}, 
{'row_id': 35, 'tds': [{'col_name': '项目', 'value': '未分配利润'}, {'col_name': '附注', 'value': '(五)35'}, {'col_name': '年末余额', 'value': '30,271,432,294.23'}, {'col_name': '年初余额', 'value': '26,886,865,734.15'}]}, 
{'row_id': 36, 'tds': [{'col_name': '项目', 'value': '归属于母公司股东权益合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '40,764,057,949.39'}, {'col_name': '年初余额', 'value': '37,430,906,350.97'}]}, 
{'row_id': 37, 'tds': [{'col_name': '项目', 'value': '少数股东权益'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '17,191,906,948.89'}, {'col_name': '年初余额', 'value': '15,672,965,316.04'}]}, 
{'row_id': 38, 'tds': [{'col_name': '项目', 'value': '股东权益合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '57,955,964,898.28'}, {'col_name': '年初余额', 'value': '53,103,871,667.01'}]}, 
{'row_id': 39, 'tds': [{'col_name': '项目', 'value': '负债和股东权益总计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '207,942,066,457.45'}, {'col_name': '年初余额', 'value': '153,634,258,937.25'}]}
], 
'inforow': '股东权益：'
}

], 
'table_info': [{'row_id': 1883, 'text_list': ['合并资产负债表']}, {'row_id': 1884, 'text_list': ['单位：人民币元']}], 
'table_unit': [['单位', '人民币元']], 
'pdf_id': '1010120180418876561'}
}


# a[0]部分：母公司资产负债表，由于在pdf上此表全在一个页面上，所以就存在a[0]里面
b =
{
'_index': 'jindi_test_table',
'_type': 'd_type',
'_id': '1010120180418876561_64',
'_score': 2.4004788,
'_source':
{
'table_id': 64,
'segments':
[


{'rows':
[
{'row_id': 0, 'tds': [{'col_name': '项目', 'value': '项目'}, {'col_name': '附注', 'value': '附注'}, {'col_name': '年末余额', 'value': '年末余额'}, {'col_name': '年初余额', 'value': '年初余额'}]}]},



{'rows':
[
{'row_id': 2, 'tds': [{'col_name': '项目', 'value': '货币资金'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '7,156,609,761.55'}, {'col_name': '年初余额', 'value': '9,596,178,329.08'}]},
{'row_id': 3, 'tds': [{'col_name': '项目', 'value': '以公允价值计量且其变动计入当期损益的金融资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 4, 'tds': [{'col_name': '项目', 'value': '衍生金融资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 5, 'tds': [{'col_name': '项目', 'value': '应收票据'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 6, 'tds': [{'col_name': '项目', 'value': '应收账款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '22,975.94'}, {'col_name': '年初余额', 'value': '32,842.83'}]},
{'row_id': 7, 'tds': [{'col_name': '项目', 'value': '预付款项'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '290,312.14'}, {'col_name': '年初余额', 'value': '289,836.10'}]},
{'row_id': 8, 'tds': [{'col_name': '项目', 'value': '应收利息'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 9,'tds': [{'col_name': '项目', 'value': '应收股利'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '19,826,888.91'}]},
{'row_id': 10,'tds': [{'col_name': '项目', 'value': '其他应收款'}, {'col_name': '附注', 'value': '(十五)1'}, {'col_name': '年末余额', 'value': '72,549,633,026.85'}, {'col_name': '年初余额', 'value': '45,698,639,327.57'}]},
{'row_id': 11, 'tds': [{'col_name': '项目', 'value': '存货'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '2,935,905.85'}, {'col_name': '年初余额', 'value': '2,935,905.85'}]}, {'row_id': 12, 'tds': [{'col_name': '项目', 'value': '持有待售资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 13, 'tds': [{'col_name': '项目', 'value': '一年内到期的非流动资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 14, 'tds': [{'col_name': '项目', 'value': '其他流动资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '100,067,657.47'}, {'col_name': '年初余额', 'value': '2,200,063,181.63'}]},
{'row_id': 15, 'tds': [{'col_name': '项目', 'value': '流动资产合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '79,809,559,639.80'},{'col_name': '年初余额', 'value': '57,517,966,311.97'}]}
],
'inforow': '流动资产：'},



{'rows':
[
{'row_id': 17, 'tds': [{'col_name': '项目', 'value': '可供出售金融资产'}, {'col_name': '附注', 'value': '(十五)2'}, {'col_name': '年末余额', 'value': '100,000,000.00'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 18, 'tds': [{'col_name': '项目', 'value': '持有至到期投资'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 19, 'tds': [{'col_name': '项目', 'value': '长期应收款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 20, 'tds': [{'col_name': '项目', 'value': '长期股权投资'}, {'col_name': '附注', 'value':'(十五)3'}, {'col_name': '年末余额', 'value': '21,309,718,618.69'}, {'col_name': '年初余额', 'value': '23,957,515,721.52'}]},
{'row_id': 21, 'tds': [{'col_name': '项目', 'value': '投资性房地产'}, {'col_name': '附注', 'value': '(十五)4'}, {'col_name': '年末余额', 'value': '511,793,704.00'}, {'col_name': '年初余额', 'value': '429,000,000.00'}]},
{'row_id': 22, 'tds': [{'col_name': '项目','value': '固定资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '125,381,713.16'}, {'col_name': '年初余额', 'value': '140,359,918.73'}]},
{'row_id': 23, 'tds': [{'col_name': '项目', 'value': '在建工程'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 24, 'tds': [{'col_name': '项目', 'value': '工程物资'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 25, 'tds': [{'col_name': '项目', 'value': '固定资产清理'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 26, 'tds': [{'col_name': '项目', 'value': '生产性生物资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 27, 'tds': [{'col_name': '项目', 'value': '油气资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 28, 'tds': [{'col_name': '项目', 'value': '无形资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 29, 'tds': [{'col_name': '项目', 'value': '开发支出'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 30, 'tds': [{'col_name': '项目', 'value': '商誉'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 31, 'tds': [{'col_name': '项目', 'value': '长期待摊费用'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '2,735,727.89'}, {'col_name': '年初余额', 'value': '3,670,238.87'}]},
{'row_id': 32, 'tds': [{'col_name': '项目', 'value': '递延所得税资产'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '243,899,770.87'}, {'col_name': '年初余额', 'value': '136,295,770.86'}]},
{'row_id': 33, 'tds': [{'col_name': '项目', 'value': '其他非流动资产'}, {'col_name':'附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 34, 'tds': [{'col_name': '项目', 'value': '非流动资产合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '22,293,529,534.61'}, {'col_name': '年初余额', 'value': '24,666,841,649.98'}]},
{'row_id': 35, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]},
{'row_id': 36, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]},
{'row_id': 37, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]},
{'row_id': 38, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]},
{'row_id': 39, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]},
{'row_id': 40, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]},
{'row_id': 41, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]},
{'row_id': 42, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]},
{'row_id': 43, 'tds': [{'col_name': '项目', 'value': ''}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': ''}, {'col_name': '年初余额', 'value': ''}]},
{'row_id': 44, 'tds': [{'col_name': '项目', 'value': '资产总计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '102,103,089,174.41'}, {'col_name': '年初余额', 'value': '82,184,807,961.95'}]},
{'row_id': 45, 'tds': [{'col_name': '项目', 'value': '项目'}, {'col_name': '附注', 'value': '附注'}, {'col_name': '年末余额', 'value': '年末余额'}, {'col_name': '年初余额', 'value': '年初余额'}]}
],
'inforow': '非流动资产：'},

## 结合两张资产负债发现，负债那一栏的第一行都会在资产栏的最后一行

{'rows':
[
{'row_id': 47, 'tds': [{'col_name': '项目', 'value': '短期借款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '387,500,000.00'}, {'col_name': '年初余额', 'value': '248,000,000.00'}]},
{'row_id': 48, 'tds': [{'col_name': '项目', 'value': '以公允价值计量且其变动计入当期损益的金融负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 49, 'tds': [{'col_name': '项目', 'value': '衍生金融负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 50, 'tds': [{'col_name': '项目', 'value': '应付票据'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '2,291,671.40'}]},
{'row_id': 51, 'tds': [{'col_name': '项目', 'value': '应付账款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '3,348,334.65'}, {'col_name': '年初余额', 'value': '6,650,277.68'}]},
{'row_id': 52, 'tds': [{'col_name': '项目', 'value': '预收款项'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '471,934.39'}, {'col_name': '年初余额', 'value': '471,934.39'}]},
{'row_id': 53, 'tds': [{'col_name': '项目', 'value': '应付职工薪酬'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '699,030,610.00'}, {'col_name': '年初余额', 'value': '302,523,021.89'}]},
{'row_id': 54, 'tds': [{'col_name': '项目', 'value': '应交税费'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '17,240,205.37'}, {'col_name': '年初余额', 'value': '11,164,421.66'}]},
{'row_id': 55, 'tds': [{'col_name': '项目', 'value': '应付利息'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '504,778,097.45'}, {'col_name': '年初余额', 'value': '382,561,833.64'}]},
{'row_id': 56, 'tds': [{'col_name': '项目', 'value': '应付股利'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 57, 'tds': [{'col_name': '项目', 'value': '其他应付款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '29,791,197,593.25'}, {'col_name': '年初余额', 'value': '24,133,584,051.41'}]},
{'row_id': 58, 'tds': [{'col_name': '项目', 'value': '持有待售负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 59, 'tds': [{'col_name': '项目', 'value': '一年内到期的非流动负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '10,579,400,549.57'}, {'col_name': '年初余额', 'value': '6,432,140,000.00'}]},
{'row_id': 60, 'tds': [{'col_name': '项目', 'value': '其他流动负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 61, 'tds': [{'col_name': '项目', 'value': '流动负债合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '41,982,967,324.68'}, {'col_name': '年初余额', 'value': '31,519,387,212.07'}]}
],
'inforow': '流动负债：'},


{'rows':
[
{'row_id': 63, 'tds': [{'col_name': '项目', 'value': '长期借款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '16,761,500,000.00'}, {'col_name': '年初余额', 'value': '9,650,320,000.00'}]},
{'row_id': 64, 'tds': [{'col_name': '项目', 'value': '应付债券'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '20,746,793,587.90'}, {'col_name': '年初余额', 'value': '18,255,977,599.01'}]},
{'row_id': 65, 'tds': [{'col_name': '项目', 'value': '其中：优先股'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 66, 'tds': [{'col_name': '项目', 'value': '永续债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 67, 'tds': [{'col_name': '项目', 'value': '长期应付款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 68, 'tds': [{'col_name': '项目', 'value': '长期应付职工薪酬'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 69, 'tds': [{'col_name': '项目', 'value': '专项应付款'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 70, 'tds': [{'col_name': '项目', 'value': '预计负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 71, 'tds': [{'col_name': '项目', 'value': '递延收益'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 72, 'tds': [{'col_name': '项目', 'value': '递延所得税负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '125,582,375.02'}, {'col_name': '年初余额', 'value': '104,883,949.02'}]},
{'row_id': 73, 'tds': [{'col_name': '项目', 'value': '其他非流动负债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 74, 'tds': [{'col_name': '项目', 'value': '非流动负债合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '37,633,875,962.92'}, {'col_name': '年初余额', 'value': '28,011,181,548.03'}]},
{'row_id': 75, 'tds': [{'col_name': '项目', 'value': '负债合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '79,616,843,287.60'}, {'col_name': '年初余额', 'value': '59,530,568,760.10'}]}
],
'inforow': '非流动负债：'},


{'rows':
[
{'row_id': 77, 'tds': [{'col_name': '项目', 'value': '股本'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '4,514,583,572.00'}, {'col_name': '年初余额', 'value': '4,513,631,772.00'}]},
{'row_id': 78, 'tds': [{'col_name': '项目', 'value': '其他权益工具'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '2,321,153.87'}]},
{'row_id': 79, 'tds': [{'col_name': '项目', 'value': '其中：优先股'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额','value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 80, 'tds': [{'col_name': '项目', 'value': '永续债'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 81, 'tds': [{'col_name': '项目', 'value': '资本公积'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '6,393,083,122.86'}, {'col_name': '年初余额', 'value': '6,385,841,162.99'}]},
{'row_id': 82, 'tds': [{'col_name': '项目', 'value': '减：库存股'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 83, 'tds': [{'col_name': '项目', 'value': '其他综合收益'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 84, 'tds': [{'col_name': '项目', 'value': '专项储备'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 85, 'tds': [{'col_name': '项目', 'value': '盈余公积'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '2,174,040,296.18'}, {'col_name': '年初余额', 'value': '1,875,472,664.24'}]},
{'row_id': 86, 'tds': [{'col_name': '项目', 'value': '一般风险准备'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '-'}, {'col_name': '年初余额', 'value': '-'}]},
{'row_id': 87, 'tds': [{'col_name': '项目', 'value': '未分配利润'}, {'col_name': '附注', 'value': '(十五)5'}, {'col_name': '年末余额', 'value': '9,404,538,895.77'}, {'col_name': '年初余额', 'value': '9,876,972,448.75'}]},
{'row_id': 88, 'tds': [{'col_name': '项目', 'value': '股东权益合计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '22,486,245,886.81'}, {'col_name': '年初余额', 'value': '22,654,239,201.85'}]},
{'row_id': 89, 'tds': [{'col_name': '项目', 'value': '负债和股东权益总计'}, {'col_name': '附注', 'value': ''}, {'col_name': '年末余额', 'value': '102,103,089,174.41'}, {'col_name': '年初余额', 'value': '82,184,807,961.95'}]}
],
'inforow': '股东权益：'}

],
'table_info': [{'row_id': 1898, 'text_list': ['母公司资产负债表']}, {'row_id': 1899, 'text_list': ['单位：人民币元']}],
'table_unit': [['单位', '人民币元']],
'pdf_id': '1010120180418876561'}}


















