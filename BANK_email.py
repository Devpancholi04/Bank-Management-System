import smtplib

class email_send:

    def send_email(self, email_id, subject, message): 
        try:
            text = f'subject : {subject}{message}'
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()

            server.login("atm.simulatorby.dev@gmail.com", "fdxx gtmn kxhb lyzm")
            server.sendmail("atm.simulatorby.dev@gmail.com", email_id, text)
            server.quit()
            return "EMAIL SEND"                

        except Exception as e:
            return f"error : {e}"
        
if __name__ == "__main__":
    email = email_send()
    email_id = "devpancholigt2004@gmail.com"
    subject = "email"
    message = "\nthis is the sample email"
    email_status = email_send.send_email(email_id, subject, message)
    print("email_status")