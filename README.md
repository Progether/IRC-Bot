Progether IRC-Bot
=======
The progether IRC bot was written by the subreddit community /r/progether and is still in progress.
Our bot is currently up on heroku.

It is currently one of the active Python programming projects as well.
For information you can visit the community http://www.reddit.com/r/progether/


Usage
-----------
Most commands should be used while messaging the bot, so you don't flood the channel

Note: To list all commands after messaging the bot, simply type "!!help commands"

This can be done by typing "/msg progether !!help"
	This will send a message to the bot ,and it will message you.

 Commands

**Mailbox** - A simple user to user mail service within IRC.

To view all commands for mailbox simply type "!!help mailbox"

	 Mailbox Commands

  !!mail :: !!mail [user] [message] :: Send a message to the specified user

  !!delmail :: !!delmail [id] :: Delete an old message with ID. Use !!mymail to see IDs

  !!mymail :: !!mymail :: Check your mailbox. Use to get ID for deleting mail too

**Info** - Makes the bot post information for the channel

To view all commands for mailbox simply type "!!help info"

	 Info Commands

  !!irc :: server: irc.freenode.net, channel: #reddit-progether

  !!reddit :: http://reddit.com/r/progether/

  !!nick :: gives information on a Nick

  !!wiki :: http://www.reddit.com/r/progether/wiki/index

**Projects**

To view all commands for projects simply type "!!help projects"

	 Project Commands

  !!projects :: No description found

  !!addproject :: Adds a project to the listing

  !!delproject :: Deletes a project from the listing

  !!projects :: Lists all active projects,id's, and repository links.

**Speak** - Commands to make the bot say something in channel

To view all commands for speak simply type "!!help speak"

	 Speak Commands

  !!speak :: No description found

  !!say :: Says typed text into channel

  !!relay :: No help found.

**Chatlog** - Commands to review previous messages

To view all commands for Chatlog simply type "!!help chatlog"

	 Chatlog Commands

  !!lastlog :: Says the last user's message in channel

  !!readlog :: Prints out the last chat log to a certain line amount ie: !!lastlog50

 **Helper** - Get help on the bot's functionality

 	 Helper Commands

  !!aid :: !!aid [user] [help arguments] :: Send help to another user. Usage is the same as for !!help.


 - Helping Out -
-----------

 1. Create an issue (optional)
 1. Fork the codebase
 1. Create a branch

      git branch <branchName>
      git checkout <branchName>

 1. Make your changes
 1. Write tests (optional)
 1. Make a pull request between your branch and the Hawk554's master
