import psycopg2
import ircHelpers
import urllib.parse
import os

class DB:
  def db_connect(self):
    urllib.parse.uses_netloc.append("postgres")
    if "DATABASE_URL" not in os.environ:
      os.environ["DATABASE_URL"] = 'postgres://ddvzstnjeyvtkk:qiJbYxnbFTlXBAtRiyRkXGkFub@ec2-23-23-80-55.compute-1.amazonaws.com:5432/d2k2tmq3q2lk62'
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    return conn
  
  def db_add_table(self,table_name,table_info):
    # table_info should follow proper sql format. i.e db_add_table("test", "id PRIMARY_KEY, name varchar(20, sample_data text")
    conn = self.db_connect()
    cur = conn.cursor()
    SQL = "CREATE TABLE IF NOT EXISTS %s (%s);" % (table_name,table_info)
    cur.execute(SQL)
    conn.commit()
    conn.close()
    
  def db_drop_table(self,table_name):
    if self.db_check_table(table_name):
      conn = self.db_connect()
      cur = conn.cursor()
      SQL = "DROP TABLE IF EXISTS %s" % (table_name)
      cur.execute(SQL)
      conn.commit()
      conn.close()
    else:
      ircHelpers.sayInChannel("There is no table: %s" % table_name)

  def db_add_data(self,table_name,data):
    if self.db_check_table(table_name):
      conn = self.db_connect()
      cur = conn.cursor()
      table_columns = ''
      column_data =''
      for key in data.keys():
        table_columns = table_columns + key + ", "
        column_data = column_data + "'" + data[key] + "', "
      table_columns = table_columns[:-2]
      column_data = column_data[:-2]
      SQL = "INSERT INTO %s (%s) VALUES(%s);" % (table_name, table_columns,column_data)
      cur.execute(SQL)
      conn.commit()
      conn.close()
    else:
      ircHelpers.sayInChannel("There is no table: %s" % table_name)
      
  def db_get_data(self,table_name,condition_column_name,condition_value,column_names='*',condition_type='='):
    if self.db_check_table(table_name):
      conn = self.db_connect()
      cur = conn.cursor()
      SQL = "SELECT %s FROM %s WHERE %s %s '%s'" % (column_names,table_name,condition_column_name,condition_type,condition_value)
      cur.execute(SQL)
      response = cur.fetchall()
      conn.close()
      return response

  def db_delete_data(self,table_name,condition_column_name,condition_value,condition_type='='):
    if self.db_check_table(table_name):
      conn = self.db_connect()
      cur = conn.cursor()
      SQL = "DELETE FROM %s WHERE %s %s '%s'" % (table_name,condition_column_name,condition_type,condition_value)
      cur.execute(SQL)
      conn.commit()
      conn.close()
    else:
      ircHelpers.sayInChannel("There is no table: %s" % table_name)

  def db_update_data(self,table_name,column_name,changed_value,condition_column_name,condition_value,condition_type='='):
    if self.db_check_table(table_name):
      conn = self.db_connect()
      cur = conn.cursor()
      SQL = "UPDATE %s SET %s = '%s' WHERE %s %s '%s'" % (table_name,column_name,changed_value,condition_column_name,condition_type,condition_value)
      cur.execute(SQL)
      conn.commit()
      conn.close()
    else:
      ircHelpers.sayInChannel("There is no table: %s" % table_name)

  def db_check_table(self,table_name):
    conn = self.db_connect()
    cur = conn.cursor()
    SQL = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='%s')" % table_name
    cur.execute(SQL)
    response = cur.fetchone()[0]
    conn.close()
    return response

