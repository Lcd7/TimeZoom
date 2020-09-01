'''
例子：
https://www.cnblogs.com/dgwblog/p/11811562.html#/zh-cn/intro
'''

from pyecharts.charts import Bar

bar = Bar()
bar.add_xaxis(['衬衫', '羊毛衫', '雪纺衫', '裤子', '袜子'])
bar.add_yaxis("商家A", [5, 20, 15, 8, 90])
bar.add_yaxis("商家B", [4, 23, 12, 13, 70])
bar.render()
