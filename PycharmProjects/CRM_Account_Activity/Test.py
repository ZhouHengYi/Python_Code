# -*- coding: utf-8 -*-
import datetime
import time
from Utility.DateTime_Utility import  DateTime_Utility as dt



print str(dt.datediff(dt,dt.datetostr('2015-05-29 16:27:20.613000'),dt.datetostr(datetime.datetime.now())))
listA = dt.getDays(dt,dt.datetostr('2015-05-29 16:27:20.613000'),dt.datetostr(datetime.datetime.now()))
listB = [(u'2015-05-03',), (u'2015-05-09',), (u'2015-05-10',), (u'2015-05-16',), (u'2015-05-31',), (u'2015-06-06',), (u'2015-06-07',), (u'2015-06-13',), (u'2015-06-14',), (u'2015-06-20',), (u'2015-06-21',), (u'2015-06-27',), (u'2015-06-28',), (u'2015-07-04',), (u'2015-07-05',), (u'2015-07-11',), (u'2015-07-12',), (u'2015-07-18',), (u'2015-07-19',), (u'2015-07-25',), (u'2015-07-26',), (u'2015-08-01',), (u'2015-08-02',), (u'2015-08-08',), (u'2015-08-09',), (u'2015-08-15',), (u'2015-08-16',), (u'2015-08-22',), (u'2015-08-23',), (u'2015-08-29',), (u'2015-08-30',), (u'2015-09-05',), (u'2015-09-06',), (u'2015-09-12',), (u'2015-09-13',), (u'2015-09-19',), (u'2015-09-20',), (u'2015-09-26',), (u'2015-09-27',), (u'2015-10-03',)]

print listA
print dt.jieJiaRi(dt,listA,listB)