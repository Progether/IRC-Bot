import psycopg2
import ircHelpers
import settings

class DB:
    def db_connect(self):
        config = settings.read_config()
        conn = psycopg2.connect(
                                database = config['db_name'],
                                user     = config['db_user'],
                                password = config['db_pass'],
                                host     = config['db_host'],
                                port     = config['db_port'])
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
            SQL = "DROP TABLE IF EXISTS %s" % table_name
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
            SQL = "INSERT INTO %s (%s) VALUES(%s);" % (table_name,table_columns,column_data)
            cur.execute(SQL)
            conn.commit()
            conn.close()
        else:
            ircHelpers.sayInChannel("There is no table: %s" % table_name)
            
    def db_get_data(self,table_name,condition_column_name,condition_value,):
        if self.db_check_table(table_name):
            conn = self.db_connect()
            cur = conn.cursor()
            SQL = "SELECT * FROM %s WHERE %s = '%s'" % (table_name,condition_column_name,condition_value)
            cur.execute(SQL)
            response = cur.fetchall()
            conn.close()
            return response

    def db_get_all_data(self,table_name):
        if self.db_check_table(table_name):
            conn = self.db_connect()
            cur = conn.cursor()
            SQL = "SELECT * FROM %s" % (table_name)
            cur.execute(SQL)
            response = cur.fetchall()
            conn.close()
            return response

    def db_delete_data(self,table_name,condition_column_name,condition_value):
        if self.db_check_table(table_name):
            conn = self.db_connect()
            cur = conn.cursor()
            SQL = "DELETE FROM %s WHERE %s = '%s'" % (table_name,condition_column_name,condition_value)
            cur.execute(SQL)
            conn.commit()
            conn.close()
        else:
            ircHelpers.sayInChannel("There is no table: %s" % table_name)

    def db_update_data(self,table_name,column_name,changed_value,condition_column_name,condition_value,):
        if self.db_check_table(table_name):
            conn = self.db_connect()
            cur = conn.cursor()
            SQL = "UPDATE "+table_name+" SET "+column_name+" = %s WHERE "+condition_column_name+" = "+condition_value
            cur.execute(SQL, (changed_value))
            conn.commit()
            conn.close()
        else:
            ircHelpers.sayInChannel("There is no table: %s" % table_name)

    def db_check_table(self,table_name):
        conn = self.db_connect()
        cur = conn.cursor()
        SQL = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)"
        data = (table_name, )
        cur.execute(SQL, data)
        response = cur.fetchone()[0]
        conn.close()
        return response

if __name__ == "__main__":
    print("Creating databases...")
    ##TODO