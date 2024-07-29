# Banking Project 1.0
import colorama
import datetime as datetime
import random as random
import mysql.connector
import os
from colorama import Fore, Style

colorama.init(autoreset=True)


def attain_server_pass():
    global server_pass
    server_pass = input("Please enter mysql server pass :")
    cls()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def establish_database():
    global server_pass
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=f"{server_pass}",

    )

    sql_select_query = "create database if not exists RCCBankinng;" \
                       "use RCCBanking;" \
                       "create table userData( name varchar(100),age varchar(100),address varchar(100),phone_no " \
                       "varchar(100),account_password varchar(100),account_number varchar(100) ,registration_date " \
                       "varchar(100), account_bal varchar(100)); "
    cursor = mydb.cursor()
    cursor.execute(sql_select_query, multi=True)


def homeScreen():
    print("Home Screen")


def saveToDataBase(name, age, address,
                   phone_no, account_password, account_number,
                   registration_date):
    global server_pass
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=f"{server_pass}",
        database="RCCBankinng",
    )

    print(f"{Fore.GREEN}{Style.BRIGHT}=================================")
    print(f"{Fore.GREEN}{Style.BRIGHT}Name:{name}")
    print(f"{Fore.GREEN}{Style.BRIGHT}age:{age}")
    print(f"{Fore.GREEN}{Style.BRIGHT}address:{address}")
    print(f"{Fore.GREEN}{Style.BRIGHT}phone_no:{phone_no}")
    print(f"{Fore.GREEN}{Style.BRIGHT}account_password:{account_password}")
    print(f"{Fore.GREEN}{Style.BRIGHT}account_number:{account_number}")
    print(f"{Fore.GREEN}{Style.BRIGHT}registration_date:{registration_date}")
    print(f"{Fore.GREEN}{Style.BRIGHT}=================================")

    # SAVE DATA TO SQL
    myCursor = mydb.cursor()
    sql = f"INSERT INTO userData (name, age, address, phone_no, " \
          "account_password, account_number, registration_date, account_bal) " \
          f"VALUES ('{name}', {age}, '{address}', {phone_no}," \
          f"'{account_password}', {account_number}, '{registration_date}', 0 )"
    myCursor.execute(sql)
    mydb.commit()


def createUniqueAccountNo():
    now = datetime.datetime.now()
    part1 = now.strftime("%Y%m%d%H%M%S")
    a = now.strftime("%d:%m:%Y")
    part2 = str(random.randint(111, 999))
    account_number = part1 + part2
    print(f"{Fore.RED}{Style.BRIGHT}your new account number is :", account_number)
    return account_number, a


def input_warning():
    a = input("correctly input data, press 1 to retry or anything else to exit:")
    if a == "1":
        cls()
        registerNewUser()
    else:
        exit()


def registerNewUser():
    print("Register New User - Input Your Information")
    First_name = input("First Name[give no space] : ").strip()

    if First_name.isalpha() is False:
        input_warning()
    else:
        pass

    Last_name = input("Last Name[give no space] : ").strip()

    if Last_name.isalpha() is False:
        input_warning()
    else:
        pass

    name = First_name + " " + Last_name

    age = input("Age[minimum 18] : ").strip()
    if (age.isdigit() is True) and (18 <= int(age)) and (int(age) <= 120):
        pass
    else:
        input_warning()

    address = input("Address : ").strip()
    phone_no = input("Phone No[10 digits] : ").strip()
    if (phone_no.isdigit() is True) and (len(phone_no) == 10):
        pass
    else:
        input_warning()
    if phone_no in get_phone():
        print("Already user registered on this number")
        input_warning()
    else:
        pass
    account_password = input("Password : ").strip()
    account_number, registration_date = createUniqueAccountNo()
    saveToDataBase(name, age, address,
                   phone_no, account_password, account_number,
                   registration_date)
    x = input("Hey!Your account was successfully saved, press 1 to go to homepage or anything else to exit:")
    if x == "1":
        cls()
        start_Program()
    else:
        exit()


def user_authentication():
    global user_chk
    global server_pass
    user_chk = int(input("Enter account number:"))
    # print(user_chk)
    connection = mysql.connector.connect(host='localhost',
                                         database='RCCBankinng',
                                         user='root',
                                         password=f'{server_pass}')

    sql_select_query = f"select account_password from userData where account_number = {user_chk}"
    cursor = connection.cursor()
    cursor.execute(sql_select_query)
    # get all records
    records = cursor.fetchall()

    ck = records[0]
    chk = ck[0]

    user_pass = input("Enter account password :")

    if chk == user_pass:
        signIn()
    else:
        print("wrong id or pass")
        user_authentication()
    return user_chk


def get_account_no():
    global user_chk
    global server_pass
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=f"{server_pass}",
        database="RCCBankinng",
    )
    phone = input("Enter phone no. registered to account: ")
    sql_select_query = f"select account_number from userData where phone_no = {phone} "
    cursor = mydb.cursor()
    cursor.execute(sql_select_query)
    y = cursor.fetchall()
    print(y[0][0])


def get_phone():
    global user_chk
    global server_pass
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=f"{server_pass}",
        database="RCCBankinng",
    )
    sql_select_query = f"select phone_no from userData; "
    cursor = mydb.cursor()
    cursor.execute(sql_select_query)
    y = cursor.fetchall()
    phone_nos = []
    for i in y:
        for j in i:
            phone_nos.append(j)
    return phone_nos


def modify_acc():
    global user_chk
    global server_pass
    print('''Modify your account:-
please renter your details: ''')

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=f"{server_pass}",
        database="RCCBankinng",
    )
    name = input("Name : ")
    age = input("Age : ")
    address = input("Address : ")
    phone_no = input("Phone No : ")
    sql_select_query = f"update userdata set name = '{name}', age = '{age}', address = '{address}', " \
                       f"phone_no = '{phone_no}'" \
                       f"where account_number = {user_chk}; "
    cursor = mydb.cursor()
    cursor.execute(sql_select_query)
    mydb.commit()


def withdraw_money():
    global user_chk
    global server_pass
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=f"{server_pass}",
        database="RCCBankinng",
    )
    sql_select_query = f"select account_bal from userData where account_number = {user_chk} "
    cursor = mydb.cursor()
    cursor.execute(sql_select_query)
    y = cursor.fetchall()
    x = y[0]
    balance = int(x[0])
    print("current balance:", balance)

    get = int(input("Enter value to be withdrawn:"))
    total = balance - get

    if total >= 0:

        sql_select_query2 = f"update userData set account_bal = {total} where account_number = {user_chk}"
        cursor.execute(sql_select_query2)
        mydb.commit()
    else:
        print("Not enough balance")


def deposit_money():
    global user_chk
    global server_pass
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=f"{server_pass}",
        database="RCCBankinng",
    )
    sql_select_query = f"select account_bal from userData where account_number = {user_chk} "
    cursor = mydb.cursor()
    cursor.execute(sql_select_query)
    y = cursor.fetchall()
    x = y[0]
    balance = int(x[0])
    print("current balance:", balance)
    add = int(input("Enter value to be added:"))
    total = balance + add
    sql_select_query2 = f"update userData set account_bal = {total} where account_number = {user_chk}"
    cursor.execute(sql_select_query2)
    mydb.commit()


def delete_account():
    global user_chk
    global server_pass
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=f"{server_pass}",
        database="RCCBankinng",
    )
    sql_select_query = f"delete from userData where account_number = {user_chk} "
    cursor = mydb.cursor()
    cursor.execute(sql_select_query)
    mydb.commit()
    x = input("Your account has been successfully closed, press enter to leave")
    x.strip()
    exit()


def chk_acc_bal():
    global user_chk
    global server_pass
    # print(user_chk)
    connection = mysql.connector.connect(host='localhost',
                                         database='RCCBankinng',
                                         user='root',
                                         password=f'{server_pass}')

    sql_select_query = f"select account_bal  from userData where account_number = {user_chk}"
    cursor = connection.cursor()
    cursor.execute(sql_select_query)
    # get all records
    records = cursor.fetchall()

    for row in records:
        print("account balance= ", row[0])


def check_user_detail():
    global user_chk
    global server_pass
    connection = mysql.connector.connect(host='localhost',
                                         database='RCCBankinng',
                                         user='root',
                                         password=f'{server_pass}')

    sql_select_query = f"select name, age, address, phone_no, account_number, registration_date  from userData where " \
                       f"account_number = {user_chk} "
    cursor = connection.cursor()
    cursor.execute(sql_select_query)
    # get all records
    records = cursor.fetchall()

    for row in records:
        print("Name = ", row[0])
        print("age = ", row[1])
        print("address  = ", row[2])
        print("phone_no  = ", row[3])
        print("account_number  = ", row[4])
        print("registration_date  = ", row[5])


def signIn():
    print("SignedIn")
    print(f'''
     {Fore.YELLOW}{Style.BRIGHT}Options--> 
    {Fore.YELLOW}{Style.BRIGHT}Press 1.Check user details 
    {Fore.YELLOW}{Style.BRIGHT}Press 2.Check account balance
    {Fore.YELLOW}{Style.BRIGHT}Press 3.Deposit money
    {Fore.YELLOW}{Style.BRIGHT}Press 4.Withdraw money 
    {Fore.YELLOW}{Style.BRIGHT}Press 5.Close account 
    {Fore.YELLOW}{Style.BRIGHT}Press 6.Modify account
    {Fore.YELLOW}{Style.BRIGHT}Press 7.Exit 
          '''
          )
    option = input("Enter your choice:").strip()
    if option == "1":
        check_user_detail()
    elif option == "2":
        chk_acc_bal()
    elif option == "3":
        deposit_money()
    elif option == "4":
        withdraw_money()
    elif option == "5":
        delete_account()
    elif option == "6":
        modify_acc()
    elif option == "7":
        exit()
    else:
        print("Wrong Input")
        cls()
        signIn()


def start_Program():
    print(f"{Fore.YELLOW}{Style.BRIGHT}~~~~~~~~~~~~~~~~~BANK OF TECHNO INDIA~~~~~~~~~~~~~~~~~~")
    print(f"{Fore.CYAN}{Style.BRIGHT}              Press 1 : For New Registration")
    print(f"{Fore.CYAN}{Style.BRIGHT}              Press 2 : For SignIn / LogIn")
    print(f"{Fore.CYAN}{Style.BRIGHT}              Press 3 : For knowing your account number")
    ch = input('''


Enter Your Choice [1 or 2 or 3 ] :''')
    if ch == "1":
        registerNewUser()
    elif ch == "2":
        global user_chk

        # print(user_chk)
        user_authentication()
    elif ch == "3":
        get_account_no()
        exit_program()
    else:
        print(" WRONG INPUT ")
        a = input("press 1 to retry or any other button to exit: ")
        if a == "1":
            cls()
            start_Program()
        else:
            exit()


def exit_program():
    x = input("Process completed~~~Press 1 to continue to sign in page or To exit please press any other key:").strip()
    if x == "1":
        cls()
        signIn()
    else:
        exit()


user_chk = 0
server_pass = 0
attain_server_pass()
establish_database()
start_Program()
while True:
    exit_program()
