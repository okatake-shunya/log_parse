import glob
import re
import os
import re
import pandas as pd
from datetime import datetime, date, timedelta

date_list = []
in_list = []
out_list = []
ip_list = []
len_list = []

for filename in glob.glob("fujisoft_ccr/*"):
    with open(os.path.join(os.getcwd(), filename), mode='rt', encoding='utf-8') as f:
        for line in f:
            l = line.split()
            if l[4] == "UNREACH:"  and l[11] == "3," and l[13] == "13)," and str(l[14])[:3] == "14.":
                #Nov/27/2021 14:41:46 → 2021/11/27 14:41:46 の形へ
                date_list.append(datetime.strptime(str(l[0]+" "+l[1]), '%b/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
                in_list.append(l[6].replace('in:', ''))
                out_list.append((l[7].replace('out:ipipv6-', '')).rstrip(','))
                ip_list.append(l[14].rstrip(','))
                len_list.append(l[16])
            
log_dict = {
    'timestamp': date_list,
    'in': in_list,
    'unreach_icmp': out_list,
    'ip': ip_list,
    'len': len_list
}

df = pd.DataFrame(log_dict,columns=['timestamp','in','unreach_icmp','ip','len'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.drop_duplicates()
df = df.set_index('timestamp')

day_ago = datetime.today() - timedelta(days=1)

yesterday = datetime.strftime(day_ago, '%Y-%m-%d')
dfa = df.sort_index().loc[yesterday:yesterday]
print("1日の全体")
print("----------------------------------------")
print(dfa.value_counts("unreach_icmp"))

unreach_icmp = []
access_dt = []
f = 0
while f < 24:
    yesterday_time = datetime.strftime(day_ago, '%Y-%m-%d 00:00:00')
    yesterday_59time = datetime.strftime(day_ago, '%Y-%m-%d 00:59:59')
    yesterday_hour = datetime.strptime(yesterday_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=+f)
    
    access_dt.append(yesterday_hour.strftime('%H:%M:%S'))
    yesterday_1hour = datetime.strptime(yesterday_59time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=+f)
    f += 1    
    
    df_time = dfa.sort_index().loc[yesterday_hour:yesterday_1hour]
    print("****************************************")
    print(yesterday_hour)
    print("----------------------------------------")
    print(df_time.value_counts("unreach_icmp"))

    
    
    unreach_icmp.append(df_time['unreach_icmp'].count())

print("----------------------------------------")
log_dict_2 = {
    'time': access_dt,
    'unreach_icmp': unreach_icmp,
}


import matplotlib.pyplot as plt

df2 = pd.DataFrame(log_dict_2,columns=['time','unreach_icmp'])

df2.plot(x="time", y="unreach_icmp", kind="bar")
plt.show()