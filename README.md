IRC-Bot
=======
progether IRC bot


Usage
-----------

**Mail**

To send a mail message:

   !!mail <user> <message>

To view messages:

   !!mymail

To del message:

   !!delmail <id>

All commands can also be performed as private messages like this:

   /msg progether !!mymail

All interactions are encouraged to be done through private messages.

Helping Out
-----------

 1. Create an issue (optional)
 1. Fork the codebase
 1. Create a branch

      git branch <branchName>
      git checkout <branchName>

 1. Make your changes
 1. Write tests (optional)
 1. Make a pull request between your branch and the Hawk554's master

Todo
-----------

 1. in-channel mail
 1. chat logs
 1. pow command


Changelog
-----------
Nov12

 1. fixed IsJoin functionality (my mistake)
 1. implemented mail method
 1. added db_get_data to db.py

Nov11

 1. cleaned up code, removed unecessary bits
 1. removed quit method (useless with heroku auto-up)
 1. fixed ascii bug
 1. added postgres support 

Nov10

 1. fix for join message
 1. changed speak to relay and added speak

Nov09

 1. Converted to python3
 1. cleaned up for new start
