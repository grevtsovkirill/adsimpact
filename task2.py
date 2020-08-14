import datetime

import argparse
parser = argparse.ArgumentParser(description='Enter Start and Finish timestamps:')
parser.add_argument('--t0', type=str, default='2019-12-02 08:00:00', help="Start timestamp") 
parser.add_argument('--t1', type=str, default='2019-12-04 12:15:00', help="Finish timestamp") 
parser.add_argument('-l', action='append',default=[], help="List of holidays") 
args = parser.parse_args()

t0 = vars(args)["t0"]
t1 = vars(args)["t1"]
l = vars(args)["l"]

    
def hours_count(t0='2019-12-02 08:00:00',t1='2019-12-04 12:15:00',holidays=[],wd_start = 9,wd_end = 17):
    def valid_date(s):
        try:        
            return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print( "Not a valid date: '{0}'.".format(s))
            #raise 
    
    t0 = valid_date(t0)
    t1 = valid_date(t1)
    delta_all = t1-t0

    if (t1-t0).total_seconds()<0:
        print("Start date: '{0}' can't be later than Finish date {1}.".format(t0,t1)  )
        raise ValueError
    full_shift = wd_end-wd_start
    t0_hour=t0.hour + ( 0 if t0.minute==0 and t0.second==0 else 1)

    def end_of_day(t):
        if t>wd_start and t<wd_end: dlt=t-wd_start
        else: dlt=full_shift
        return dlt
    def is_wd(day,holidays_list=holidays):
        holidays = [ datetime.datetime.strptime(s, "%Y-%m-%d").date() for s in holidays_list]
        if day.weekday()<5 and day not in holidays:
            return True
        else: return False

    dayS_h = 0
    dayF_h = 0
    dayM_h=0
    n_wds=0

    
    if (t0_hour>wd_start and t0_hour<wd_end) and is_wd(t0):
        dayS_h = wd_start-t0_hour
    
    if delta_all.days==0 :
        if is_wd(t0) and t0_hour<wd_end:
            dayS_h+=end_of_day(t1.hour)
        if (t1-t0).total_seconds()<86399.0:
            total_hours = dayS_h
            return total_hours 
    else:
        if is_wd(t0) and t0_hour<wd_end:
            dayS_h+=full_shift
        for i in range(1,delta_all.days):            
            if is_wd(t0.date()+datetime.timedelta(days=i)): n_wds+=1
        dayM_h=n_wds*full_shift

        if is_wd(t1) and t1.hour>wd_start: dayF_h=end_of_day(t1.hour)

    total_hours = dayS_h+dayM_h+dayF_h
    #print(dayS_h,dayM_h,dayF_h,total_hours)
    return total_hours
            

    
if __name__ == "__main__":
    print(hours_count(t0,t1,l))
    
