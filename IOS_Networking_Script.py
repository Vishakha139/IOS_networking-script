#!/usr/bin/python

#####################################################################
# XLSX coulumn masking script
# Vishakha
# Date Modified 03/05/2018
# Python 3.6.4
# Install pandas
######################################################################

## importing libraries
from paramiko import client
import sys
import time
import pandas as pd
import time
import os.path

##Main function
def main():
    f = open('IP_Core.txt')
    server_list = f.readlines()
    g = open('IP_Nexus.txt')
    server_list1 = g.readlines()
    h = open('IP_Access.txt')
    server_list2 = h.readlines()
    write_df=pd.DataFrame(columns=['Device','CPU','Clock'])
    write_df1=pd.DataFrame(columns=['Device','Free Memory','Used Memory'])
    write_df2=pd.DataFrame(columns=['Device','Number of existing VLANs','Number of existing VTP VLANs','Number of existing extendedVLANs'])
    write_df3=pd.DataFrame(columns=['Device','Number of BGP Neighbors'])
    write_df4=pd.DataFrame(columns=['Device','Number of OSPF Neighbors'])
    write_df5=pd.DataFrame(columns=['Device','Image','Serial number','Uptime'])
    write_df6=pd.DataFrame(columns=['Device','CPU','Clock'])
    write_df7=pd.DataFrame(columns=['Device','CPU','Clock'])
    for HOST in server_list:
        USER = "python"
        PASS = "python"
        client1=SSH(HOST.strip(),USER,PASS)
        client2=client1.invoke_shell()
        cpu_out=CPU(client2)
        mem_free_out,mem_used_out=Memory(client2)
        existVlan,VTPvlan,ExtendedVlan=VLAN(client2)
        clock,device,clock2=Clock(client2)
        Image=HW1(client2)
        Serial=HW2(client2)
        Uptime=HW3(client2)
        ospf=OSPF(client2)
        bgp=BGP(client2)
        client1.close()
        df = pd.DataFrame([[device,cpu_out,clock]], columns=['Device','CPU','Clock'])
        write_df=write_df.append(df)
        df1 = pd.DataFrame([[device,mem_free_out,mem_used_out]], columns=['Device','Free Memory','Used Memory'])
        write_df1=write_df1.append(df1)
        df2 = pd.DataFrame([[device,existVlan,VTPvlan,ExtendedVlan]], columns=['Device','Number of existing VLANs','Number of existing VTP VLANs','Number of existing extendedVLANs'])
        write_df2=write_df2.append(df2)
        df3 = pd.DataFrame([[device,bgp]], columns=['Device','Number of BGP Neighbors'])
        write_df3=write_df3.append(df3)
        df4 = pd.DataFrame([[device,ospf]], columns=['Device','Number of OSPF Neighbors'])
        write_df4=write_df4.append(df4)
        df5 = pd.DataFrame([[device,Image,Serial,Uptime]], columns=['Device','Image','Serial number','Uptime'])
        write_df5=write_df5.append(df5)
    for HOST1 in server_list1:
        USER = "python"
        PASS = "python"
        client1=SSH(HOST1.strip(),USER,PASS)
        client2=client1.invoke_shell()
        cpu_out=CPU(client2)
        clock,device,clock2=Clock(client2)
        client1.close()
        df6 = pd.DataFrame([[device,cpu_out,clock2]], columns=['Device','CPU','Clock'])
        write_df6=write_df6.append(df6)
    for HOST2 in server_list2:
        USER = "python"
        PASS = "python"
        client1=SSH(HOST2.strip(),USER,PASS)
        client2=client1.invoke_shell()
        cpu_out=CPU(client2)
        clock,device,clock2=Clock(client2)
        client1.close()
        df7 = pd.DataFrame([[device,cpu_out,clock2]], columns=['Device','CPU','Clock'])
        write_df7=write_df7.append(df7)
    write_df.insert(0, 'Sr.No', range(1, 1 + len(write_df)))
    write_df1.insert(0, 'Sr.No', range(1, 1 + len(write_df1)))
    write_df2.insert(0, 'Sr.No', range(1, 1 + len(write_df2)))
    write_df3.insert(0, 'Sr.No', range(1, 1 + len(write_df3)))
    write_df4.insert(0, 'Sr.No', range(1, 1 + len(write_df4)))
    write_df5.insert(0, 'Sr.No', range(1, 1 + len(write_df5)))
    write_df6.insert(0, 'Sr.No', range(1, 1 + len(write_df6)))
    write_df7.insert(0, 'Sr.No', range(1, 1 + len(write_df7)))
    TodaysTime = time.strftime("%d-%m-%Y")
    save_path = TodaysTime
    TodaysDate = time.strftime("%H")
    excelfilename = os.path.join(save_path,"Health_"+ TodaysDate +"hours.xlsx")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    writer = pd.ExcelWriter(excelfilename)
    write_df.to_excel(writer,'CPU',index=False)
    write_df6.to_excel(writer,'CPU_Nexus',index=False)
    write_df7.to_excel(writer,'CPU_Access',index=False)
    write_df1.to_excel(writer,'Memory',index=False)
    write_df2.to_excel(writer,'VLAN',index=False)
    write_df3.to_excel(writer,'BGP',index=False)
    write_df4.to_excel(writer,'OSPF',index=False)
    write_df5.to_excel(writer,'Hardware',index=False)
    workbook  = writer.book
    worksheet = writer.sheets['CPU']
    worksheet1 = writer.sheets['CPU_Nexus']
    worksheet2 = writer.sheets['CPU_Access']
    worksheet3 = writer.sheets['Memory']
    worksheet4 = writer.sheets['VLAN']
    worksheet5 = writer.sheets['BGP']
    worksheet6 = writer.sheets['OSPF']
    worksheet7 = writer.sheets['Hardware']
    header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#D7E4BC',
    'border': 1})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num +1, value, header_format)
    for col_num, value in enumerate(df1.columns.values):
        worksheet1.write(0, col_num +1, value, header_format)
    for col_num, value in enumerate(df2.columns.values):
        worksheet2.write(0, col_num +1, value, header_format)
    for col_num, value in enumerate(df3.columns.values):
        worksheet3.write(0, col_num +1, value, header_format)
    for col_num, value in enumerate(df4.columns.values):
        worksheet4.write(0, col_num +1, value, header_format)
    for col_num, value in enumerate(df5.columns.values):
        worksheet5.write(0, col_num +1, value, header_format)
    for col_num, value in enumerate(df6.columns.values):
        worksheet6.write(0, col_num +1, value, header_format)
    for col_num, value in enumerate(df7.columns.values):
        worksheet7.write(0, col_num +1, value, header_format)
    worksheet.write(0, 0, 'Sr.No', header_format)
    worksheet1.write(0, 0, 'Sr.No', header_format)
    worksheet2.write(0, 0, 'Sr.No', header_format)
    worksheet3.write(0, 0, 'Sr.No', header_format)
    worksheet4.write(0, 0, 'Sr.No', header_format)
    worksheet5.write(0, 0, 'Sr.No', header_format)
    worksheet6.write(0, 0, 'Sr.No', header_format)
    worksheet7.write(0, 0, 'Sr.No', header_format)
    width= len("long text hidden test-1")
    worksheet.set_column(1, 4, width)
    worksheet1.set_column(1, 4, width)
    worksheet2.set_column(1, 4, width)
    worksheet3.set_column(1, 4, width)
    worksheet4.set_column(1, 4, width)
    worksheet5.set_column(1, 4, width)
    worksheet6.set_column(1, 4, width)
    worksheet7.set_column(1, 4, width)
    writer.save()

## SSH Function
def SSH(HOST,USER,PASS):
    try:
        client1=client.SSHClient()
        client1.set_missing_host_key_policy(client.AutoAddPolicy())
        client1.connect(HOST,username=USER,password=PASS,port=22,look_for_keys=False)        
        print ("SSH connection to %s established" %HOST)
    except IOError:
        print("There was an error connecting to host",HOST)
    return client1;
    
## Hardware function
def HW1(client1):
    try:
        #client2 = client1.invoke_shell()
        #output=client2.recv(999)
        print("Image Information")
        time.sleep(2)
        client1.send('show version | include boot\n')
        #while not client1.recv_ready():
            #time.sleep(2)
        output=client1.recv(999)
        time.sleep(2)
        output=client1.recv(999)
        #print (output)
        output=output.decode("utf-8")
        output.strip()
        temp=output.split("\n")
        df=pd.DataFrame(list(map(lambda x : x.split(),temp)))
        #print (df.head())
        image = df.iloc[1][4]
        #client2.close()
        #print("hardware END ")
    except IOError:
        print("Wrong Command for Hardware")
    return image;
    
def HW2(client1):
    #client2 = client1.invoke_shell()
    #output=client2.recv(999)
    print('Start HW2')
    time.sleep(2)
    client1.send('show version | include Processor \n')
    #while not client1.recv_ready():
        #time.sleep(2)
    output=client1.recv(999)
    time.sleep(2)
    output=client1.recv(999)
    output=output.decode("utf-8")
    output.strip()
    temp=output.split("\n")
    df=pd.DataFrame(list(map(lambda x : x.split(),temp)))
    serial = df.iloc[1][3]
    #client2.close() 
    print('END HW2')
    return serial;

def HW3(client1):
    #client2 = client1.invoke_shell()
    #output=client2.recv(999)
    print('Start HW3')
    time.sleep(2)
    client1.send('show version | include uptime \n')
    #while not client1.recv_ready():
        #time.sleep(2)
    output=client1.recv(999)
    time.sleep(2)
    output=client1.recv(999)
    output=output.decode("utf-8")
    output.strip()
    temp=output.split("\n")
    df=pd.DataFrame(list(map(lambda x : x.split(),temp)))
    uptime = df.iloc[1][3],"years",df.iloc[1][5],"weeks",df.iloc[1][7],"hours",df.iloc[1][9],"minutes"
    #client2.close() 
    print('Start HW3')
    return uptime;
    
## CPU function
def CPU(client1):
    try:
        #client2 = client1.invoke_shell()
        #output=client2.recv(999)
        print("start CPU")
        time.sleep(2)
        client1.send('show processes cpu | include CPU\n')
        while not client1.recv_ready():
            time.sleep(2)
        output=client1.recv(999)
        time.sleep(2)
        output=client1.recv(999)
        output=output.decode("utf-8")
        output.strip()
        temp=output.split("\n")
        df=pd.DataFrame(list(map(lambda x : x.split(),temp)))
        print(df.head())
        CPU1 = df.iloc[1][8].replace(";","")
        print('END CPU')
        #client2.close() 
    except IOError:
        print("Wrong Command for CPU")
    return CPU1;

## Clock Function
def Clock(client1):
    try:
        #client2 = client1.invoke_shell()
        #output=client2.recv(999)
        print("start clock")
        time.sleep(2)
        client1.send('show clock\n\n')
        #while not client1.recv_ready():
            #time.sleep(2)
        output=client1.recv(999)
        time.sleep(2)
        output=client1.recv(999)
        output=output.decode("utf-8")
        output.strip()
        temp=output.split("\n")
        df=pd.DataFrame(list(map(lambda x : x.split(),temp)))
        #print(df.head())#print(df.head())
        clk = df.iloc[1][0]
        clk2 = df.iloc[0][0]
        print(clk2)
        hst = df.iloc[2][0].replace("#","")
        #client2.close()
        print('END CLock')
    except IOError:
        print("Wrong Command for Clock")
        #while not client1.recv_ready():
            #time.sleep(2)  
    return clk,hst,clk2;

## VLAN function
def VLAN(client1):
    try:
        #client2 = client1.invoke_shell()
        #output=client2.recv(999)
        print("start VLAN")
        time.sleep(2)
        client1.send('show vlan summary\n')
        #while not client1.recv_ready():
            #time.sleep(2)
            #print("..")
        output=client1.recv(999)
        time.sleep(2)
        output=client1.recv(999)
        #print (output)
        output=output.decode("utf-8")
        output.strip()
        temp=output.split("\n")
        df=pd.DataFrame(list(map(lambda x : x.split(),temp)))
        #print (df.head())
        eVlan = df.iloc[1][5]
        VTPvlan = df.iloc[2][6]
        ExVlan = df.iloc[3][6]
        #client2.close()
        print('END VLAN')
    except IOError:
        print("Wrong Command for VLAN")
    return eVlan,VTPvlan,ExVlan;
    
## Memory function
def Memory(client1):
    try:
        #client2 = client1.invoke_shell()
        #output=client2.recv(999)
        print("end memory")
        #time.sleep(2)
        client1.send('show processes memory sorted | include Processor\n')
       # while not client1.recv_ready():
            #print("..")
        output=client1.recv(999)
        time.sleep(5)
        output=client1.recv(999)
        print(output)
        output=output.decode("utf-8")
        output.strip()
        temp=output.split("\r\n")
        #print (temp)
        df=pd.DataFrame(list(map(lambda x : x.split(),temp)))
        print (df.head())
        FreeMem = df.iloc[1][7]
        UsedMem = df.iloc[1][5]
        #client2.close()   
        print('END Memmory')
    except IOError:
        print("Wrong Command for Memory")
    return FreeMem,UsedMem;
    
## BGP function
def BGP(client1):
    try:
        #client2 = client1.invoke_shell()
        #output=client2.recv(999)
        print("BGP")
        time.sleep(2)
        client1.send('show ip bgp summary\n')
        #while not client1.recv_ready():
            #time.sleep(2)
        output=client1.recv(9999)
        time.sleep(10)
        output=client1.recv(9999)
        output=output.decode("utf-8")
        output.strip()
        #print(output)
        #print(output.split("\n\n")[0].split("\n")
        #print("#########")
        #print(output.split("\n\n"))
        #print("#########")
        temp=len(output.split("\n\r\n")[1].split('\n'))-2
        #print(temp)
        #client2.close()
        print('END BGP')
    except IOError:
        print("Wrong Command for BGP")
    return temp;
    
## OSPF function
def OSPF(client1):
    try:
        #client2 = client1.invoke_shell()
        #output=client2.recv(999)
        print("start ospf")
        time.sleep(2)
        client1.send('show ip ospf neighbor\n')
        #while not client1.recv_ready():
            #time.sleep(2)
        output=client1.recv(9999)
        time.sleep(5)
        output=client1.recv(9999)
        output=output.decode("utf-8")
        output=output.strip()
        #print(output)
        temp=output.split('\n')
        #print(temp)
        temp1=len(temp)-4
        #print(temp1)
        #client2.close()
        print('END OSPF')
    except IOError:
        print("Wrong Command for OSPF")
    return temp1;  

## calling main function      
if __name__== "__main__":
    main()

