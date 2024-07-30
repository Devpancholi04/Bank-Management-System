import mysql.connector as sqltor
from BANK_email import email_send
from BANK_otp_gen import otp
import time
from datetime import datetime
from BANK_user_reg import user_reg
from tabulate import tabulate
from BANK_time_frame import time_frame
from BANK_transaction_id_gen import tran_id

class admin_login:
    # creating instance of class from other folder
    def __init__(self):
        self.email_sender = email_send()
        self.new_user = user_reg()
        self.time_f = time_frame()
        self.tran = tran_id()

    # creating connection with db
    def connect_db(self):
        global mycon, mycursor
        mycon = sqltor.connect(host = "localhost", user = "root", passwd = "DEV19163247", database = "ATM_SIMULATOR")
        mycursor = mycon.cursor()

    # closing connection with db
    def close_db(self):
        mycursor.close()
        mycon.close()

    # getting otp from other modules
    def get_otp(self): 
        generated_otp = otp.otp_generation(self)
        print(f"\ngenerated otp : {generated_otp}\n")
        return generated_otp
    
    def curr_time(self):
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return current_timestamp    

    # creating self email verification is compelete or not 
    def admin_verification_check(self, admin_id, email_id):
        try:
            self.connect_db()
            mycursor.execute("select AD_VERIFICATION from admin where AD_USER_ID = %s;",(admin_id,))
            ad_check = mycursor.fetchone()[0]
            if ad_check == "NOT VERIFIED":
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
                            mycursor.execute("update admin set AD_verification = 'VERIFIED', updated_at = %s where AD_USER_ID = %s;",(self.curr_time(),admin_id,))
                            mycon.commit()
                            print("Verifing your email... WAIT.....")
                            time.sleep(5)
                            print("your email has been verified.......")
                            print("login again.......\n Exiting.....")
                            print("THANK YOU FOR USING ATM_SIMULATOR BY DEV")
                            return
                        else:
                            print("otp doesnot match....")
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
    
    # checking manager has verification is compelete or not
    def manager_verification_check(self, admin_id):
        try:
            self.connect_db()
            mycursor.execute("select m_status from admin where AD_USER_ID = %s;",(admin_id,))
            m_check = mycursor.fetchone()[0]

            if m_check == "PENDING":
                print("Your account has not been approved by Manager... \nOnce your account is verified you will recieve email....")
                print("you can't procced..... \nSorry for inconvenience.....")
                print("\nif your account doesnot verified in 24 hours... then,\nemail your user_id, name, contact no. and email_id at atm.simulatorby.dev@gmail.com")
                print("Exiting.....")
                time.sleep(5)
                return
            else:
                return "\nYour account is verified by Manager.. \nYou can procced..\n"
        except Exception as e:
            print(f'error : {e}')
        finally:
            self.close_db() 
        #return m_check

    # manager verification can verify admin to procced
    def manager_option_verification(self):
        pin = int(input("enter your manager pins : "))
        if pin == 7641011:
            m_v_admin_id = input("enter the admin id to verify : ").upper().strip()
            m_v_email_id = input("enter the email id of admin to verify : ").upper().strip()
            try:
                self.connect_db()
                mycursor.execute("select AD_NAME, AD_EMAIL_ID from admin where AD_USER_ID = %s;",(m_v_admin_id,))
                check = mycursor.fetchone()
                if check:
                    name = check[0]
                    db_email = check[1]
                    if db_email == m_v_email_id:
                        mycursor.execute("update admin set M_status = 'APPROVED',updated_at = %s where AD_USER_ID = %s;",(self.curr_time(), m_v_admin_id))
                        mycon.commit()

                        subject_m_v = "ACCOUNT VERIFIED"
                        message_m_v = f'''
Hello, {name}
This Email is from ATM SIMULATOR by DEV
your Account has been approved by Manager
Now you can login and do your works.
Best regards
Dev
'''          
                        m_con_email = self.email_sender.send_email(db_email, subject_m_v, message_m_v)
                        if m_con_email == "EMAIL SEND":
                            print(f"{m_v_admin_id} Account has been verification Succesfull")
                        else:
                            mycursor.execute("select M_STATUS from admin where AD_USER_ID = %s;", (m_v_admin_id,))
                            s_check = mycursor.fetchone()[0]
                            if s_check == "PENDING":
                                print("❌❌❌ verification failed.... ❌❌❌")
                                return
                            else:
                                print("Verification success")
                    else:
                        print("❌❌❌ entered email doesnot match with DB check it again..... ❌❌❌")
                        return
                    
                else:
                    print("❌❌❌ Admin Id not found. ❌❌❌")
                    return
                    
            except Exception as e:
                print(f'Error : {e}')
            finally:
                self.close_db()
        else:
            print("❌❌❌ Incorrect Manager pin. ❌❌❌")
            return

    # add new user
    def new_user_account(self):
        self.new_user.user_registration()

    # view all account in db
    def view_all_account(self):
        try:
            self.connect_db()
            mycursor.execute("select USER_ID, ACCOUNT_NO, USER_FULLNAME AS NAME, USER_CONTACT_NO AS NUMBER, USER_EMAIL_ID AS EMAIL_ID, USER_ADDRESS AS ADDRESS, USER_DOB AS DOB, CREATED_AT from user_info;")
            data = mycursor.fetchall()
            print("getting details.....\n")
            columns_name = [i[0] for i in mycursor.description]
            time.sleep(5)
            print(tabulate(data,headers=columns_name, tablefmt="fancy_grid"))
            self.close_db()

        except Exception as e:
            print(f"error while fetching details : {e}")

    # total balance available with bank
    def total_balance(self):
        try:
            self.connect_db()
            mycursor.execute("select sum(balance) as Total_Balance from account;")
            data = mycursor.fetchone()

            print("getting balance....\n")

            columns_name = [i[0] for i in mycursor.description]
            time.sleep(5)

            formatted_data = [[f'{data[0]:,.2f}' if data[0] is not None else "N/A"]]

            print(tabulate(formatted_data, headers=columns_name, tablefmt="fancy_grid"))
            self.close_db()

        except Exception as e:
            print(f"error while fetching details : {e}")

    # change user details like name, email_id, mobile_no,  date of birth
    def update_user_details(self):
        try:
            self.connect_db()
            username = input("enter username : ").upper().strip()
            mycursor.execute("select user_fullname, user_email_id, user_contact_no, user_dob from user_info where user_id = %s;",(username,))
            result = mycursor.fetchone()[0]

            subject_info = "DETAILS CHANGED"

            option = int(input('''\noperation : 
1. change Name
2. change Email_ID
3. Change Contact_No.
4. change DOB
5. Exit
: '''))
            
            if option == 1:
                new_name = input("\nenter new name : ").upper().strip()
                
                message_name_info = f'''
Hello {result[0]},
This email is from ATM Simulator by DEV
This is to inform you that your name has been changed from {result[0]} to {new_name}
if it is not done on your request then inform as soon as possible
this is system generated mail, please don't reply to this mail 
thank You
'''
                email = self.email_sender.send_email(result[1], subject_info, message_name_info)
                if email == "EMAIL SEND":
                    mycursor.execute("update user_info set user_fullname = %s, updated_at = %s where user_id = %s;",(new_name, self.curr_time(),username,))
                    mycon.commit()
                    print(f"Name changed to || {new_name} || successfully")
                else:
                    print("something went wrong.....")

            elif option == 2:
                new_email_id = input("\nenter new Email ID : ").upper().strip()
                message_email_info = f'''
Hello {result[0]},
This email is from ATM Simulator by DEV
This is to inform you that your EMAIL ID has been changed from {result[1]} to {new_email_id}
------------------------------------
Please verify your email by login
------------------------------------
if it is not done on your request then inform as soon as possible
this is system generated mail, please don't reply to this mail 
thank You
'''
                email = self.email_sender.send_email(result[1], subject_info, message_email_info)
                if email == "EMAIL SEND":
                    email_s = self.email_sender.send_email(new_email_id, subject_info, message_email_info)
                    if email_s == "EMAIL SEND":
                        mycursor.execute("update user_info set user_email_id = %s,updated_at = %s, status = 'PENDING' where user_id = %s;",(new_email_id, self.curr_time(), username,))
                        mycon.commit()
                        print(f"Email Id changed to || {new_email_id} || successfully")
                    else:
                        print("something went wrong...")
                else:
                    print("something went wrong...")

            elif option == 3:
                new_number = int(input("enter new number : "))
                message_number_info = f'''
Hello {result[0]},
This email is from ATM Simulator by DEV
This is to inform you that your Mobile Number has been changed from {result[2]} to {new_number}
if it is not done on your request then inform as soon as possible
this is system generated mail, please don't reply to this mail 
thank You
'''
                email = self.email_sender.send_email(result[1], subject_info, message_number_info)
                if email == "EMAIL SEND":
                    mycursor.execute("update user_info set user_contact_no = %s, updated_at = %s where user_id = %s;",(new_number, self.curr_time(), username))
                    mycon.commit()
                    print(f"Mobile number changed to || {new_number} || successfully")
                else:
                    print("Something went wrong....")

            elif option == 4:
                new_dob = input("enter new DOB [YYYY-MM-DD] : ").strip()
                message_dob_info = f'''
Hello {result[0]},
This email is from ATM Simulator by DEV
This is to inform you that your DATE OF BIRTH has been changed from {result[2]} to {new_number}
if it is not done on your request then inform as soon as possible
this is system generated mail, please don't reply to this mail 
thank You
'''
                email = self.email_sender.send_email(result[1], subject_info, message_dob_info)

                if email == "EMAIL SEND":
                    mycursor.execute("update user_info set user_dob = %s, updated_at = %s where user_id = %s;",(new_dob, self.curr_time(), username))
                    mycon.commit()
                else:
                    print("Something went wrong....")

            elif option == 5:
                print("exiting....")
                time.sleep(2)
                return
            
            else:
                print("invalid option....")
                return
                        
        except Exception as e:
            print(f"upating details error : {e}")

        finally:
            self.close_db()

    # delete user account
    def delete_user(self):
        try:
            self.connect_db()
            username = input("enter username : ")

            mycursor.execute("select balance from account where user_id = %s;",(username,))
            result = mycursor.fetchone()[0]

            if result == 0.00:
                mycursor.execute("delete from account where user_id = %s", (username,))
                mycursor.execute("delete from user_info where user_id = %s;", (username,))
                mycon.commit()
            else:
                print("account balance must be 0")

        except Exception as e:
            print(f"delete error : {e}")

        finally:
            self.close_db()

    # view statement of user based on one year or specific date
    def view_statement(self):
        try:
            self.connect_db()
            account_no = int(input("enter account no. of user : "))
            
            mycursor.execute("select * from account where account_no = %s;",(account_no,))
            result = mycursor.fetchone()

            if result:
                option = int(input("choice the option \n1. one year \n2. between specific date \n3. exit \n: "))
                cur_time = self.time_f.cur_time()   
                if option == 1:
                    one_year = self.time_f.one_year()
                    mycursor.execute("SELECT transaction_id, transaction_date as date, message, debit, credit, balance FROM transaction_log where account_no = %s and transaction_date between %s and %s;",(account_no, one_year, cur_time,))
                    data = mycursor.fetchall()

                elif option == 2:
                    start_date = input("enter start date in [YYYY-MM-DD] format : ")
                    start_date = start_date + " 00:00:00"
                    end_date = input("enter end date in [YYYY-MM-DD] format : ")
                    end_date = end_date + " 23:59:59"
                    mycursor.execute("SELECT transaction_id, transaction_date as date, message, debit, credit, balance FROM transaction_log where account_no = %s and transaction_date between %s and %s;",(account_no, start_date, end_date,))
                    data = mycursor.fetchall()

                elif option == 3:
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

            else:
                print("Account Number Not Found.....")

        except Exception as e:
            print(f"error while fetching statement : {e}")

    # update interset daily in user account but not reflect in main balance
    def update_int(self):
        try:
            self.connect_db()
            mycursor.execute("select account_no from account;")
            account = mycursor.fetchall()

            for acc in account:
                account_no = acc[0]

                mycursor.execute("select balance from account where account_no = %s",(account_no,))
                balance = mycursor.fetchone()[0]

                intrest = (((balance*5)/100)/365)

                mycursor.execute("select intrest_day_mon from account where account_no = %s;",(account_no,))
                exisitng_interest = mycursor.fetchone()[0]

                if exisitng_interest is None:
                    exisitng_interest = 0

                updated_intrest = exisitng_interest + intrest

                mycursor.execute("update account set intrest_day_mon = %s where account_no = %s;",(updated_intrest, account_no,))
                mycon.commit()
            print("interest updated in all account...")

        except Exception as e:
           print(f"update daily interset error : {e}")
        
        finally:
            self.close_db()

    # at end the month admin can call this function to credit all interset in account
    def update_interest_mon(self):
        try:
            self.connect_db()

            mycursor.execute("select account_no from account;")
            account = mycursor.fetchall()

            for acc in account:
                account_no = acc[0]

                mycursor.execute("select balance from account where account_no = %s",(account_no,))
                balance = mycursor.fetchone()[0]

                mycursor.execute("select intrest_day_mon from account where account_no = %s;",(account_no,))
                monthly_interest = mycursor.fetchone()[0]
            
                if monthly_interest is None:
                    monthly_interest = 0
                
                updated_balance = balance + monthly_interest


                mycursor.execute("update account set balance = %s, updated_at = %s, intrest_day_mon = %s where account_no = %s;",(updated_balance, self.curr_time(), None, account_no,))
                mycon.commit()

                ins_t = "insert into transaction_log (transaction_id, account_no, message, debit, credit, balance) values (%s,%s,%s,%s,%s,%s);"
                data_t = (self.tran.trn(), account_no, "INTEREST CREDITED", None, monthly_interest, updated_balance)

                mycursor.execute(ins_t, data_t)
                mycon.commit()

            print("Interest credited in all account......")
        
        except Exception as e:
            print(f"error while transfering monthly interest : {e}")

        finally:
            self.close_db()
    # main menu
    def option(self):
        try:
            while True:
                choice = int(input('''choice operations : 
1. New user account
2. View all account
3. View total balance in bank 
4. Update User Account details
5. Delete user Account
6. View statement of user
7. Update interset daily interset
8. update interset montly interset
9. Verify Admin
10. Exit                                                                                                                                                                                              
: '''))
                
                if choice == 1:
                    self.new_user_account()

                elif choice == 2:
                    self.view_all_account()

                elif choice == 3:
                    self.total_balance()

                elif choice == 4:
                    self.update_user_details()

                elif choice == 5:
                    self.delete_user()

                elif choice == 6:
                    self.view_statement()

                elif choice == 7:
                    self.update_int()

                elif choice == 8:
                    self.update_interest_mon()
                
                elif choice == 9:
                    print("Exiting.....")
                    time.sleep(5)
                    break
                else:
                    print("❌❌❌ Invalid Choice ❌❌❌")

        except Exception as e:
            print(f"option error : {e}")
        
    # creating main login operation
    def login_main(self):
        try:
            admin_id = input("enter your user id : ").upper().strip()
            admin_pass = input("enter your password : ").upper().strip()
            admin_confirm_pass = input("confirm your password : ").upper().strip()

            if admin_pass == admin_confirm_pass:
                print("\npassword matched......\nProcced")
                self.connect_db()
                mycursor.execute("select AD_PASSWORD from admin where AD_USER_ID = %s;",(admin_id,))
                passw = mycursor.fetchone()[0]
                self.close_db()

                if passw == admin_pass:
                    self.connect_db()
                    mycursor.execute("select AD_EMAIL_ID from admin where AD_USER_ID = %s;", (admin_id,))
                    email_id = mycursor.fetchone()[0]
                    self.close_db()
                    generated_L_ver_otp = self.get_otp()
                    subject_l_ver = "Login verification"
                    message_l_ver = f'''
This email is from ATM SIMULATOR by DEV
your otp for login verification is {generated_L_ver_otp}
this otp is valid for 2 min only
don't reply to this mail it is system generated mail
'''
                    email = self.email_sender.send_email(email_id, subject_l_ver, message_l_ver)
                    if email == "EMAIL SEND":
                        print("Verify OTP to login \nCheck your EMAIL ID")
                        vertify_l_otp = input('enter OTP to verify : ').strip()

                        if generated_L_ver_otp == vertify_l_otp:
                            print("\nlogin Succesfull......")
                            print("\nChecking account......")
                            time.sleep(5)
                            check_self_ver = self.admin_verification_check(admin_id, email_id)
                            if check_self_ver is None:
                                return
                            else:
                                print(check_self_ver)
                            check_manager_ver = self.manager_verification_check(admin_id)
                            if check_manager_ver is None:
                               return
                            else:
                                print(check_manager_ver)
                                self.option()

                        else:
                            print("❌❌❌ INVALID OTP ❌❌❌")
                else:
                    print("❌❌❌ Incorrect password!!!! ❌❌❌")
            else:
                print("❌❌❌ Password Doesnot Matched!!!!! ❌❌❌")
                        
        except Exception as e:
            print(e)                                            


if __name__ == "__main__":
    a = admin_login()
    a.login_main()