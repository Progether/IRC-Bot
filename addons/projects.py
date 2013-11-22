from core import ircBot, AddonBase
from db import DB
import os,binascii
import ircHelpers

import re

@ircBot.registerAddon()
class Projects(AddonBase):
    def __init__(self):
        ##TODO verify table exists
        self.commandList = { "projects" : self.list_projects, "addproject" : self.add_projects, "delproject" : self.delete_projects }

    def list_projects(self, arguments, messageInfo):
        user = messageInfo['user']
        if not DB().db_check_table("projects"):
            DB().db_add_table("projects", "name text, language text, link text, description text, id text")
        if (arguments):
            data = DB().db_get_data("projects", "language", arguments.replace('\r',''))
        else:
            data = DB().db_get_all_data("projects")
        if data == None:
            ircHelpers.pmInChannel(user, "Error while trying to retrieve Projects")
        if len(data) == 0:
            ircHelpers.pmInChannel(user, "There are no listed projects")
        else:
            max_name = len("name")
            max_lang = len("language")
            max_desc = len("description")
            max_link = 0
            for proj_tuple in data:
                if len(proj_tuple[1]) > max_lang:
                    max_lang = len(proj_tuple[1])
                if len(proj_tuple[0]) > max_name:
                    max_name = len(proj_tuple[0])
                if len(proj_tuple[3]) > max_desc:
                    max_desc = len(proj_tuple[3])
                if len(proj_tuple[2]) > max_link:
                    max_link = len(proj_tuple[2])
            title_row = "(%s)  %s [[ %s ]]  %s  (( %s ))" %(
                                     "  id  ",
                                     "language".ljust(max_lang),
                                     "name".ljust(max_name),
                                     "description".ljust(max_desc),
                                     "   link".ljust(max_link))
            
            ircHelpers.sayInChannel(title_row)
            ircHelpers.sayInChannel('-'*len(title_row))
            
            for proj_tuple in data:
                ircHelpers.sayInChannel(
                                       #(id) lang [[ name ]]  desc  << link >>
                                       "(%s)  %s [[ %s ]]  %s  (( %s ))"
                                       % (proj_tuple[4],                  # id
                                          proj_tuple[1].ljust(max_lang),  # lang
                                          proj_tuple[0].ljust(max_name),  # name
                                          proj_tuple[3].ljust(max_desc),  # desc
                                          proj_tuple[2].ljust(max_link))) # link

    def add_projects(self, arguments, messageInfo):
        message = arguments.split(" ")
        try:
            name = message[0]
            language = message[1]
            link = message[2]
            message.pop(0)
            message.pop(0)
            message.pop(0)
            description = ' '.join(message)
        except IndexError:
            ircHelpers.pmInChannel(messageInfo['user'], "Correct usage is: !!addproject [name] [language] [link] [description]")
            return False
        
        proj_id = binascii.b2a_hex(os.urandom(3)).decode()
        proj_dict = { "name" : name, "language" : language, "link" : link, "description" : description.strip("\r"), "id" : proj_id }
        if DB().db_add_data("projects", proj_dict):
            ircHelpers.pmInChannel(messageInfo['user'], "Added project %s. Thank's for taking part!" % name)
            ircHelpers.sayInChannel("Added new project: %s" % name)
        else:
            ircHelpers.pmInChannel("Error trying to add project %s" % name)

    def delete_projects(self, arguments, messageInfo):
        if not arguments.strip('\r').strip():
            ircHelpers.pmInChannel(messageInfo['user'], "Correct usage is: !!delproject [project_id]")
            return False
        if DB().db_delete_data("projects", "id", arguments.strip('\r')):
            ircHelpers.sayInChannel("Deleted project (if available)")
            return True
        else:
            ircHelpers.sayInChannel("Error trying to delete project")
            return False
