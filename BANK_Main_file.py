from BANK_admin_reg import admin_reg
from BANK_admin_login import admin_login
from BANK_user_reg import user_reg
from BANK_user_login import user_log
import time

class main:

    def __init__(self):
        self.admin_registration = admin_reg()
        self.admin_log = admin_login()

        self.user_registration = user_reg() 
        self.user_login = user_log()

    def choice(self):
        option = input("Enter your choice: \n1. REGISTRATION__(R) \n2. LOGIN__(L) \n3. EXIT__(E,EXIT) \n: ").upper().strip()
        return option

    def main_menu(self):
        try:
            while True:
                choice = input("Enter your choice: \n1. EMPLOYEE__(E) \n2. USER__(U) \n3. EXIT__(EXIT) \n: ").upper().strip()

                if choice == '1' or choice == "E":
                    option = self.choice()

                    if option == '1' or option == "R":
                        print()
                        self.admin_registration.admin_registration()
                    elif option == '2' or option == "L":
                        print()
                        self.admin_log.login_main()
                    elif option == "3" or option == "E" or option == "EXIT":
                        print("Exiting....")
                        time.sleep(5)
                        break
                    else:
                        print("Invalid Choice")

                elif choice == '2' or choice == "U":
                    option = self.choice()

                    if option == '1' or option == "R":
                        print()
                        self.user_registration.user_registration()
                    elif option == '2' or option == "L":
                        print()
                        self.user_login.main()
                    elif option == "3" or option == "E" or option == "EXIT":
                        print("Exiting....")
                        time.sleep(5)
                        break
                    else:
                        print("Invalid Choice")

                elif choice == "3" or choice == "EXIT":
                    print("Exiting...")
                    time.sleep(5)
                    exit()
                else:
                    print("Invalid Choice")
                    

        except Exception as e:
            print(f"Error in main file: {e}")


if __name__ == "__main__":
    m = main()
    m.main_menu()
