a_str = '12,42,34.34）'
print(a_str.replace(',','').replace('（','').replace('）',''))


# yuyi_std_map
{
"_index": "yuyi_std_map",
"_type": "d_type",
"_id": "xuUPN2gB2AXrgNEP33SF",
"_version": 1,
"_score": 1,
"_source": 
{ "alias": 
	[ 
	{ "source": "指标类型","name": [ "利润表"]},
	{ "source": "yuyi","name": [ "reinsur_inc"]},
	{ "source": "wind","name": [ "reinsur_inc"]},
	{ "source": "tushare","name": [ "reins_income"]},
	{ "source": "pdf","name": [ "分保费收入"]}
	],
	"field_name": "分保费收入"}
}
data = { 
	"alias": 
	[ 
	{ "source": "指标类型","name": [ "利润表"]},
	{ "source": "yuyi","name": [ "reinsur_inc"]},
	{ "source": "wind","name": [ "reinsur_inc"]},
	{ "source": "tushare","name": [ "reins_income"]},
	{ "source": "pdf","name": [ "分保费收入"]}
	],
	"field_name": "分保费收入"}

result = es.index(index='jvlunl_jindi_test', doc_type='d_type', body=data)


应付债券-永续债
应付债券-优先股


其他权益工具-永续债
其他权益工具-优先股


"end_date": "20170630",
"sheet_type": "合并报表",
"report_season": "中报",
"table_type": "现金流量表",
"trade_code": "000002",


"end_date": "20170930",
"sheet_type": "合并报表（调整）",
"report_season": "三季报",
"table_type": "资产负债表",
"trade_code": "000002",







