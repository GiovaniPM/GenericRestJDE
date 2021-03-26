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

print(datestdtojd('1999-11-01')-1900000)
print(jdtodatestd(str(2018305)))