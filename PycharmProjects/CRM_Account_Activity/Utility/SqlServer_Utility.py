# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：SqlServer数据库 操作类
#   版本：0.1
#   作者：Henry.Zhou
#   日期：2015.06.03
#   语言：Python 2.7
#---------------------------------------
import pymssql
from Account_Item import Account_Item
from Utility.Log_Utility import Log_Utility as Log

class SqlServer_Utility(object):
    host = "203.88.173.107"
    # 根据类型获取节假日
    def GetCalendarDay(self, type):
        self.conn = pymssql.connect(host=self.host,user="sa",password="newegg@123",database="wisecrm_nbs")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT DISTINCT [start] FROM [wisecrm_nbs].[dbo].[calendar] WHERE title = %s", (type))
        list = self.cur.fetchall()
        items = []
        for (start) in list:
            items.append(start)
        self.cur.close()
        self.conn.close()
        return items

    # 根据客户类型获取客户信息
    def GetAccountByCustomerTypeCode(self, typeCode):
        self.conn = pymssql.connect(host=self.host,user="sa",password="newegg@123",database="wisecrm_nbs")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT AccountId,AccountName,CustomerTypeCode,OwningBusinessUnit FROM Account WHERE SystemObjectTypeCode ='1' AND CustomerTypeCode = %s AND OwningBusinessUnit != '030-0cb12d9f-c907-4414-8d4a-fca3d01b63da' AND  isDeleted = 0", (typeCode))
        list = self.cur.fetchall()
        items = []
        for (AccountId, AccountName, CustomerTypeCode, OwningBusinessUnit) in list:
            item = Account_Item()
            item.AccountId = AccountId
            item.AccountName = AccountName
            item.CustomerTypeCode = CustomerTypeCode
            item.OwningBusinessUnit = OwningBusinessUnit
            items.append(item)
        self.cur.close()
        self.conn.close()
        return items

    # 根据客户类型获取客户信息
    def GetAccountByCustomerTypeCode2(self, typeCode):
        self.conn = pymssql.connect(host=self.host,user="sa",password="newegg@123",database="wisecrm_nbs")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT AccountId,AccountName,CustomerTypeCode,(SELECT TOP 1 endTime FROM Activity WHERE State ='2' AND systemObjectTypeCode ='1' AND AccountId = Account.AccountId ORDER BY endTime DESC) AS ActivityTime ,OwningBusinessUnit,(SELECT FullName FROM [User] WHERE UserId = Account.OwningUser) AS FullName FROM Account WHERE SystemObjectTypeCode ='1' AND isDeleted <> 1 AND CustomerTypeCode = %s AND OwningBusinessUnit != '030-0cb12d9f-c907-4414-8d4a-fca3d01b63da' AND c__cjjg > 2 AND  isDeleted = 0", (typeCode))
        list = self.cur.fetchall()
        items = []
        for (AccountId,AccountName,CustomerTypeCode,ActivityTime,OwningBusinessUnit,FullName) in list:
            item = Account_Item()
            item.AccountId = AccountId
            item.AccountName = AccountName
            item.CustomerTypeCode = CustomerTypeCode
            item.ActivityTime = ActivityTime
            item.OwningBusinessUnit = OwningBusinessUnit
            item.FullName = FullName
            items.append(item)
        self.cur.close()
        self.conn.close()
        return items

    #无效：7   以在其它机构：13  联系不上：11
    def GetAccountByCustomerTypeCode3(self):
        self.conn = pymssql.connect(host=self.host,user="sa",password="newegg@123",database="wisecrm_nbs")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT AccountId,AccountName,CustomerTypeCode,(SELECT TOP 1 CreatedOn FROM Activity WHERE State ='2' AND systemObjectTypeCode ='1' AND AccountId = Account.AccountId ORDER BY CreatedOn DESC) AS ActivityTime ,OwningBusinessUnit,(SELECT FullName FROM [User] WHERE UserId = Account.OwningUser) AS FullName FROM Account WHERE SystemObjectTypeCode ='1' AND isDeleted <> 1 AND CustomerTypeCode in (7,13,11) AND OwningBusinessUnit != '030-0cb12d9f-c907-4414-8d4a-fca3d01b63da' AND  isDeleted = 0")
        list = self.cur.fetchall()
        items = []
        for (AccountId,AccountName,CustomerTypeCode,ActivityTime,OwningBusinessUnit,FullName) in list:
            item = Account_Item()
            item.AccountId = AccountId
            item.AccountName = AccountName
            item.CustomerTypeCode = CustomerTypeCode
            item.ActivityTime = ActivityTime
            item.OwningBusinessUnit = OwningBusinessUnit
            item.FullName = FullName
            items.append(item)
        self.cur.close()
        self.conn.close()
        return items

    def UpdateAccountCustomerType(self,accountId):
        item = []
        #conn=pymssql.connect(host="203.88.173.107",user="sa",
        #password="newegg@123",database="wisecrm_nbs")
        #cur=conn.cursor()
        #cur.execute("UPDATE Account SET CustomerTypeCode = 4 WHERE AccountId = %s ", (accountId))
        #conn.commit()
        #cur.close()
        #conn.close()


    #超过2天未联系
    def GetAccountByCustomerTypeCode4(self):
        self.conn = pymssql.connect(host=self.host,user="sa",password="newegg@123",database="wisecrm_nbs")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT AccountId FROM account WHERE systemObjectTypeCode=1 AND c__gjlb = 0 AND c__cjjg > 2 AND (c__wlxts is null or c__wlxts like '') AND  isDeleted = 0")
        list = self.cur.fetchall()
        items = []
        for (AccountId) in list:
            item = Account_Item()
            item.AccountId = AccountId
            items.append(item)
        self.cur.close()
        self.conn.close()
        return items
