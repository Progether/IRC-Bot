from core import ircBot, AddonBase
from db import DB
import ircHelpers

@ircBot.registerAddon()
class DataBaseTest(AddonBase):
  def __init__(self):
    self.commandList = { "create_test_table" : self.create_test_table, "add_test_data_to_table" : self.add_data_to_table, "drop_test_table" : self.drop_table, "delete_test_data" : self.delete_data, "update_test_data" : self.update_data }

  def create_test_table(self, arguments, messageInfo):
    # table name, column name and column type
    DB().db_add_table("test", "name text, details text")
    ircHelpers.sayInChannel("Created table")

  def add_data_to_table(self, arguments, messageInfo):
    dict = { "name" : "test1", "details" : "sample_details" }
    # table_name, dict of column name and column value
    DB().db_add_data("test", dict)
    ircHelpers.sayInChannel("Wrote data to table")
    
  def drop_table(self, arguments, messageInfo):
    # table_name
    DB().db_drop_table("test")
    ircHelpers.sayInChannel("Dropped table")
  
  def delete_data(self, arguments, messageInfo):
    # table_name, name of column to determine deletion, column value, type of condition to match (= or LIKE)
    # makes DELETE FROM test where name = 'test1'
    DB().db_delete_data("test","name","test1")
    ircHelpers.sayInChannel("Deleted data")

  def update_data(self, arguments, messageInfo):
    # table_name, name of column to change, column value, name of column to determine change, column value, = or LIKE
    # makes UPDATE test SET name = 'test2' WHERE name = 'test1'
    DB().db_update_data("test","name","test2","name","test1")
    ircHelpers.sayInChannel("Updated data")
