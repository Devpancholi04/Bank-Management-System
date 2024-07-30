import mysql.connector as sqltor
from BANK_otp_gen import otp
from BANK_email import email_send
from BANK_user_account_no_gen import account_no
from datetime import datetime
import time
from BANK_transaction_id_gen import tran_id
from tabulate import tabulate
from BANK_time_frame import time_frame

class user_log:
    def __init__(self):
        self.email_sender = email_send()
        self.account_num = account_no()
        self.tran = tran_id()
        self.time_f = time_frame()
    
    # database connection
    def connect_db(self):
        global mycon, mycursor
        mycon = sqltor.connect(host = "localhost", user = "root", passwd = "DEV19163247", database = "ATM_SIMULATOR")
        mycursor = mycon.cursor()

    # database connection closed
    def close_db(self):
        mycursor.close()
        mycon.close()

    # random Otp generated
    def get_otp(self): 
        generated_otp = otp.otp_generation(self)
        print(f"generated otp : {generated_otp}")
        return generated_otp
    
    # getting current time to store in db whenever needed
    def curr_time(self):
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return current_timestamp
    
    # checking verification is complete by user or not 
    def self_verifaction_check(self, username, email_id):
        try:
            self.connect_db()
            mycursor.execute('select STATUS from USER_INFO where USER_ID = %s;',(username,))
            us_check = mycursor.fetchone()[0]
            if us_check == "PENDING":
                print("Your Email has not been verified yet......")
                ask_ver = input("Do you want to verify it : [Y,N] : ").upper().strip()
                if ask_ver == "Y":
                    print("Verifying......")
                    generated_e_ver_otp = self.get_otp()
                    subject_e_ver = "EMAIL VERIFICATION"
                    message_e_ver = f'''
This email is from ATM Simulator by DEV
your otp for verification {generated_e_ver_otp}
this otp is valid for 2 min only
don't reply to this mail it is system generated mail
'''     
                    send_e_ver_email = self.email_sender.send_email(email_id, subject_e_ver, message_e_ver)
                    if send_e_ver_email == "EMAIL SEND":
                        print("Email Verifiaction mail has been send.....")
                        e_ver_otp = input("enter OTP to verify EMAIL : ").strip()
                        if e_ver_otp == generated_e_ver_otp:
                            mycursor.execute("update user_info set STATUS = 'APPROVED', UPDATED_AT = %s where USER_ID = %s;", (self.curr_time(), username,))
                            mycon.commit()
                            print("Verifing your email... WAIT.....")
                            time.sleep(5)
                            print("your email has been verified.......")
                            print("login again.......\n Exiting.....")
                            print("THANK YOU FOR USING ATM_SIMULATOR BY DEV")
                            return
                        else:
                            print("OTP doesnot match....")
                            print("for security reason..... Exiting....\nlogin again to verify.....")
                            print("THANK YOU FOR USING ATM_SIMULATOR BY DEV")
                            return
                    else:
                        print("something went wrong.... Try Again....")
                        return
                else:
                    print("THANK YOU FOR USING ATM_SIMULATOR BY DEV")
                    print("Exiting.....")
                    time.sleep(5)
                    return
            else:
                return "your self verifiaction is complete \nyou can procced..\n"
            
        except Exception as e:
               print(f"error : {e}")
        finally: 
            self.close_db()

    # create new account 
    def create_account(self,username,name,email_id):
        try:
            while True:
                acc_t = input("choose you account type [S / C] : ").upper().strip()
                if acc_t == "S":
                    acc_t = "SAVING"
                    break
                elif acc_t == "C":
                    acc_t == "CURRENT"
                    break
                else:
                    print("invalid value using correct account type : [S/C] : ")

            balance = float(input("enter the amount to want to deposit : "))

            while True:
                min_balance = float(input("enter the min balance amount : [min 1000] : "))
                if min_balance >= 1000:
                    break
                else:
                    print("minimum balance must be 1000 or greater....")
        
            t_pin = int(input("create your T-pin of 4 digit : "))
            account_no = self.account_num.gen_account()
            
            self.connect_db()



            ins_t = 'insert into transaction_log (transaction_id, account_no, MESSAGE, DEBIT, CREDIT, balance) VALUES (%s,%s,%s,%s,%s,%s);'
            data_t = (self.tran.trn(), account_no, "FIRST DEPOSIT MADE ON ACCOUNT CREAITON",None, balance, balance)
            mycursor.execute(ins_t, data_t)
            mycon.commit()

            ins = 'insert into account (ACCOUNT_NO, USER_ID, ACCOUNT_TYPE, BALANCE, MIN_BALANCE, T_PIN, UPDATED_AT) VALUES (%s,%s,%s,%s,%s,%s,%s);'
            data = (account_no, username, acc_t, balance, min_balance, t_pin, None)
            mycursor.execute(ins, data)
            mycon.commit()
            mycursor.execute("update user_info set account_no = %s where user_id = %s;",(account_no, username))
            mycon.commit()
            self.close_db()

            print("your account has been successfully created.....\n")
            subject_a_c = "BANK ACCOUNT CREATED"
            message_a_c = f'''
Hello, {name}
This email is from ATM Simulator by DEV
Your account has been created successfully
---------------------------------------
YOUR ACCOUNT DETAILS ARE AS FOLLOWED.....
---------------------------------------
USERNAME = {username}
ACCOUNT NO = {account_no}
ACCOUNT TYPE = {acc_t}
DEPOSITED AMOUNT = {balance}
MINIMUM BALANCE = {min_balance}
T-PIN = {t_pin}
---------------------------------------
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
don't share this details with any one and save it for future reference.......
also keep in mind to keep minimum balance in account to avoid unnessary deduction from account.....
T-PIN is important to made every transaction.....
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
---------------------------------------
dont reply to this mail it is system generated mail
'''
            details_send = self.email_sender.send_email(email_id, subject_a_c, message_a_c)
            if details_send == "EMAIL SEND":
                print("details has been send on mail....")
                print("THANK YOU FOR USING ATM_SIMULATOR BY DEV")
                print("login again.....")
                return

        except Exception as e:
            print(f'error : {e}')

    # checking user account exits or not
    def check_account_exits(self, username, name,email_id):
        try:
            self.connect_db()
            mycursor.execute("select ACCOUNT_NO from user_info where user_id = %s;",(username,))
            acc_check = mycursor.fetchone()[0]
            if acc_check == None:
                while True:
                    ask_c_a = input("Do you want to Create Account [Y/N] : ").upper().strip()
                    if ask_c_a == 'Y':
                        print("enter details to create account : ")
                        self.create_account(username,name ,email_id)
                        ins_t = 'insert into '
                    elif ask_c_a == 'N':
                        print("THANK YOU FOR USING ATM_SIMULATOR BY DEV")
                        print("Exiting.....")
                        break
                    else:
                        print("Invalid choice")
            else:
                return "account already exits....."
                        
        except Exception as e:
            print(f"error : {e}")

    # checking balance 
    def check_bal(self, account_no):
        try:
            self.connect_db()
            mycursor.execute("select balance from account where account_no = %s;",(account_no,))
            balance = mycursor.fetchone()[0]
            print("---------------------------------------")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print(f"YOUR BALANCE IS :- {balance}")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("---------------------------------------")
        except Exception as e:
            print(f"check balance error :- {e}")
        finally:
            self.close_db()

    # deposit in account
    def Deposit(self, account_no):
        try:
            self.connect_db()
            mycursor.execute("select balance, T_pin from account where account_no = %s;",(account_no,))
            result = mycursor.fetchone()
            cu_balance = result[0]
            t_pin = result[1]

            ask_deposit_amount = int(input("enter the amount you want to deposit : "))
            check_pin = int(input("enter your pin : "))
            if check_pin == t_pin:
                update_balance = cu_balance + ask_deposit_amount
                mycursor.execute("update account set balance = %s, updated_at = %s where account_no = %s;",(update_balance, self.curr_time(),account_no,))
                mycon.commit()
                print(f"the amount {ask_deposit_amount} has been deposit successfully")
                print("---------------------------------------")
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                mycursor.execute("select balance from account where account_no = %s;",(account_no,))
                bal = mycursor.fetchone()[0]
                print(f"YOUR BALANCE IS :- {bal}")
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                print("---------------------------------------")
                ins_d = "insert into transaction_log (transaction_id, account_no, message, debit, credit, balance) values (%s,%s,%s,%s,%s,%s);"
                data_d = (self.tran.trn(), account_no, "Deposited", None, ask_deposit_amount,bal)
                mycursor.execute(ins_d, data_d)
                mycon.commit() 
                return
            else:
                print("❌❌❌ wrong pin... ❌❌❌")
                return
        except Exception as e:
            print("error while depositing")
            print(e)
        finally:
            self.close_db()

    # withdrawal from account
    def withdraw(self,account_no):
        try:
            self.connect_db()
            mycursor.execute("select balance, T_pin from account where account_no = %s;",(account_no,))
            result = mycursor.fetchone()
            cu_balance = result[0]
            t_pin = result[1]

            ask_withdrawal = int(input("enter the amount you want to withdraw : "))
            check_pin = int(input("enter your pin : "))
            if check_pin == t_pin:
                if cu_balance < ask_withdrawal:
                    print("enter amount is more than the current balance.....")
                    return
                else:
                    update_balance = cu_balance - ask_withdrawal
                    mycursor.execute("update account set balance = %s, updated_at = %s where account_no = %s;",(update_balance,self.curr_time() ,account_no,))
                    mycon.commit()
                    print(f"the amount {ask_withdrawal} has been withdawal successfully")
                    print("---------------------------------------")
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    mycursor.execute("select balance from account where account_no = %s;",(account_no,))
                    bal = mycursor.fetchone()[0]
                    print(f"YOUR BALANCE IS :- {bal}")
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print("---------------------------------------")
                    ins_d = "insert into transaction_log (transaction_id, account_no, message, debit, credit, balance) values (%s,%s,%s,%s,%s,%s);"
                    data_d = (self.tran.trn(), account_no, "withdrawal", ask_withdrawal, None, bal)
                    mycursor.execute(ins_d, data_d)
                    mycon.commit() 
                    return
            else:
                print("❌❌❌ Wrong Pin..... ❌❌❌")

        except Exception as e:
            print("error while withdrawal")
            print(e)
        finally:
            self.close_db()
 
    # transfer to specific account no.
    def transfer(self, account_no):
        try:
            self.connect_db()
            mycursor.execute("select balance, T_pin from account where account_no = %s;",(account_no,))
            result = mycursor.fetchone()
            cu_balance = result[0]
            t_pin = result[1]

            ask_transfer_amount = int(input("enter the amount you want to transfer : "))
            check_pin = int(input("enter your pin : "))
            if check_pin == t_pin:
                if cu_balance > ask_transfer_amount:
                    ask_account_no = int(input("enter account no to which you want to transfer : "))
                    mycursor.execute("select balance from account where account_no = %s;",(ask_account_no,))
                    D_cu_balance = mycursor.fetchone()
                    if not D_cu_balance:
                        print(f"account No {ask_account_no} doesnot exists....")
                        return
                    else:
                        D_cu_balance = D_cu_balance[0]
                        update_balance_W = cu_balance - ask_transfer_amount
                        mycursor.execute("update account set balance = %s, updated_at = %s where account_no = %s;",(update_balance_W,self.curr_time() ,account_no,))
                        mycon.commit()
            
                        update_balance_D = D_cu_balance + ask_transfer_amount
                        mycursor.execute("update account set balance = %s, updated_at = %s where account_no = %s;",(update_balance_D,self.curr_time() ,ask_account_no,))
                        mycon.commit()

                        print(f"the amount {ask_transfer_amount} has been transfered successfully")
                        print("---------------------------------------")
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        mycursor.execute("select balance from account where account_no = %s;",(account_no,))
                        bal = mycursor.fetchone()[0]
                        print(f"YOUR BALANCE IS :- {bal}")
                        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        print("---------------------------------------")

                        transaction_id = self.tran.trn()
                        tran_t = transaction_id + "T"
                        ins_w = 'insert into transaction_log (transaction_id, account_no, message, debit, credit, balance) values (%s,%s,%s,%s,%s,%s);'
                        data_w = (tran_t, account_no, f"Transfered to {ask_account_no}", ask_transfer_amount, None, bal)
                        mycursor.execute(ins_w, data_w)
                        mycon.commit()

                        tran_r = transaction_id + "R"
                        ins_d = 'insert into transaction_log (transaction_id, account_no, message, debit, credit, balance) values (%s,%s,%s,%s,%s,%s);'
                        data_d = (tran_r, ask_account_no, f"transfered by {account_no}", None, ask_transfer_amount, bal)
                        mycursor.execute(ins_d, data_d)
                        mycon.commit()
                else:
                    print("enter amount is more than the current balance....")
            else:
                print("❌❌❌ Wrong Pin..... ❌❌❌")

        except Exception as e:
            print("error while transferring...")
            print(e)
        finally:
            self.close_db()

    # view statement of user based on time like 1 year, 6 months or specific time
    def view_statement(self, account_no):
        try:
            self.connect_db()
            mycursor.execute("select t_pin from account where account_no = %s;", (account_no,))
            t_pin = mycursor.fetchone()[0]

            check_pin = int(input("enter the pins : "))
            if check_pin == t_pin: 
                option = int(input("choice the option \n1. one year \n2. 6 months \n3. between specific date \n4. exit \n: "))
                
                cur_time = self.time_f.cur_time()   
                print(cur_time)
                if option == 1:
                    one_year = self.time_f.one_year()
                    mycursor.execute("SELECT transaction_id, transaction_date as date, message, debit, credit, balance FROM transaction_log where account_no = %s and transaction_date between %s and %s;",(account_no, one_year, cur_time,))
                    data = mycursor.fetchall()
                elif option == 2:
                    six_mon = self.time_f.six_mon()
                    mycursor.execute("SELECT transaction_id, transaction_date as date, message, debit, credit, balance FROM transaction_log where account_no = %s and transaction_date between %s and %s;",(account_no, six_mon, cur_time,))
                    data = mycursor.fetchall()
                elif option == 3:
                    start_date = input("enter start date in [YYYY-MM-DD] format : ")
                    start_date = start_date + " 00:00:00"
                    end_date = input("enter end date in [YYYY-MM-DD] format : ")
                    end_date = end_date + " 23:59:59"
                    mycursor.execute("SELECT transaction_id, transaction_date as date, message, debit, credit, balance FROM transaction_log where account_no = %s and transaction_date between %s and %s;",(account_no, start_date, end_date,))
                    data = mycursor.fetchall()
                elif option == 4:
                    print("exiting...")
                    time.sleep(2)
                    return
                else:
                    print("invalid option.....")

                print("getting your statement wait........\n")
                time.sleep(5)
                cloumns_name = [i[0] for i in mycursor.description]
                
                formatted_data = [
    [row[0], row[1].strftime('%Y-%m-%d %H:%M:%S'), row[2], 
     f'{row[3]:,.2f}' if row[3] is not None else 'N/A', 
     f'{row[4]:,.2f}' if row[4] is not None else 'N/A', 
     f'{row[5]:,.2f}' if row[5] is not None else 'N/A'] 
    for row in data
]

                print("\t\t\tyour Bank statement is :-")
                print(tabulate(formatted_data, headers = cloumns_name, tablefmt = "fancy_grid"))
                print()
                time.sleep(5)
                
        except Exception as e:
            print(e)
                
        finally:
            self.close_db()

    # changing transaction pin using otp
    def change_tpin(self,account_no, email_id):
        try:
            self.connect_db()
            generated_otp = self.get_otp()
            subject_t = "reset pin verification"
            message_t = f'''
Hello sir,
This email is from ATM Simulator by DEV
your otp for Pins change verification is {generated_otp}
this otp is valid for 2 min only
Don't share OTP with any one...
don't reply to this mail it is system generated mail
'''
            email = self.email_sender.send_email(email_id, subject_t, message_t)
            if email == "EMAIL SEND":
                print("OTP has been send....")
                verify_otp = input("enter the otp which you received on email : ").strip()

                if generated_otp == verify_otp:
                    c_pin = int(input("create new pins : "))
                    v_c_pin = int(input("re-enter new pins : "))

                    if v_c_pin == c_pin:
                        mycursor.execute("update account set T_PIN = %s, UPDATED_AT = %s where account_no = %s;",(c_pin,self.curr_time(), account_no,))
                        mycon.commit()
                        print("pin has been change successfully")
                    else:
                        print("❌❌❌ PIN doesnot matched.... ❌❌❌")
                        return
                else:
                    print("❌❌❌ Invaild OTP ❌❌❌")
                    return
            else:
                print("email doesnot send\n❌❌❌ Something went Wrong ❌❌❌\nTry Again")
                return
        except Exception as e:
            print(f"pins change error : {e}")
        
        finally:
            self.close_db()

    # changing password using t-pin or otp
    def change_pass(self, account_no, email_id):
        try:
            self.connect_db()
            option = int(input("enter \n1. Change using T-PIN\n2. Change using OTP verification \n3. Exit \n : "))

            if option == 1:
                mycursor.execute("select T_PIN from account where account_no = %s;",(account_no,))
                t_pin = mycursor.fetchone()[0]

                ask_t_pin = int(input("enter your t_pin : "))
                if ask_t_pin == t_pin:
                    new_password = input("enter new password : ").strip()
                    c_new_password = input("confirm new password : ").strip()

                    if c_new_password == new_password:
                        mycursor.execute("update user_info set password = %s, updated_at = %s where account_no = %s;",(new_password, self.curr_time(), account_no,))
                        mycon.commit()
                        print("password has been changed successfully.....")
                        return
                    else:
                        print("❌❌❌ Password doesnot matched... ❌❌❌")
                        return
                else:
                    print("❌❌❌ Invalid T-PIN ❌❌❌")
                    return
            
            elif option == 2:
                generated_otp = self.get_otp()
                subject_t = "CHANGE PASSWORD VERIFICATION"
                message_t = f''' 
Hello sir,
This email is from ATM Simulator by DEV
your otp for Password change verification is {generated_otp}
this otp is valid for 2 min only
Don't share OTP with any one...
don't reply to this mail it is system generated mail
'''
                email = self.email_sender.send_email(email_id, subject_t, message_t)
                if email == "EMAIL SEND":
                    print("Email has been send successfully....")
                    print("check your mail")

                    verify_otp = input("enter the otp which you received on email : ").strip()

                    if verify_otp == generated_otp:
                        new_password = input("enter new password : ").strip()
                        c_new_password = input("confirm new password : ").strip()
                        if c_new_password == new_password:
                            mycursor.execute("update user_info set password = %s, updated_at = %s where user_email_id = %s;",(new_password, self.curr_time(), email_id,))
                            mycon.commit()
                            print("password has been changed successfully.....")
                            return
                        else:
                            print("❌❌❌ Password doesnot matched... ❌❌❌")
                            return
                        
                    else:
                        print("❌❌❌ Invalid OTP ❌❌❌")
                        return
                else:
                    print("send email failed....")
                    print("❌❌❌ Something went wrong ❌❌❌\nTry again....")
                    return
            elif option == 3:
                print("exiting....")
                time.sleep(5)
                return
            else:
                print("invalid Input")
                    
        except Exception as e:
            print(f"error while changing password : {e}")
        
        finally:
            self.close_db()

    # various operation for users
    def option(self, email_id):
        try:
            self.connect_db()
            mycursor.execute("select account_no from user_info where user_email_id = %s;",(email_id,))
            acc_num = mycursor.fetchone()[0]
            self.close_db()
            while True:
                choice = int(input('''choice operations : 
1. Check Balance                           
2. Deposit : 
3. Withdrawal
4. transfer with account No.
5. View statement
6. Change T-Pin
7. Change Password
8. Exit                                    
: '''))
                if choice == 1:
                    self.check_bal(acc_num)

                elif choice == 2:
                    self.Deposit(acc_num)

                elif choice == 3:
                    self.withdraw(acc_num)

                elif choice == 4:
                    self.transfer(acc_num)

                elif choice == 5:
                    self.view_statement(acc_num)

                elif choice == 6:
                    self.change_tpin(acc_num, email_id)

                elif choice == 7:
                    self.change_pass(acc_num, email_id)

                elif choice == 8:
                    break

                else:
                    print("❌❌❌ Invalid Choice ❌❌❌")

        except Exception as e:
            print(f'error : {e}')

        finally:
            self.close_db()

    # main function
    def main(self):
        try:
            username = input("enter your username : ")
            password = input("enter your password : ")
            re_password = input("confirm your password : ")

            if re_password == password:
                self.connect_db()
                mycursor.execute('select user_fullname, user_email_id, password from user_info where user_id = %s;',(username,))
                fetch = mycursor.fetchone()
                name = fetch[0]
                email_id = fetch[1]
                db_password = fetch[2]
                self.close_db()
                if db_password == password:
                    generated_otp = self.get_otp()
                    subject_l_v = "Login verification"
                    message_l_v = f'''
Hello {name},
This email is from ATM Simulator by DEV
your otp for Login verification is {generated_otp}
this otp is valid for 2 min only
Don't share OTP with any one...
don't reply to this mail it is system generated mail
'''
                    email = self.email_sender.send_email(email_id, subject_l_v, message_l_v)
                    if email == "EMAIL SEND":
                        print("Check email...")
                        verify_otp = input("enter the OTP : ")
                        if verify_otp == generated_otp:
                            print("Login Success....")
                            self_check = self.self_verifaction_check(username, email_id)
                            if self_check is None:
                                return
                            else:
                                print(self_check)
                    
                            check_account = self.check_account_exits(username, name,email_id)
                            if check_account is None:
                                return
                            else:   
                                print(check_account)
                                self.option(email_id)
                        else:
                            print("❌❌❌ Invalid OTP ❌❌❌")
                            return
                    else:
                        print("❌❌❌ Something went Wrong Login Again!!!! ❌❌❌")
                else:
                    print("❌❌❌ Wrong password ❌❌❌")
            else:
                print("❌❌❌ Password Doesnot matched ❌❌❌")


        except Exception as e:
            print(f'error in main: {e}')


if __name__ == "__main__":
    lo = user_log()
    lo.main()
    