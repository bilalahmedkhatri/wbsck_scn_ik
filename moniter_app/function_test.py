import datetime


x = datetime.datetime.now()
print(x.ctime().replace(" ", "_"))
