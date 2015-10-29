import psycopg2
import ircHelpers
import yaml

class DB:
    
    # info for all tables.  # increment version number when updating create (look at self.__on_upgrade() too)
    tables = {
        ##   table     | version,    schema
            'tables'   : (1,
                    "table_name text PRIMARY KEY, "+
                    "current_version integer NOT NULL"),
            'mail'     : (1,
                    "sender text NOT NULL, "+
                    "recipient text NOT NULL, "+
                    "message text NOT NULL, "+
                    "id text NOT NULL"),
            'projects' : (1,
                    "name text NOT NULL, "+
                    "language text NULL, "+
                    "link text NULL, "+
                    "description text NULL, "+
                    "id text NOT NULL"), 
            'users'    : (1,
                    "_id integer PRIMARY KEY DEFAULT nextval('serial'), "+
                    "nick text NOT NULL, "+
                    "userlevel integer NOT NULL DEFAULT 0, "+
                    "last_online integer NOT NULL"),
            'logs'     : (1,
                    "_id integer PRIMARY KEY DEFAULT nextval('serial'), "+
                    "time type text NOT NULL, "+
                    "log text NOT NULL")
            }
    # unmanaged_tables are left alone by the automatic table handling - don't get created, updated etc
    unmanaged_tables = ('logs', 'users', 'tables')
    
    # future table ideas:  
    #   user: possibly include timezone settings to localise timestamps on logs, mail etc for each user (maybe with a '!!me' command group)
    
    def __init__(self):
        # test that all (managed) tables exist and are at correct version (version check not implemented yet)
        self.__ensure_all_tables_correct()

        
    def db_connect(self):
        with open("irc.yaml", 'r') as settings_file:
            conf = yaml.load(settings_file)
        try:
            conn = psycopg2.connect(
                            database = conf['database']['name'],
                            user     = conf['database']['user'],
                            password = conf['database']['pass'],
                            host     = conf['database']['host'],
                            port     = conf['database']['port'])
         
            return conn
        except psycopg2.Error as e:
            print("!! Error connecting to db")
            print(e)
            return None
    
    def db_add_table(self,table_name,table_info):
        # table_info should follow proper sql format.
        #     i.e: db_add_table("test", "id PRIMARY_KEY, name varchar(20, sample_data text)")
        print(".. Creating table: %s...\n  Schema: %s" % (table_name, table_info))
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
            print("!! Error creating new table: %s" % table_name)
            print(e)
            return False
        finally:
            try:
                conn.close()
            except Exception:
                pass
        
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
            print("!! Error dropping table: %s" % table_name)
            print(e)
            return False
        finally:
            try:
                conn.close()
            except Exception:
                pass

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
            print("!! Error adding data to table: %s" % table_name)
            print(e)
            return False
        finally:
            try:
                conn.close()
            except Exception:
                pass
            
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
            print("!! Error retrieving data from table: %s" % table_name)
            print(e)
            return None
        finally:
            try:
                conn.close()
            except Exception:
                pass

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
            print("!! Error retrieving data from table: %s" % table_name)
            print(e)
            return None
        finally:
            try:
                conn.close()
            except Exception:
                pass

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
            print("!! Error deleting data from table: %s" % table_name)
            print(e)
            return False
        finally:
            try:
                conn.close()
            except Exception:
                pass

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
            print("!! Error updating data in table: %s" % table_name)
            print(e)
            return False
        finally:
            try:
                conn.close()
            except Exception:
                pass

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
            print("!! Error checking table exists: %s  [ironic, right?]" % table_name)
            print(e)
            return False    ##ASK Really want to return False on fail here?? Table may actually exist.
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def __ensure_all_tables_correct(self):
        all_tables = DB.tables.keys()
        all_successful = True
        print(".. Checking all tables...")
        for table in all_tables:
            if table in DB.unmanaged_tables:
                continue
            if self.__ensure_table_correct(table):
                print(".. Table found: %s" % table)
            else:
                print("!! Table not found: %s" % table)
                if self.__recreate_table(table):
                    print(".. Created table: %s" % table)
                else:
                    print("!! Failed to create table: %s" % table)
                    all_successful = False
        return all_successful
    
    def __ensure_table_correct(self, table_name):
        # TODO Test old/new version numbers and trigger __on_upgrade, __recreate etc etc
        #   For now we'll just test if table exists
        return self.db_check_table(table_name)
    
    def __recreate_table(self, table_name):
        go_for_new = False
        if self.db_check_table(table_name):
            if self.db_drop_table(table_name):
                go_for_new = True
        else:
            go_for_new = True
        
        if go_for_new:
            if self.db_add_table(table_name, self.tables[table_name][1]):
                return True
        return False
    
    
    def __on_upgrade(self, table_name, new_version, old_version=0):
        # Can eventually handle upgrades to tables without losing data
        #     by making use of the version numbers
        # For now just destroy and recreate the tables
        # Skipping the projects table to retain info
        
        if table_name == 'mail':
            return self.__recreate_table('mail')
        
        elif table_name == 'projects':
            if self.db_check_table('projects'):
                print(".. Attempt to upgrade/recreate Projects table. Ignored to preserve info until upgrade possible")
                return True  # cheaty
            else:
                return self.__recreate_table('projects')
        
        elif table_name == 'users':
            return self.__recreate_table('users')
        
        elif table_name == 'logs':
            return self.__recreate_table('logs')
        
        else:
            print("Unsupported table: %s. Add to db.tables and db.__on_upgrade to deploy")
            return False
        
        
if __name__ == "__main__":
    pass
