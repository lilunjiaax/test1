import xlwt
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('sheet1')
j = 0
# for i in p.keys():
#
#     sheet.write(j,1,i)
#     j+=1
# wbk.save('kk.xls')


def read_from_index(items):
    global j
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
                sheet.write(j,1,key)
                j+=1
                value0 = line['tds'][2]['value']
                value1 = line['tds'][3]['value']
                if value0 == '-':
                    value0 = 'None'
                if value1 == '-':
                    value1 = 'None'
                data0.update({key: value0})
                data1.update({key: value1})

    print('----------------------------------------------------')
    print(data1)
    print(len(data1.keys()))



a1 = {'_index': 'jindi_test_table',
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

a2 = {
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

read_from_index(a1)

read_from_index(a2)

wbk.save('jindi_test.xls')
