import re
import pandas as pd

date_list = []
time_list = []
interface_list = []
macaddress_list = []
protcol_list = []
ipaddress_list = []
len_list = []

i = 0

with open('test.txt', mode='rt', encoding='utf-8') as f:
    for line in f:
        l = line.split()

        date_list.append(l[0])
        time_list.append(l[1])
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
    '日付': date_list,
    '時間': time_list,
    'I/F': interface_list,
    'mac addres': macaddress_list,
    'protcol': protcol_list,
    '通信IP': ipaddress_list,
    'len': len_list
}

df = pd.DataFrame(csv_dict,columns=['日付','時間','I/F','mac addres','protcol','通信IP','len'])


pd.set_option('display.max_rows', 5)
print(df)

print(type(df))

#.to_csv('./test.csv')