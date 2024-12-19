import requests
import math
import time
import pandas as pd
import json
from datetime import datetime, timedelta

# def calculate_future_date(start_date_str, days_to_add):
#     # 将字符串转换为datetime对象
#     start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
#
#     # 计算新的日期
#     future_date = start_date + timedelta(days=days_to_add)
#
#     # 输出新的日期
#     return future_date.strftime('%Y-%m-%d')

def get_paginated_results(base_url, monitor_type,headers, params):
    # params['pageSize'] = page_size
    all_results1 = []
    page = 1
    time1 = 0.1
    while True:
        params['currentPage'] = page
        response = requests.post(f"{base_url}/{monitor_type}/keys", headers=headers, data=params)
        time.sleep(time1)
        # time1 = 0.1
        response.raise_for_status()
        data = response.json()
        all_results1.extend(data['response_data']['result'])
        # print(all_results)
        if page * 20 >= data['response_data']['pagination']['totalRecord']:
            # totalcount_results.extend([{"app_name":params["appName"],"monitor_type":monitor_type, "totalRecord":data['response_data']['pagination']['totalRecord']}])
            return all_results1
        page += 1


# start_date = '2023-11-07'  # 起始日期
# days_to_add = 41  # 要添加的天数
# new_date = calculate_future_date(start_date, days_to_add)
# print(f"新的日期是: {new_date}")

# 配置你的请求参数
base_url = "https://api-pserve-proxy.jd.com/api/ump/v1"  # 替换为你的实际 API URL
# headers = {
#         # "Content-Type": "application/json",
#         "token": "jwt::eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsaXlhbmcxNTU5IiwiaXNzIjoidW1wIiwic3ViIjoie1wiZXJwXCI6XCJsaXlhbmcxNTU5XCIsXCJxcG1cIjoyMDAsXCJzdGFydFRpbWVzdGFtcFwiOjE3MjQyMzMxOTI3NTcsXCJlbmRUaW1lc3RhbXBcIjoxNzI0ODM3OTkyNzU3LFwiYm91bmRBcHBDb29yZHNcIjpbXCJcIl19In0.lfH00U9WimyKGgp4hif5wiZSHyfCCM1drmhFoLWZ9RU"
# }
Cookie_value = "ssa.origin-gateway.state=BpSrsVM5C9AoMZvxa8z3xuwhY9E-DQxOadm0lhgiKHE; jd.erp.lang=zh_CN; jdd69fo72b8lfeoe=MG5ZEYF5AZ4O7BJ352SACAE3PCTDJLQWTSNPCCIEAGT6FO4XKEFHWCG7ZS72ELAZGXJHGT47IJ2HJCG462QROQ3ARQ; sso.jd.com=BJ.DF4B005DD25D4C321CF198B0736C303C.2820241216173505; ssa.ticket=BJ.FEE960453803D3C2329F688BE20E7582.6920241216173505S; ssa.origin-api.state=J9QjWCenv0MO-5KqeDNgN0_z4a_N9kBUPyx8khuiuz0; ssa.origin-gateway=66fd8fd459a60a025a1896a88dc48163c907348c0253eff095083d3d2d611056d3a973551fd5695083cc19ff96ededac3d89a37b57fc95a53907113c6d6d11b5edc6f6fc55343f7d65b418b02cd55e58eaa3a82f8b3039a4f7fdfa6679706d5cc4b36b3d38fa5bc5aef24ae10c7ab108ffb6cc89c5019022ddad687e932cf36d; ssa.oidc.qc=b2lkYy5zdGF0ZT1KOVFqV0NlbnYwTU8tNUtxZUROZ04wX3o0YV9OOWtCVVB5eDhraHVpdXowJm9pZGMuY29kZT1YODlDNHpLN3RWNzdfNUJpZkVRNno1eTdadTN1M1BZRUZuaDU1YkVyUG1B; ssa.origin-api=2b16bf126a49e58d7aaf7d6b8a0030b36ce8cf39fd8b9a63b316b1059c43db880b4cc95a44254074c9ffa2d5d3c76125b7ab2c47d51bc36b73796267ded1947b326407dcf7ea31fbf088afafba132e42e7bb3efff77957ad65c8bac90387cc4fc7b2c2af86a8eb0e44dd8384adc5d1cd09e63fd731051aa88580528f81e3359a; ssa.global.ticket=52fa3a68a19b6db59265233a64608ac4e05f12c3c4095e53df4ad762a88972d1; psvSsoRdrt=1734341705398; __jda=230157721.17343417059032134830076.1734341706.1734341706.1734341706.1; __jdb=230157721.1.17343417059032134830076|1.1734341706; __jdc=230157721; __jdv=230157721|direct|-|none|-|1734341705903; __jdu=17343417059032134830076; psverp2=s%3Aliyang1559%3B1734341706.EnjQC6EyNAZbPsbTeWcGNM62ZOAJEtkTLllI9MPkecY; logbook_u=liyang1559"
headers = {
    'Cookie': Cookie_value
}
monitor_types = ["method", "jvm", "url", "port", "custom", "biz", "alive"]
# applications = [
#     {"appName": "api-service-1", "platform": "jdos"},
#     {"appName": "api-service-2", "platform": "jdos"},
#     # 添加更多应用配置
# ]

df = pd.read_excel('D:/easybi/endpoint_count/50/50.xlsx')
# applications = df["app_name"]
applications = ['shopm']
# plats = df['平台']
print(type(applications))
print(len(applications))
# 存储所有应用的结果
all_app_results = {}
totalnum = 0
totalcount_results = []
error_list = []
not_exist = []
for i in range(len(applications)):
    app_results = {}
    for monitor_type in monitor_types:
        totalnum += 1
        print("process is ", totalnum)
        params = {
            'appName': applications[i],
            'platform': 'jdos',
            'strictSwitch': '0',
            'currentPage': 1,
            'pageSize': 20,
            'adminSwitch': '0',
        }
        results = get_paginated_results(base_url, monitor_type, headers, params)
        print(applications[i],monitor_type, results)
        app_results[monitor_type] = results
    all_app_results[applications[i]] = app_results

# # 打印结果
# for app_name, results in all_app_results.items():
#     print(f"Results for {app_name}:")
#     for monitor_type, monitor_results in results.items():
#         print(f"  Monitor type: {monitor_type}")
#         for result in monitor_results:
#             print(f"    {result}")
print(totalnum)
#
with open('D:/easybi/endpoint_count/50/all_app_results_end_new1.json', 'w') as file:
    json.dump(all_app_results, file, indent=4)

# df2 = pd.DataFrame(totalcount_results)
# df2.to_excel('D:/easybi/20241031/normal/totalcount_results.xlsx', index=False)

# df2 = pd.DataFrame(error_list)
# df2.to_excel('D:/Updata_jk_data/result/error/error_list.xlsx', index=False)
#
# df2 = pd.DataFrame(not_exist)
# df2.to_excel('D:/Updata_jk_data/result/no_exist/no_exist_list.xlsx', index=False)


# with open('D:/easybi/endpoint_count/50/all_app_results_end_new1.json','r') as file:
#     data = json.load(file)
# print(len(data))


data = all_app_results
df = pd.read_excel('D:/easybi/endpoint_count/50/50.xlsx')
applications = df["app_name"]
groups = df["group"]
monitor_types = ["method", "jvm", "url", "port", "custom", "biz", "alive"]

all_results = []
num1 = 0
num2 = 0
start_time = "2024-12-06"
end_time = "2024-12-12"


start_timestamp = int(datetime.strptime(start_time, '%Y-%m-%d').timestamp() * 1000)
end_timestamp =   int(datetime.strptime(end_time, '%Y-%m-%d').timestamp() * 1000)
print(end_timestamp)

pattern1 = r'^(pre_|yf_|yc_|pre.|PRE_|monitor_dao|PRE.|Pre.|Pre_|yfb.)'
pattern2 = r"(\.yufa\.|_yf|\.pre$|alpha_|beta)"
for i in range(len(applications)):
    for monitor_type in monitor_types:
        if len(data[applications[i]][monitor_type]) >0:
            for endp in data[applications[i]][monitor_type]:
                if "create_time" in endp and "create_by" in endp:
                    print(i)
                    print(applications[i])
                    print(monitor_type)
                    if endp["create_time"] <= end_timestamp and endp["create_time"]>= start_timestamp and not re.match(pattern1, endp['endPointKey']) and not re.search(pattern2,endp['endPointKey']):
                        second_timestamp = endp['create_time']/1000.0
                        utc_time = datetime.utcfromtimestamp(second_timestamp)
                        utc = pytz.utc
                        utc_time = utc.localize(utc_time)
                        beijing_timezone = pytz.timezone('Asia/Shanghai')
                        beijing_time = utc_time.astimezone(beijing_timezone)
                        formatted_beijing_time = beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                        second_timestamp1 = endp['update_time']/1000.0
                        utc_time1 = datetime.utcfromtimestamp(second_timestamp1)
                        utc1 = pytz.utc
                        utc_time1 = utc.localize(utc_time1)
                        beijing_timezone1 = pytz.timezone('Asia/Shanghai')
                        beijing_time1 = utc_time1.astimezone(beijing_timezone1)
                        formatted_beijing_time1 = beijing_time1.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                        all_results.extend([{'应用名称':applications[i],'监控点':endp['endPointKey'], '所属部门':groups[i] ,'erp_create':endp['create_by'],'erp_update':endp['update_by'],'监控类型':monitor_type,'create_time':formatted_beijing_time,'update_time':formatted_beijing_time1,'开启状态':endp['endPointAlarmSwitch']}])
                        # all_results.extend([{'应用名称':applications[i],'监控点':endp['endPointKey'],'erp_create':endp['create_by'],'erp_update':endp['update_by'],'监控类型':monitor_type,'create_time':formatted_beijing_time,'update_time':formatted_beijing_time1,'开启状态':endp['endPointAlarmSwitch']}])
df = pd.DataFrame(all_results)
# df.to_excel('D:/easybi/endpoint_count/50/all_app_results_new1.xlsx', index=False)
print(all_results)
print(len(all_results))
print('success')