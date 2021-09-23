from getpass import getpass
import re


def get_file():
    inputfile = input("Inputfile path: ")
    try:
        if not os.path.exists(inputfile):
            print("Path doesn't exist ")
            return get_file()
        return inputfile
    except TypeError:
        print("Path must be valid ")
        return get_file

def get_host():
    host = input("Host IP: ") 
    try:
        if not re.match(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}",host):
            print("Must be valid IP address\n")
            return get_host()
        return host
    except





host = input("Host IP: ") 
port = input("SSH port number: ")
username = input("Admin username: ")
password = getpass() 
address_group_name = input("Address group name: ")
x=0
while x=0:
    login_disclaimer = input("Login disclaimer? 1 for yes, 0 for no: ")
    if login_disclaimer