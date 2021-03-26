import re
import subprocess

import pymysql as MySQLdb
import sqlparse


class MysqlTool(object):
    """docstring for mysql"""

    def __init__(self, dbconfig):
        ''' cursor_dict参数存在时返回字典结构数据 '''
        self.db = {}
        self.db['connect_timeout'] = 20
        if 'charset' not in dbconfig: self.db['charset'] = 'utf8'
        self.cursor_dict = False
        if 'cursor_dict' in dbconfig: self.cursor_dict = dbconfig.pop('cursor_dict')
        self.db['host'] = dbconfig['host']
        self.db['port'] = int(dbconfig['port'])
        self.db['user'] = dbconfig['user']
        self.db['passwd'] = dbconfig['passwd']
        self.db['db'] = dbconfig['name']
        # 查询超过60秒，断开进程避免库挂了
        self.db['read_timeout'] = 60
        self._cursor = None

    def connect(self):
        ret = {'result': '', 'status': 0}
        try:
            self._conn = MySQLdb.connect(**self.db)
            if self.cursor_dict:
                self._cursor = self._conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            else:
                self._cursor = self._conn.cursor()
        except MySQLdb.Error as e:
            print(e)
            ret['status'] = -1
            ret['result'] = "Mysql Error {}: {}".format(e.args[0], e.args[1])
        return ret

    def is_select_sql(self, sql):
        ret = False
        sql = sqlparse.split(sql.lower())[0]
        if re.match(r"^select", sql): ret = True
        return ret

    def is_query_sql(self, sql):
        ret = False
        sql = sqlparse.split(sql.lower())[0]
        if re.match(r"^select|^show|^explain", sql): ret = True
        return ret

    def convert_sql(self, sql):
        return sql.replace('"', '\'')

    def sql_add_limit(self, sql, limit_num):
        # 对查询sql语句增加limit限制
        sql = sqlparse.split(sql.lower())[0]
        sql = sql.strip(' ;')
        if re.match(r"^select", sql):
            r = re.search(r"limit\s+(\d+)$", sql)
            _r = re.search(r"limit\s+(\d+)\s*,\s*(\d+)$", sql)
            if r:
                sql_limit_num = int(r.group(1))
                if sql_limit_num > limit_num:
                    sql = re.sub('\d+$', str(limit_num), sql)
            elif _r:
                offset = int(r.group(1))
                sql_limit_num = int(r.group(2))
                if sql_limit_num - offset > limit_num:
                    sql = re.sub('\d+$', str(limit_num), sql)
            else:
                sql = '{} limit {}'.format(sql, limit_num)
        return '{};'.format(sql)

    def execute(self, sql):
        ret = {'result': '', 'status': 0}
        try:
            if not self._cursor:
                ret = self.connect()
                if ret['status'] == -1: return ret
            self._cursor.execute(sql)
        except MySQLdb.Error as e:
            print(e)
            ret['status'] = -1
            ret['result'] = "Mysql Error {}: {}".format(e.args[0], e.args[1])
        return ret

    def select(self, table, column='*', condition='', row=False):
        ''' row=True时只查一行记录 '''
        condition = ' where ' + condition if condition else None
        if condition:
            sql = "select %s from %s %s" % (column, table, condition)
        else:
            sql = "select %s from %s" % (column, table)
        self.execute(sql)
        if row:
            return self._cursor.fetchone()
        else:
            return self._cursor.fetchall()

    def insert(self, table, tdict):
        column = ''
        value = ''
        for key in tdict:
            column += ',' + key
            value += "','" + str(tdict[key])

        column = column[1:]
        value = value[2:] + "'"
        sql = "insert into %s(%s) values(%s)" % (table, column, value)
        self._cursor.execute(sql)
        self._conn.commit()
        return self._cursor.lastrowid  # 返回最后的id

    def update(self, table, tdict, condition=''):
        if not condition:
            print("must have id")
            exit()
        else:
            condition = 'where ' + condition
        value = ''
        for key in tdict:
            value += ",%s='%s'" % (key, tdict[key])
        value = value[1:]
        sql = "update %s set %s %s" % (table, value, condition)
        self._cursor.execute(sql)
        self._conn.commit()
        return self.affected_num()  # 返回受影响行数

    def delete(self, table, condition=''):
        condition = 'where ' + condition if condition else None
        sql = "delete from %s %s" % (table, condition)
        self._cursor.execute(sql)
        self._conn.commit()
        return self.affected_num()  # 返回受影响行数

    def execsql(self, sql):
        self._cursor.execute(sql)
        self._conn.commit()
        return self.affected_num()  # 返回受影响行数

    def execute_sql(self, sql):
        self._cursor.execute(sql)
        self._conn.commit()
        return self.affected_num()  # 返回受影响行数

    def rollback(self):
        self._conn.rollback()

    def affected_num(self):
        return self._cursor.rowcount

    def get_databases(self):
        sql = 'show databases'
        self.execute(sql)
        return [row[0] for row in self._cursor.fetchall()]

    def get_tables(self):
        sql = 'show tables'
        self.execute(sql)
        return [row[0] for row in self._cursor.fetchall()]

    def get_variables(self):
        sql = 'show variables'
        self.execute(sql)
        return self._cursor.fetchall()

    def get_table_info(self, table_name):
        sql = 'SHOW CREATE TABLE {}'.format(table_name)
        self.execute(sql)
        return self._cursor.fetchall()[0][1]

    def get_columns(self, table_name):
        sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (
            self.db['db'], table_name)
        self.execute(sql)
        return [row[0] for row in self._cursor.fetchall()]

    def get_processlist(self):
        sql = 'show full processlist'

        self.execute(sql)
        return [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in self._cursor.fetchall()]

    def query_sql(self, sql):
        rets = {}
        try:
            self.execute(sql)
            rets['rows'] = self._cursor.fetchall()
            rets['effect_row'] = self.affected_num()
            rets['column_list'] = [row[0] for row in self._cursor.description]
        except MySQLdb.Error as e:
            rets['errmsg'] = str(e)
        return rets

    def get_user_drop_priv(self):
        sql = "SELECT Drop_priv FROM mysql.user WHERE User='{}' AND Host='{}'".format(self.db['user'], self.db['host'])
        self.execsql(sql)
        try:
            priv = self._cursor.fetchall()[0][0]
        except Exception:
            priv = 'N'
        return '-online-dsn' if priv == 'N' else '-test-dsn'

    def cmd_res(self, cmd):
        data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return data.stdout.read()

    def sql_beautify(self, sql):
        return sqlparse.format(sql, reindent=True, keyword_case='upper')

    def get_slave_hosts(self):
        sql = "select host from information_schema.processlist as p where p.command = 'Binlog Dump';"
        self.execute(sql)
        return [row[0].split(':')[0] for row in self._cursor.fetchall()]

    def sql_soar(self, sql, param, host='127.0.0.1'):
        # dsn = self.get_user_drop_priv()
        dsn = '-test-dsn'
        if host == '127.0.0.1':
            cmd = '''echo \"{}\" | soar {}=\"{}:{}@{}:{}/{}\" {}'''.format(self.convert_sql(sql), dsn, self.db['user'],
                                                                           self.db['passwd'], self.db['host'],
                                                                           self.db['port'], self.db['db'], param)
        else:
            cmd = "ssh root@{} '''echo \"{}\" | soar {}=\"{}:{}@{}:{}/{}\" {}'''".format(host, self.convert_sql(sql),
                                                                                         dsn, self.db['user'],
                                                                                         self.db['passwd'],
                                                                                         self.db['host'],
                                                                                         self.db['port'], self.db['db'],
                                                                                         param)
        return self.cmd_res(cmd)

    def sql_advisor(self, sql, host='127.0.0.1'):
        if host == '127.0.0.1':
            cmd = '''sqladvisor -u {} -p '{}' -P {} -h {} -d {} -q \"{}\" -v 1'''.format(self.db['user'],
                                                                                         self.db['passwd'],
                                                                                         self.db['port'],
                                                                                         self.db['host'], self.db['db'],
                                                                                         sql)
        else:
            cmd = "ssh root@{} '''sqladvisor -u {} -p '{}' -P {} -h {} -d {} -q \"{}\" -v 1'''".format(host,
                                                                                                       self.db['user'],
                                                                                                       self.db[
                                                                                                           'passwd'],
                                                                                                       self.db['port'],
                                                                                                       self.db['host'],
                                                                                                       self.db['db'],
                                                                                                       sql)
        return self.cmd_res(cmd)

    def __del__(self):
        try:
            self._cursor.close()
            self._conn.close()
        except:
            pass

    def close(self):
        self.__del__()
