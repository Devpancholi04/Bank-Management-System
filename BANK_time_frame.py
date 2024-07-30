from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class time_frame:
    def __init__(self):
        self.current_timestamp = datetime.now()

    def cur_time(self):
        cur = self.current_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        #print(self.current_timestamp)
        #print(cur)
        return cur

    def one_year(self):
        one_year_time = self.current_timestamp - relativedelta(years=1)
        one = one_year_time.strftime('%Y-%m-%d') + '00:00:00'
        #print(one)
        return one

    def six_mon(self):
        six_mon = self.current_timestamp - relativedelta(months= 6)
        six = six_mon.strftime('%Y-%m-%d %H:%M:%S')
        #print(f"six : - {six}")
        return six

if __name__ == "__main__":
    ti = time_frame()
    ti.one_year()
    ti.six_mon()
    ti.cur_time()