# Import firewall addresses
"""
Created on 2020-11-27

@author: Chrisopher Rose

imports csv file in the format subnet,name into a fortigate configuraiton
"""
import paramiko
import os
import csv
import re

################################input variables################################
inputfile = 'github public ip block.csv'
host = "192.168.100.4"
port = 22
username = "admin"
password = "" 
address_group_name = "github-public-ips"
login_discalimer = 0 #set to 1 if there is a login disclaimer
################################_______________################################

#output file for cli output
outputfile = "Import_firewall_addresses_output.txt"
writefile = open(outputfile,'w')

# Clear terminal screen
os.system('cls')

# Open csv 
with open(inputfile) as f:
    reader = csv.reader(f)
    ip_list = list(reader)

# initialize variables
command =""
ip4_exists = 0
ip6_exists = 0

# Generate Command
"""
this structure below is far from optimized. It currently loops through the csv file four times
this is due to the nature of the fortigate config file
this could be fixed in the future by generating the fortigate command seperately from looping through the csv list
"""



if login_discalimer:
    command += "a\n " #this is needed for logindisclaimers

##add ipv4 addresses to config
command += "config firewall address\n "
for line in ip_list:
    #looping through the ip list to build the command
    #first make sure the line actually has an IP4 address
    if re.match(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}",line[0]):
        line[1] = line[1].lstrip() #strip any leading spaces
        command += "edit " + "\"" + line[1] + "\" \n "
        command += "set subnet " + line[0] + "\n "
        command += "next \n "
        ip4_exists = 1
command += "end\n "

##add ipv6 addresses to config
command += "config firewall address6\n "
for line in ip_list:
    if re.match(r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))",line[0]):
        line[1] = line[1].lstrip() #strip any leading spaces
        command += "edit " + "\"" + line[1] + "\" \n "
        command += "set ip6 " + line[0] + "\n "
        command += "next \n "
        ip6_exists = 1
command += "end\n "

if ip4_exists:
    ##Add ipv4 addresses to group
    command += "config firewall addrgrp\n "
    command += "edit " + "\"" + address_group_name + "\" \n "
    for line in ip_list:
        if  re.match(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}",line[0]):
            line[1] = line[1].lstrip()
            command += "append member " + "\"" + line[1] + "\" \n "
    command += "end\n "

if ip6_exists:
    #add ipv6 to group
    command += "config firewall addrgrp6\n "
    command += "edit " + "\"" + address_group_name + "6\" \n "
    for line in ip_list:
        if re.match(r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))",line[0]):
            line[1] = line[1].lstrip()
            command += "append member " + "\"" + line[1] + "\" \n "
    command += "end\n "


# Setup an SSH session
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

# Execute command
(stdin, stdout, stderr) = ssh.exec_command(command)
stdout=stdout.readlines()
# Print the command output to file
for line in stdout:
    writefile.write("--> "+line)

# Close SSH session
ssh.close()