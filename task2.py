import datetime

def valid_date(s):
    try:
        
        return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        print(msg)
        raise 

def end_of_day(t1_hour,wd_end):
    if t1_hour<wd_end: dlt=t1_hour-9
    else: dlt=full_shift
    return dlt

def get_delta(t):
    delta = 0 
    if t.minute!=0: delta = 1
    return delta

def holidays_dates(holidays_list):
    holidays = [ datetime.datetime.strptime(s, "%Y-%m-%d").date() for s in holidays_list]
    return holidays

def is_wd(day,holidays_list = []):
    holidays = holidays_dates(holidays_list)
    if day.weekday()<5 and day not in holidays:
        return True
    else: return False
    
def hours_count(t0='2019-12-02 8:00:00',t1='2019-12-04 12:15:00', holidays=['2019-12-08','2019-12-05']):
#def hours_count(t0='2019-12-02 09:01:00',t1='2019-12-04 12:15:00'):
#def hours_count(t0='2019-12-01 09:30:00',t1='2019-12-07 12:15:00'):
    t0 = valid_date(t0)
    t1 = valid_date(t1)
    delta_all = t1.day-t0.day
    if (t1-t0).total_seconds()<0:
        print("Start date: '{0}' can't be later than Finish date {1}.".format(t0,t1)  )
        raise
    wd_start = 9
    wd_end = 17
    full_shift = wd_end-wd_start
    print(t1.day-t0.day)
    t0_hour=t0.hour+get_delta(t0) 

    dayI_h = 0
    dayL_h = 0
    dayM_h=0

    if (t0_hour>wd_start and t0_hour<wd_end) and is_wd(t0,holidays):
        dayI_h = wd_start-t0_hour
        
    if delta_all==0:
        if is_wd(t0,holidays) and t0_hour<wd_end:
            dayI_h+=end_of_day(t1.hour,wd_end)
    else:
        if is_wd(t0,holidays) and t0_hour<wd_end:
            dayI_h+=full_shift
        #loop over intermediate days
        n_wds=0
        for i in range(1,delta_all):
            tmp_date = t0.date()+datetime.timedelta(days=i)
            #check that it's working day
            if is_wd(tmp_date,holidays): n_wds+=1

        dayM_h=n_wds*full_shift

        if is_wd(t1,holidays): dayL_h=end_of_day(t1.hour,wd_end)

    total_hours = dayI_h+dayM_h+dayL_h
    print(dayI_h,dayM_h,dayL_h,total_hours)
            

    
if __name__ == "__main__":
    hours_count()
    
