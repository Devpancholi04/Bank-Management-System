import mysql.connector as sqltor
from BANK_otp_gen import otp
from BANK_email import email_send

class admin_reg:

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
    
    def admin_registration(self):
        try:
            ad_user_id = input("create your user Id: ").upper().strip()
            ad_name = input("enter your name : ").upper().strip()
            ad_number = int(input("enter your contact number : "))
            ad_email = input("enter your email id : ").upper().strip()
            ad_address = input("enter your address here : ").upper().strip()
            ad_pass = input("create your password : ").upper().strip()
            ad_repass = input("re-enter your password : ").upper().strip()

            if ad_pass == ad_repass:
                print("password matched.....")
                print("verify your email id : ")
                generated_otp = self.get_otp()
                subject_otp = "verification mail"
                message_otp = f'''
This email is from ATM Simulator by DEV
your otp for verification {generated_otp}
this otp is valid for 2 min only
don't reply to this mail it is system generated mail
'''
                email = self.email_sender.send_email(ad_email, subject_otp, message_otp)
                if email == "EMAIL SEND":
                    print("otp has been send!!!")
                    verify_otp = input("enter the OTP which you received in email : ").strip()


                    if generated_otp == verify_otp:
                        print("your email has been verified......")
                        self.connect_db()
                        ins = "INSERT INTO ADMIN (AD_USER_ID, AD_NAME, AD_CONTACT_NUMBER, AD_EMAIL_ID,Ad_ADDRESS, AD_PASSWORD, AD_verification, UPDATED_AT) values (%s, %s, %s, %s, %s, %s, %s,%s);"
                        data = (ad_user_id,ad_name,ad_number, ad_email, ad_address, ad_pass,"verified",None)
                        mycursor.execute(ins,data)
                        mycon.commit()
                        self.close_db()

                        print("your login details are :- ")
                        print("----------------------------")
                        print(f"user_id = {ad_user_id}")
                        print(f"password = {ad_pass}")
                        print("----------------------------")
                        # SENDING EMAIL.............
                        message_det = f'''
This email is from ATM SIMULATOR by DEV
YOUR EMAIL HAS BEEN VERIFIED
your ADMIN login details are as followed.....
---------------------------------------
USER_ID = {ad_user_id}
PASSWORD = {ad_pass}
---------------------------------------
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
don't share this details with any one and save it for future reference........
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
---------------------------------------
dont reply to this mail it is system generated mail
'''
                        subject_det = "LOGIN DETAILS"
                        details_send = self.email_sender.send_email(ad_email, subject_det, message_det)
                        print('login details send on email for future reference...........')
                        print("Reminder.........")
                        print("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
                        print("--------------------------------------")
                        print("DON'T SHARE THIS DETAILS WITH ANY ONE........")
                        print("your details has been shared with MANAGER for further verification.\nonce verification is complete you will get a mail and you can able to login.....")
                        print("--------------------------------------")
                        print("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
                        print(details_send)

                    else:
                        print("invalid otp.....")

                else:
                    print(email)
                    print("your email is not verified ❌❌❌ till now.... verify your email by login first to perform other task....")
                    self.connect_db()
                    ins = "INSERT INTO ADMIN (AD_USER_ID, AD_NAME, AD_CONTACT_NUMBER, AD_EMAIL_ID,Ad_ADDRESS, AD_PASSWORD, AD_verification, UPDATED_AT) values (%s, %s, %s, %s,%s,%s, %s, %s);"
                    data = (ad_user_id,ad_name,ad_number, ad_email, ad_address, ad_pass,"PENDING", None)
                    mycursor.execute(ins,data)
                    mycon.commit()
                    self.close_db()
                    print("your login details are :- ")
                    print("----------------------------")
                    print(f"user_id = {ad_user_id}")
                    print(f"password = {ad_pass}")
                    print("----------------------------")
                    # SENDING EMAIL.............
                    subject_nv_det = "LOGIN DETAILS"
                    message_nv_det = f'''
This email is from ATM SIMULATOR by DEV
your ADMIN login details are as followed.....
---------------------------------------
USER_ID = {ad_user_id}
PASSWORD = {ad_pass}
---------------------------------------
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
---------------------------------------
your email has not been verified yet..... please verify it by login 
---------------------------------------
don't share this details with any one and save it for future reference........
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
---------------------------------------
dont reply to this mail it is system generated mail
'''
                    details_send = self.email_sender.send_email(ad_email, subject_nv_det, message_nv_det)
                    print('login details send on email for future reference...........')
                    print("Reminder.........")
                    print("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
                    print("--------------------------------------")
                    print("DON'T SHARE THIS DETAILS WITH ANY ONE........")
                    print("--------------------------------------")
                    print("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
                    print(details_send)
            else:
                print("❌❌❌ your password does not match..... ❌❌❌")
                print("your form has been reset... fill all details again.....")

        except Exception as e:
            print(f"error : {e}")


if __name__ == "__main__":
    main = admin_reg()
    main.admin_registration()
