import peewee
from peewee import *


db = MySQLDatabase('centuriondb', user='root',passwd='gravitant')

'''
class Book(peewee.Model):
    author = peewee.CharField()
    title = peewee.TextField()

    class Meta:
        database = db

Book.create_table()
book = Book(author="me", title='Peewee is cool')
book.save()
for book in Book.filter(author="me"):
    print book.title
'''

class centurionapi_datewisedetailknownerrcounts(peewee.Model):

    cust_name= peewee.CharField()
    month_name = peewee.CharField()
    err_name= peewee.CharField()
    appsrv_name = peewee.CharField()
    date_date = peewee.DateField()
    err_counts = peewee.IntegerField()

    class Meta:
        database = db

try:
    centurionapi_datewisedetailknownerrcounts.create_table(fail_silently=True)
except peewee.InternalError:
    print "centurionapi_datewisedetailknownerrcounts table already exists!"
    pass

class centurionapi_datewiseerrcounts(peewee.Model):

    cust_name = peewee.CharField()
    date_stamp = peewee.DateField()
    month_name = peewee.CharField()
    appsrv_name = peewee.CharField()
    err_counts  = peewee.IntegerField()

    class Meta:
        database = db

try:
    centurionapi_datewiseerrcounts.create_table(fail_silently=True)
except peewee.InternalError:
    print "DateWiseErrCounts table already exists!"


class CustomerProdLogsLoca(peewee.Model):
    cust_name = peewee.CharField()
    add_date = peewee.DateField()
    appsrv_tools_logpath = peewee.CharField()
    appsrv_localws_logpath = peewee.CharField()
    log_monitor = peewee.BooleanField(default=True)

    class Meta:
        database = db
try:
    CustomerProdLogsLoca.create_table(fail_silently=True)
except peewee.InternalError:
    print "Sorry Table CustomerProdLogsLoca already exists!"


class KnownErrorsDict(peewee.Model):
    error_name =peewee.CharField()
    err_date = peewee.DateField()

    class Meta:
        database = db

try:
    KnownErrorsDict.create_table(fail_silently=True)
except peewee.InternalError:
    print "Sorry Table KnownErrorsDict already exists!"
    pass



