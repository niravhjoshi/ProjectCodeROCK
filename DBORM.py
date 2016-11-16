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

class DateWiseDetailKnownErrCounts(peewee.Model):

    cust_name= peewee.CharField()
    month_name = peewee.CharField()
    err_name= peewee.CharField()
    appsrv_name = peewee.CharField()
    date_day = peewee.DateField()
    err_counts = peewee.IntegerField()

    class Meta:
        database = db

try:
    DateWiseDetailKnownErrCounts.create_table()
except peewee.InternalError:
    print "DateWiseDetailKnownErrCounts table already exists!"


class DateWiseErrCounts(peewee.Model):

    cust_name = peewee.CharField()
    date_stamp = peewee.DateField()
    month_name = peewee.CharField()
    appsrv_name = peewee.CharField()
    err_counts  = peewee.IntegerField()

    class Meta:
        database = db

try:
    DateWiseErrCounts.create_table()
except peewee.InternalError:
    print "DateWiseErrCounts table already exists!"

