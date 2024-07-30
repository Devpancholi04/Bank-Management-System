import mysql.connector as sqltor
from BANK_otp_gen import otp
from BANK_email import email_send

class user_reg:

    def __init__(self):
        self.email_sender = email_send()

    def connect_db(self):
        global mycon, mycursor
        mycon = sqltor.connect(host = "localhost", user = "root", passwd = "DEV19163247", database = "ATM_SIMULATOR")
        mycursor = mycon.cursor()

    def close_db(self):
        mycursor.close()
        mycon.close()

    def get_otp(self): 
        generated_otp = otp.otp_generation(self)
        print(f"generated otp : {generated_otp}")
        return generated_otp
    
    def user_registration(self):
        try:
            username = input("create username : ").upper().strip()
            fullname = input("enter your name : ").upper().strip()
            contact_no = int(input("enter your mobile number : "))
            email_id = input("enter your email id : ").upper().strip()
            address = input("enter your address : ").upper().strip()
            dob = input("enter your date of birth : [yyyy-mm-dd] : ").strip()
            password = input("create password : ").strip()
            re_password = input("confirm password : ").strip()

            if re_password == password:
                print("password matched....")
                print("verify your email id : ")
                generated_otp = self.get_otp()

                sub_otp = "OTP Verification Mail"
                mes_otp = f'''
This email is from ATM Simulator by DEV
your otp for verification {generated_otp}
this otp is valid for 2 min only
don't reply to this mail it is system generated mail
'''
                
                email = self.email_sender.send_email(email_id, sub_otp, mes_otp)
                if email == "EMAIL SEND":
                    print("otp has been send!!!")
                    verify_otp = input("enter the OTP which you received in email : ").strip()

                    if generated_otp == verify_otp:
                        print("VERIFING.........\n")
                        self.connect_db()
                        ins = "insert into USER_INFO (USER_ID, ACCOUNT_NO, USER_FULLNAME, USER_CONTACT_NO, USER_EMAIL_ID, USER_ADDRESS, USER_DOB, PASSWORD, STATUS, UPDATED_AT) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                        data = (username, None, fullname, contact_no, email_id, address, dob, password, "APPROVED", None)
                        mycursor.execute(ins, data)
                        mycon.commit()
                        self.close_db()

                        print("your login details are :- ")
                        print("----------------------------")
                        print(f"user_id = {username}")
                        print(f"password = {password}")
                        print("----------------------------")

                        # SENDING EMAIL.............
                        message_det = f'''
This email is from ATM SIMULATOR by DEV
YOUR EMAIL HAS BEEN VERIFIED
your user login details are as followed.....
---------------------------------------
USER_ID = {username}
PASSWORD = {password}
---------------------------------------
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
don't share this details with any one and save it for future reference........
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
---------------------------------------
dont reply to this mail it is system generated mail
'''
                        subject_det = "LOGIN DETAILS"
                        details_send = self.email_sender.send_email(email_id, subject_det, message_det)
                        print('login details send on email for future reference...........')
                        print("Reminder.........")
                        print("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
                        print("--------------------------------------")
                        print("DON'T SHARE THIS DETAILS WITH ANY ONE........")
                        print("--------------------------------------")
                        print("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
                        print(details_send)
                        return
                    else:
                        print("❌❌❌ Inavlid OTP ❌❌❌")
                        return
                else:
                    print(email)
                    print("your email is not verified ❌❌❌ till now.... verify your email by login first to perform other task....")
                    self.connect_db()
                    ins = "insert into USER_INFO (USER_ID, ACCOUNT_NO, USER_FULLNAME, USER_CONTACT_NO, USER_EMAIL_ID, USER_ADDRESS, USER_DOB, PASSWORD, UPDATED_AT) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    data = (username, None, fullname, contact_no, email_id, address, dob, password, None)
                    mycursor.execute(ins, data)
                    mycon.commit()

                    print("\nyour login details are :- ")
                    print("----------------------------")
                    print(f"user_id = {username}")
                    print(f"password = {password}")
                    print("----------------------------")
                    # SENDING EMAIL.............
                    subject_nv_det = "LOGIN DETAILS"
                    message_nv_det = f'''
This email is from ATM SIMULATOR by DEV
your USER login details are as followed.....
---------------------------------------
USER_ID = {username}
PASSWORD = {password}
---------------------------------------
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
---------------------------------------
your email has not been verified yet..... please verify it by login 
---------------------------------------
don't share this details with any one and save it for future reference........
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-------------       --------------------------
dont reply to this mail it is system generated mail
'''
                    details_send = self.email_sender.send_email(email_id, subject_nv_det, message_nv_det)
                    print('login details send on email for future reference...........')
                    print("Reminder.........")
                    print("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
                    print("--------------------------------------")
                    print("DON'T SHARE THIS DETAILS WITH ANY ONE........")
                    print("--------------------------------------")
                    print("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
                    print(details_send)
                    return  

            else:
                print("\n❌❌❌ your password does not match..... ❌❌❌")
                print("your form has been reset... fill all details again.....")
                return

        except Exception as e:
            print(f'error : {e}')


if __name__ == "__main__":
    reg = user_reg()
    reg.user_registration()