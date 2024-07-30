import random
import datetime

class tran_id:
    
    def trn(self):
        rando = random.randint(1000,9999)
        time = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
        return f"TRN{time}--{rando}"
    
if __name__ == "__main__":
    t = tran_id()
    transaction_id = t.trn()
    print(transaction_id)