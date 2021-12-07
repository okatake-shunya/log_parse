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

i = 0

with open('test.txt', mode='rt', encoding='utf-8') as f:
    for line in f:
        l = line.split()
        #Nov/27/2021 14:41:46 → 2021/11/27 14:41:46 の形へ
        date_list.append(datetime.strptime(str(l[0]+" "+l[1]), '%b/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
        interface_list.append((l[6].lstrip('out:')).rstrip(','))
        macaddress_list.append(l[8].rstrip(','))
        protcol_list.append(l[10].rstrip(','))

        if protcol_list[i] == "TCP":
            ip = re.split('[->,:]',l[12])
            src_ip_list.append(ip[0])
            src_port_list.append(ip[1])
            dst_ip_list.append(ip[3])
            dst_port_list.append(ip[4])
            len_list.append(l[14])
        else:
            ip = re.split('[->,:]',l[11])
            src_ip_list.append(ip[0])
            src_port_list.append(ip[1])
            dst_ip_list.append(ip[3])
            dst_port_list.append(ip[4])
            len_list.append(l[13])
        
        i+=1


csv_dict = {
    'timestamp': date_list,
    'I/F': interface_list,
    'mac addres': macaddress_list,
    'protcol': protcol_list,
    'src_ip': src_ip_list,
    'src_port': src_port_list,
    'dst_ip': dst_ip_list,
    'dst_port': dst_port_list,
    'len': len_list
}

df = pd.DataFrame(csv_dict,columns=['timestamp','I/F','mac addres','protcol','src_ip','src_port','dst_ip','dst_port','len'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.drop_duplicates()
df = df.set_index('timestamp')