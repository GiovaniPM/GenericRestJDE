import datetime

def datestdtojd (stddate):
    fmt='%Y-%m-%d'
    sdtdate = datetime.datetime.strptime(stddate, fmt)
    nmyear=sdtdate.year
    sdtdate = sdtdate.timetuple()
    jdate = sdtdate.tm_yday
    return(nmyear*1000+jdate)

def jdtodatestd (jdate):
    fmt = '%Y%j'
    datestd = datetime.datetime.strptime(jdate, fmt).date()
    return(datestd)

def timestdtonum (stddate):
    fmt='%H:%M:%S'
    stddate = datetime.datetime.strptime(stddate, fmt)
    mmHour=stddate.hour
    mnMinute=stddate.minute
    mnSecond=stddate.second
    return(mnSecond+100*mnMinute+10000*mmHour)

print(datestdtojd('1999-11-01')-1900000)
print(jdtodatestd(str(2018305)))
print(timestdtonum("14:09:01"))