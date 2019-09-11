import os
import re
import time
shuiyin_str = "<p class='x'>所有最新极客时间课程请加QQ群170701297</p>"


from_dir = 'C:\\Users\\jvlunl\\Desktop\\极客时间测试52讲'

dest_dir = "C:\\Users\\jvlunl\\Desktop\\极客时间测试52讲去水印版"

a_list = []
os.chdir(from_dir)
for i in os.listdir():
    a_list.append(from_dir+os.sep+i)

os.chdir(dest_dir)

for i in a_list:
    f = open(i, encoding="utf8")
    a_str = f.read()
    b_str = re.sub(r'<p class="x">所有最新极客时间课程请加QQ群170701297</p>', '', a_str)
    with open(os.path.split(i)[1], "w", encoding="utf8") as f1:
        print("开始写入{}".format(os.path.split(i)[1]))
        time.sleep(0.5)
        f1.write(b_str)

    






