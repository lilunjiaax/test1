"""
1. 读取存储地产公司的pk文件，对每个地产公司进行遍历操作
2. 可以先获取所有的地产公司的目录（先统一执行获取目录操作）
3. 获取的目录存储在index:url_frm_wss_wind_index中
4. 获取的内容存储在index:wind_wss_index 中
5. 然后再对所有公司的目录进行获取内容操作
"""
#coding = utf-8
import pickle
from elasticsearch import Elasticsearch
from yhj_tool.wind_server_remote import WindDataRemote
from yfinfunc.get_url_frm import UrlStp
from yfinfunc.spider_wss import ContentStp, ParseData


class JvSpider:
    def __init__(self):
        self.elasticsearch_ip_port = '127.0.0.1:9200'
        self.url_frm_wss_index_name = 'url_frm_wss_wind_index'
        self.wind_wss_index_content = 'wind_wss_index'
        self.data = self.__load_pickle()

    # 此函数由于是直接将pk文件地址写死，需要注意，没有灵活性
    # 修改意见：可以将pk文件与此模块放入同一目录（只需要对pk文件存储的数据结构提出要求即可）,也可以利用sys模块
    def __load_pickle(self):
        """注意：pk文件存放在桌面上,文件路径为：C:\\Users\\jvlunl\\Desktop\\house.pk """
        with open('C:\\Users\\jvlunl\\Desktop\\house.pk', 'rb') as f:
            file = pickle.load(f)
        # 获取DataFrame对象：其中index为例：'000002.SZ',对应的columns为例：name（地产公司的name）
        f2 = file['f2']
        return f2  # 此时f2是一个DataFrame对象

    def ach_directory(self):
        """获取所有地产公司目录"""
        es = Elasticsearch(hosts=self.elasticsearch_ip_port)
        url_stp = UrlStp(es)
        url_frm_index = self.url_frm_wss_index_name
        trade_code_list = list(self.data.index)
        frm = url_stp.get_url_frm(url_frm_index, trade_code_list, date_begin='20170101', date_end='20190521')

    def ach_content(self, host):
        """按照目录获取内容，需要注意host限额问题
        1. 在spider_wss.py中有针对限额的报错程序，
        2. 故只需要当报错时利用try..except..对程序进行重启就可以
        """
        es = Elasticsearch(hosts=self.elasticsearch_ip_port)
        print('----------------------------------')
        print(es.count(index=self.url_frm_wss_index_name))
        url_frm_index = self.url_frm_wss_index_name
        wind_wss_index = self.wind_wss_index_content
        wind_bhv = WindDataRemote(host=host)
        parse_data = ParseData(wind_bhv)
        get_content = ContentStp(parse_data, es)
        get_content.get_content(url_frm_index, wind_wss_index)


def main():
    jv_spider = JvSpider()
    # 获取目录
    # jv_spider.ach_directory()
    host_list = ['192.168.0.106']

    for host in host_list:
        jv_spider.ach_content(host)
        # try:
        #     jv_spider.ach_content(host)
        #
        # except Exception as e:
        #     continue


if __name__ == '__main__':
    main()
