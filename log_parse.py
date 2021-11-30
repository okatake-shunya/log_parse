import re
import pandas as pd
import datetime

date_list = []
interface_list = []
macaddress_list = []
protcol_list = []
ipaddress_list = []
len_list = []

i = 0

with open('test.txt', mode='rt', encoding='utf-8') as f:
    for line in f:
        l = line.split()
        #Nov/27/2021 14:41:46 → 2021/11/27 14:41:46 の形へ
        date_list.append(datetime.datetime.strptime(str(l[0]+" "+l[1]), '%b/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
        interface_list.append((l[6].lstrip('out:')).rstrip(','))
        macaddress_list.append(l[8].rstrip(','))
        protcol_list.append(l[10].rstrip(','))

        if protcol_list[i] == "TCP":
            ipaddress_list.append(l[12].rstrip(','))
            len_list.append(l[14])
        else:
            ipaddress_list.append(l[11].rstrip(','))
            len_list.append(l[13])
        
        i+=1


csv_dict = {
    '日時': date_list,
    'I/F': interface_list,
    'mac addres': macaddress_list,
    'protcol': protcol_list,
    '通信': ipaddress_list,
    'len': len_list
}

df = pd.DataFrame(csv_dict,columns=['日時','I/F','mac addres','protcol','通信','len'])


pd.set_option('display.max_rows', 5)
print(df)

print(type(df))

#df.to_csv('./test.csv')