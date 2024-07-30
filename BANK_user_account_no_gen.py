import random
import string

class account_no:
    def gen_account(self):
            try:
               poss = string.digits
               acc_no = ''.join(random.choice(poss) for _ in range(12))
               return acc_no
            except Exception as e:
                print(f'Error : {e}')

if __name__ == "__main__":
    acc = account_no()
    account_number = acc.gen_account()
    print(f'account no : {account_number}')