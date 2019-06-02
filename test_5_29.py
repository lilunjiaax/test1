class A:
    def aa(self,num):
        print('aaaa',num)


class B(A):
    def bb(self,num2):
        print('bbb',num2)



a = A()
a.aa(2)

b = B()
b.bb(333)


cc = {'aaa': 'xxx', 'sss': 'ccc'}
for i in cc:
    print(cc[i])

print('aaa' in cc)   # ---> True

que = '永续股'
print('出现缺失：{}'.format(que))
c = input("请输入替换值：")
print('------------------')
print('{} ----------> {}'.format(que, c))

a_dict = {'aa':'asd'}
from test_5_29_2 import AA
aaa = AA()
for i in range(3):
    aaa.a(a_dict)

print(a_dict)


# es.search('yuyi_std_map',doc_type = 'd_type', body={"query":{"bool":{"must":[{"term":{"alias.name.keyword":"期初现金及现金等价物余额"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}})['hits']['hits']
pk = \
[
{
    '_index': 'yuyi_std_map',
    '_type': 'd_type',
    '_id': 'YeUPN2gB2AXrgNEP33WF',
    '_score': 4.001254,
    '_source':
        {'alias':
             [
                 {'source': '指标类型', 'name': ['现金流量表']},
                 {'source': 'yuyi', 'name': ['cash_cash_equ_beg_period']},
                 {'source': 'wind', 'name': ['cash_cash_equ_beg_period']},
                 {'source': 'tushare', 'name': ['c_cash_equ_beg_period']},
                 {'source': 'pdf', 'name': ['期初现金及现金等价物余额', '期初现金及现金等价物余额__筹资活动产生的现金流量']}
             ],
            'field_name': '期初现金及现金等价物余额'}
}
]

print(pk)

'''
>>> pk
[{'_index': 'yuyi_std_map', '_type': 'd_type', '_id': 'YeUPN2gB2AXrgNEP33WF', '_score': 4.001254, '_source': {'alias': [{'source': '指标类型', 'nam
e': ['现金流量表']}, {'source': 'yuyi', 'name': ['cash_cash_equ_beg_period']}, {'source': 'wind', 'name': ['cash_cash_equ_beg_period']}, {'source':
 'tushare', 'name': ['c_cash_equ_beg_period']}, {'source': 'pdf', 'name': ['期初现金及现金等价物余额', '期初现金及现金等价物余额__筹资活动产生的现
金流量']}], 'field_name': '期初现金及现金等价物余额'}}]
>>> pk[0]['_source']['alias'][1]
{'source': 'yuyi', 'name': ['cash_cash_equ_beg_period']}
>>> pk[0]['_source']['alias'][1]['name']
['cash_cash_equ_beg_period']
>>> pk[0]['_source']['alias'][1]['name'][0]
'cash_cash_equ_beg_period'


'''
