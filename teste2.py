import datetime

def valid_date(datestring):
    try:
        datetime.datetime.strptime(datestring, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def valid_time(datestring):
    try:
        datetime.datetime.strptime(datestring, '%H:%M:%S')
        return True
    except ValueError:
        return False

print(valid_date('2018-15-01'))
print(valid_time('52:00:00'))

#/^\d{4}-\d{2}-\d{2}$/