#coding:utf-8
"""
综合项目:世行历史数据基本分类及其可视化
作者：罗鑫
日期：2020.6.9

"""

import csv
import math
import pygal
import pygal_maps_world.maps
wm = pygal_maps_world.maps.World() #导入需要使用的库


def read_csv_as_nested_dict(filename, keyfield, separator, quote): #读取原始csv文件的数据，格式为嵌套字典
    
    result={}
    with open(filename,newline="")as csvfile:
        csvreader=csv.DictReader(csvfile,delimiter=separator,quotechar=quote)
        for row in csvreader:
            result[row[keyfield]]=row
    return result
   


pygal_countries = pygal.maps.world.COUNTRIES #读取pygal.maps.world中国家代码信息（为字典格式），其中键为pygal中各国代码，值为对应的具体国名(建议将其显示在屏幕上了解具体格式和数据内容）
# print(pygal_countries)


def reconcile_countries_by_name(plot_countries, gdp_countries): #返回在世行有GDP数据的绘图库国家代码字典，以及没有世行GDP数据的国家代码集合
    
    set1 = set()
    dict1 = {}
    for k,v in gdp_countries.items():
        crusial = set(v.values())
        if len(crusial) == 5:
            set1.add(from_value_to_key(k))
        else:
            dict1[from_value_to_key(k)] = k
    for key,value in plot_countries.items():
        if key not in dict1:
            set1.add(key)
    
    tuple1 = (dict1,set1)
    return tuple1


def from_value_to_key(value):           #通过定义value_to_key,key_to_value两函数实现国家代码缩写与国名的自由转换
    for k,v in pygal_countries.items():
        if v == value:
            return k

def from_key_to_value(key):               #同上
    for k,v in pygal_countries.items():
        if k == key:
            return v


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    
    dict2 = {}
    set2 = set()
    for key,value in gdpinfo.items():
        if from_value_to_key(key) in plot_countries[0]:               #遍历判断“有数据的国家信息”的国名里的键，进入下一个判断
            if value[year] != "":                                   #若此年无数据，则放入第一个集合里
                aeee = float(value[year])
                dict2[from_value_to_key(key)] = math.log(aeee)
            else:                                                 #若该年有数据，则放入字典里
                set2.add(from_value_to_key(key))
    tuple2 = (dict2,set2,plot_countries[1])
    return tuple2                                          #返回元组
    


def render_world_map(gdpinfo, plot_countries, year, map_file):

    dict3 = {}
    dict4 = {}
    list4 = list(gdpinfo[1])                             #集合无顺序，因此需变为列表进行遍历，放入字典中并赋值“1”
    list5 = list(gdpinfo[2])
    for values in list4:
        dict3[values] = "1"
    for i in list5:
        if i != None:                             #删除第二个集合中的空值
            dict4[i] = "1"
    
    # worldmap_chart = pygal.maps.world.World()
    wm.title = '全球GDP分布图'                      #数据可视化输出操作
    wm.add('%s'%year,gdpinfo[0])
    wm.add('missing from world bank',dict3)
    wm.add('no data at this year',dict4)
    wm.render_to_file(map_file)
    # print(map_file)


    
# pygal_countries = pygal.maps.world.COUNTRIES
print("欢迎使用世行GDP数据可视化查询")
print("----------------------")

year=input("请输入需查询的具体年份:")

love = read_csv_as_nested_dict("isp_gdp.csv","Country Name",",",'"')      #运行函数进行操作
# print(love) 
mymy = reconcile_countries_by_name(pygal_countries,love)                 #运行第二个函数，并将结果存为变量mymy
ymym = build_map_dict_by_name(love,mymy,year)                             #运行第三个函数，并将结果存为变量ymym
render_world_map(ymym,pygal_countries,year,"isp_gdp_world_name_%s.svg"%year)   
