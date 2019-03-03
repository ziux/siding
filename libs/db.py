from django.db import connection
from libs.printf import print_debug



def select_sql(sql,args=None):
    cursor = connection.cursor()
    if args:
        cursor.execute(sql,args)
    else:
        cursor.execute(sql)
    res = cursor.fetchall()
    print_debug(res)
    return res

