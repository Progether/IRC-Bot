import psycopg2
import ircHelpers
import settings

class DB:
    
    def __init__(self):
        self.tables = {
                       'mail'     : "sender text, recipient text, message text, id text",
                       'projects' : "name text, language text, link text, description text, id text"
                       }
        
    def db_connect(self):
        config = settings.read_config()
        try:
            conn = psycopg2.connect(
                            database = config['db_name'],
                            user     = config['db_user'],
                            password = config['db_pass'],
                            host     = config['db_host'],
                            port     = config['db_port'])
            return conn
        except psycopg2.Error as e:
            print("Error connecting to db")
            print(e)
            return None
    
    def db_add_table(self,table_name,table_info):
        # table_info should follow proper sql format.
        #     i.e: db_add_table("test", "id PRIMARY_KEY, name varchar(20, sample_data text)")
        try:
            if not self.db_check_table(table_name):
                conn = self.db_connect()
                cur = conn.cursor()
                SQL = "CREATE TABLE IF NOT EXISTS %s (%s);" % (table_name,table_info)
                cur.execute(SQL)
                conn.commit()
                return True
            else:
                print("!! Error creating table %s. Already exists" % table_name)
                return False
        except psycopg2.Error as e:
            print("Error creating new table: %s" % table_name)
            print(e)
            return False
        finally:
            try:
                conn.close()
            except Exception as e:
                print(e)
        
    def db_drop_table(self,table_name):
        try:
            if self.db_check_table(table_name):
                conn = self.db_connect()
                cur = conn.cursor()
                SQL = "DROP TABLE IF EXISTS %s" % table_name
                cur.execute(SQL)
                conn.commit()
                return True
            else:
                ircHelpers.sayInChannel("There is no table: %s" % table_name)
                return False
        except psycopg2.Error as e:
            print("Error dropping table: %s" % table_name)
            print(e)
            return False
        finally:
            try:
                conn.close()
            except Exception as e:
                print(e)

    def db_add_data(self,table_name,data):
        try:
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
                return True
            else:
                ircHelpers.sayInChannel("There is no table: %s" % table_name)
                return False
        except psycopg2.Error as e:
            print("Error adding data to table: %s" % table_name)
            print(e)
            return False
        finally:
            try:
                conn.close()
            except Exception as e:
                print(e)
            
    def db_get_data(self,table_name,condition_column_name,condition_value,):
        try:
            if self.db_check_table(table_name):
                conn = self.db_connect()
                cur = conn.cursor()
                SQL = "SELECT * FROM %s WHERE %s = '%s'" % (table_name,condition_column_name,condition_value)
                cur.execute(SQL)
                response = cur.fetchall()
                return response
            else:
                return None
        except psycopg2.Error as e:
            print("Error retrieving data from table: %s" % table_name)
            print(e)
            return None
        finally:
            try:
                conn.close()
            except Exception as e:
                print(e)

    def db_get_all_data(self,table_name):
        try:
            if self.db_check_table(table_name):
                conn = self.db_connect()
                cur = conn.cursor()
                SQL = "SELECT * FROM %s" % (table_name)
                cur.execute(SQL)
                response = cur.fetchall()
                return response
            else:
                return None
        except psycopg2.Error as e:
            print("Error retrieving data from table: %s" % table_name)
            print(e)
            return None
        finally:
            try:
                conn.close()
            except Exception as e:
                print(e)

    def db_delete_data(self,table_name,condition_column_name,condition_value):
        try:
            if self.db_check_table(table_name):
                conn = self.db_connect()
                cur = conn.cursor()
                SQL = "DELETE FROM %s WHERE %s = '%s'" % (table_name,condition_column_name,condition_value)
                cur.execute(SQL)
                conn.commit()
                return True
            else:
                ircHelpers.sayInChannel("There is no table: %s" % table_name)
                return False
        except psycopg2.Error as e:
            print("Error deleting data from table: %s" % table_name)
            print(e)
            return False
        finally:
            try:
                conn.close()
            except Exception as e:
                print(e)

    def db_update_data(self,table_name,column_name,changed_value,condition_column_name,condition_value,):
        try:
            if self.db_check_table(table_name):
                conn = self.db_connect()
                cur = conn.cursor()
                SQL = "UPDATE "+table_name+" SET "+column_name+" = %s WHERE "+condition_column_name+" = "+condition_value
                cur.execute(SQL, (changed_value))
                conn.commit()
                return True
            else:
                ircHelpers.sayInChannel("There is no table: %s" % table_name)
                return False
        except psycopg2.Error as e:
            print("Error updating data in table: %s" % table_name)
            print(e)
            return False
        finally:
            try:
                conn.close()
            except Exception as e:
                print(e)

    def db_check_table(self,table_name):
        try:
            conn = self.db_connect()
            cur = conn.cursor()
            SQL = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)"
            data = (table_name, )
            cur.execute(SQL, data)
            response = cur.fetchone()[0]
            if not response:
                print("!! DB Table not exists: %s" % table_name)
            return response
        except psycopg2.Error as e:
            print("Error checking table exists: %s  [ironic, right?]" % table_name)
            print(e)
            return False    ##ASK Really want to return False on fail here?? Table may actually exist.
        finally:
            try:
                conn.close()
            except Exception as e:
                print(e)

    def ensure_all_tables_exist(self):
        pass
    
    def recreate_table(self, table_name):
        pass
        
if __name__ == "__main__":
    pass