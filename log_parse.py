import glob
import re
import os
import re
import pandas as pd
from datetime import datetime, date, timedelta

date_list = []
interface_list = []
macaddress_list = []
protcol_list = []
ip = []
src_ip_list = []
src_port_list = []
dst_ip_list = []
dst_port_list = []
len_list = []

for filename in glob.glob("test_dir/*"):
    with open(os.path.join(os.getcwd(), filename), mode='rt', encoding='utf-8') as f:
        for line in f:
            l = line.split()
            if len(l) == 15 and l[10] == "TCP" and l[4] == 'forward:':
                #Nov/27/2021 14:41:46 → 2021/11/27 14:41:46 の形へ
                date_list.append(datetime.strptime(str(l[0]+" "+l[1]), '%b/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
                interface_list.append((l[6].lstrip('out:')).rstrip(','))
                macaddress_list.append(l[8].rstrip(','))
                protcol_list.append(l[10].rstrip(','))
                ip = re.split('[->,:]',l[12])
                src_ip_list.append(ip[0])
                src_port_list.append(ip[1])
                dst_ip_list.append(ip[3])
                dst_port_list.append(ip[4])
                len_list.append(l[14])


log_dict = {
    'timestamp': date_list,
    'I/F': interface_list,
    'macaddres': macaddress_list,
    'protcol': protcol_list,
    'src_ip': src_ip_list,
    'src_port': src_port_list,
    'dst_ip': dst_ip_list,
    'dst_port': dst_port_list,
    'len': len_list
}

df = pd.DataFrame(log_dict,columns=['timestamp','I/F','macaddres','protcol','src_ip','src_port','dst_ip','dst_port','len'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.drop_duplicates()
df = df.set_index('timestamp')

yesterday = datetime.strftime(datetime.today() - timedelta(days=1), '%Y-%m-%d')

dfa = df.sort_index().loc[yesterday:yesterday]

print("----------------------------------------")
print(dfa.value_counts("protcol"))
print("----------------------------------------")
print(dfa.value_counts("I/F"))
print("----------------------------------------")
print(dfa.value_counts("dst_port").head(30))
print("----------------------------------------")
print(dfa.value_counts("macaddres").head(30))

access = []
access_dt = []
f = 0
while f < 24:
    yesterday_time = datetime.strftime(datetime.today() - timedelta(days=1), '%Y-%m-%d 00:00:00')
    yesterday_59time = datetime.strftime(datetime.today() - timedelta(days=1), '%Y-%m-%d 00:59:59')
    yesterday_hour = datetime.strptime(yesterday_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=+f)
    
    access_dt.append(yesterday_hour.strftime('%H:%M:%S'))
    f += 1
    yesterday_1hour = datetime.strptime(yesterday_59time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=+f)
    
    df_time = dfa.sort_index().loc[yesterday_hour:yesterday_1hour]
    print("****************************************")
    print(yesterday_hour)
    print("----------------------------------------")
    print(df_time.value_counts("protcol"))
    print("----------------------------------------")
    print(df_time.value_counts("I/F"))
    print("----------------------------------------")
    print(df_time.value_counts("dst_port").head(5))
    print("----------------------------------------")
    print(df_time.value_counts("macaddres").head(5))
    
    
    access.append(df_time['protcol'].count())

print("----------------------------------------")
log_dict_2 = {
    'time': access_dt,
    'access': access,
}


import matplotlib.pyplot as plt

df2 = pd.DataFrame(log_dict_2,columns=['time','access'])

df2.plot(x="time", y="access", kind="bar")
plt.show()