from core import ircBot, AddonBase
from db import DB
import os,binascii
import ircHelpers


@ircBot.registerAddon()
class Mail(AddonBase):
    prefix = ircBot.command_prefix
    
    # All command groups should have a 'help_description' that explains the addon package. Help will take care of listing the commands.
    help_description = ["An IRC postal service",]
    # Each command should have a help message to desc its usage. Register and assign help to command in 'self.helplist{}'
    help_check  = ["%smymail :: Check your mailbox. Use to get ID for deleting mail too" % prefix,"test 2nd line prints"]
    help_send   = ["%smail [user] [message] :: Send a message to the specified user" % prefix,]
    help_delete = ["%sdelmail [id] :: Delete an old message with ID. Use %smymail to see IDs" % (prefix, prefix),]
    
    def __init__(self):
        ##TODO verify table exists
        self.title = "mailbox"
        self.commandList = {"mail" : self.send_mail, "mymail" : self.get_mail,   "delmail" : self.delete_mail }
        self.helpList    = {'mail' : self.help_send, 'mymail' : self.help_check, "delmail" : self.help_delete }
        self.joinList = [self.notify]

    def send_mail(self, arguments, messageInfo):
        sender = messageInfo['user']
        message = arguments.split(" ", 1)
        try:
            recipient = message[0]
            message = message[1]
        except IndexError:
            ircHelpers.pmInChannel(sender, Mail.help_send)
            return False
        mail_id = binascii.b2a_hex(os.urandom(3)).decode()
        mail_dict = { "sender" : sender, "recipient" : recipient, "message" : message.strip("\r"), "id" : mail_id }
        if DB().db_add_data("mail", mail_dict):
            ircHelpers.pmInChannel(sender, "sent message to %s: %s" % (recipient, message.strip("\r")))
            return True
        else:
            ircHelpers.pmInChannel(sender, "Failed to send message to %s" % recipient)
            return False

    def get_mail(self, arguments, messageInfo):
        recipient = messageInfo["user"]
        data = DB().db_get_data("mail", "recipient", recipient)
        if data == None:
            ircHelpers.pmInChannel(messageInfo["user"], "Error retrieving mail")
            return False
        elif len(data) == 0:
            ircHelpers.pmInChannel(messageInfo["user"], "You have no messages")
            return True
        else:
            for mail_tuple in data:
                ircHelpers.privateMessage(mail_tuple[1], "[ %s ] <%s>: %s" % (mail_tuple[3],mail_tuple[0],mail_tuple[2]))
            return True

    def delete_mail(self, arguments, messageInfo):
        if DB().db_delete_data("mail","id",arguments.strip('\r')):
            ircHelpers.pmInChannel(messageInfo["user"], "Deleted message (if available)")
            return True
        else:
            ircHelpers.pmInChannel(messageInfo["user"], "Error while deleting message")
            return False
        
    def notify(self, user):
        data = DB().db_get_data("mail", "recipient", user)
        if data == None:
            print("!! Error attempting to notify user of mail.")
            return False
        elif len(data) != 0:
            ircHelpers.pmInChannel(user, "You have mail! You can check it with mymail and delete it with delmail <id>")
            return True
