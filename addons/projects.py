from core import ircBot, AddonBase
from db import DB
import os,binascii
import ircHelpers

import re

@ircBot.registerAddon()
class Projects(AddonBase):
    def __init__(self):
        self.commandList = { "projects" : self.list_projects, "addproject" : self.add_projects, "delproject" : self.delete_projects }

    def list_projects(self, arguments, messageInfo):
        if not DB().db_check_table("projects"):
            DB().db_add_table("projects", "name text, language text, description text, id text")
        data = DB().db_get_all_data("projects")
        if len(data) == 0:
            ircHelpers.privateMessage(messageInfo["user"], "There are no listed projects")
        else:
            for tuple in data:
                ircHelpers.privateMessage(messageInfo["user"], "[%s] %s - %s. id: %s" % (tuple[1], tuple[0], tuple[2], tuple[3]))

    def add_projects(self, arguments, messageInfo):
        message = arguments.split(" ")
        name = message[0]
        language = message[1]
        message.pop(0)
        message.pop(0)
        description = ' '.join(message)
        id = binascii.b2a_hex(os.urandom(3)).decode()
        dict = { "name" : name, "language" : language, "description" : description.strip("\r"), "id" : id }
        DB().db_add_data("projects", dict)
        ircHelpers.privateMessage(messageInfo["user"], "added project %s" % name)

    def delete_projects(self, arguments, messageInfo):
        DB().db_delete_data("projects", "id", arguments.strip('\r'))
        ircHelpers.privateMessage(messageInfo["user"], "Deleted project (if available)")
