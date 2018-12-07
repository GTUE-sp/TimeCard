import sqlite3
from datetime import datetime

class DB:
    def __init__(self):
        self.con = sqlite3.connect('./DB.db', isolation_level = None)
        self.cur = self.con.cursor()
        self.init_db()

    def init_db(self):
        sql = u"""
        create table if not exists students(
            student_num varchar(255),
            hash varchar(255),
            kj_family_name varchar(255),
            kj_first_name varchar(255),
            ka_family_name varchar(255),
            ka_first_name varchar(255)
        );
        """
        self.con.execute(sql)
        sql = u"""
        create table if not exists administrator(
            id varchar(255),
            password varchar(255)
        );
        """ 
        self.con.execute(sql)
        sql = u"""
        create table if not exists authHistory(
            datetime varchar(255),
            name varchar(255)
        );
        """
        self.con.execute(sql)

    def delete_table(self, table):
        sql = "drop table %s" % (table)
        self.cur.execute(sql)

    def insert_record(self, table, values):
        sql = u"insert into %s values" % (table)
        insert = ' ('
        for value in values:
            insert += self.__change_value_format(value)
            insert += ','
        insert = insert[0:len(insert)-1]
        insert += ')'
        sql += insert
        self.con.execute(sql)

    def update_field(self, table, column, conditions, value):
        sql = u"update %s set %s = '%s'" % (table, column, value)
        where = self.__make_where(conditions)
        sql += where
        self.con.execute(sql)

    def delete_record(self, table, conditions):
        sql = u'delete from %s' % (table)
        where = self.__make_where(conditions)
        sql += where
        self.con.execute(sql)

    def get_field(self, table, column, conditions):
        sql = u'select %s from %s' % (column, table)
        if not conditions is None:
            where = self.__make_where(conditions)
            sql += where
        self.cur.execute(sql)
        record = self.cur.fetchone()
        if record is None: return None
        else: return record[0]

    def get_table_tuple(self, table):
        sql = u'select * from %s' % (table)
        self.cur.execute(sql)
        table_tuple = self.cur.fetchall()
        return table_tuple

    def print_table(self, table):
        sql = u"select * from %s" % (table)
        self.cur.execute(sql)
        for row in self.cur:
            print(row)

    def print_db(self):
        sql = u'select * from sqlite_master'
        self.cur.execute(sql)
        for row in self.cur:
            print(row)

    def __change_value_format(self, value):
        if isinstance(value, str): return "'" + value + "'"
        else: return str(value)

    def __make_where(self, conditions):
        text = u' where '
        for column, value in conditions.items():
            text += column + '='
            text += self.__change_value_format(value)
            text += ' and '
        return text[0:len(text) - 5]