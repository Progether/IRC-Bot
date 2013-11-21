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
        if not DB().db_check_table("projects"):
            DB().db_add_table("projects", "name text, language text, link text, description text, id text")
        if (arguments):
            data = DB().db_get_data("projects", "language", arguments.replace('\r',''))
        else:
            data = DB().db_get_all_data("projects")
        if data == None:
            ircHelpers.pmInChannel(messageInfo["user"], "Error while trying to retrieve Projects")
        if len(data) == 0:
            ircHelpers.pmInChannel(messageInfo["user"], "There are no listed projects")
        else:
            for proj_tuple in data:
                ircHelpers.pmInChannel(messageInfo["user"], "[%s] %s - %s. link: %s.id: %s" % (proj_tuple[1], proj_tuple[0], proj_tuple[3], proj_tuple[2], proj_tuple[4]))

    def add_projects(self, arguments, messageInfo):
        message = arguments.split(" ")
        name = message[0]
        language = message[1]
        link = message[2]
        message.pop(0)
        message.pop(0)
        message.pop(0)
        description = ' '.join(message)
        proj_id = binascii.b2a_hex(os.urandom(3)).decode()
        proj_dict = { "name" : name, "language" : language, "link" : link, "description" : description.strip("\r"), "id" : proj_id }
        if DB().db_add_data("projects", proj_dict):
            ircHelpers.sayInChannel("added project %s" % name)
        else:
            ircHelpers.pmInChannel("Error trying to add project %s" % name)

    def delete_projects(self, arguments, messageInfo):
        if DB().db_delete_data("projects", "id", arguments.strip('\r')):
            ircHelpers.sayInChannel("Deleted project (if available)")
        else:
            ircHelpers.sayInChannel("Error trying to delete project")
