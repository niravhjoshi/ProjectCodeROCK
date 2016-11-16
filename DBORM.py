import peewee
from peewee import *


db = MySQLDatabase('centuriondb', user='root',passwd='gravitant')

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


class DateWiseDetailKnownErrCounts(peewee.Model):
    id_field = PrimaryKeyField(),
    cust_name= peewee.CharField(),
    month_name = peewee.CharField(),
    err_name= peewee.CharField(),
    appsrv_name = peewee.CharField(),
    date_day = peewee.DateField()
    err_counts = peewee.IntegerField()

    class Meta:
        database = db
DateWiseDetailKnownErrCounts.create_table()


class DateWiseErrCounts(peewee.Model):
    id_field = PrimaryKeyField(),
    cust_name = peewee.CharField(),
    date_stamp = peewee.DateField(),
    month_name = peewee.CharField(),
    appsrv_name = peewee.CharField(),
    err_counts  = peewee.IntegerField()

    class Meta:
        database = db
DateWiseErrCounts.create_table()