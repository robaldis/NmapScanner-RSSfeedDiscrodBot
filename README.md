# NmapScanner-RSSfeedDiscordBot


install all the requirements
simply run `pip install -r requirements.txt`


connecting the code to the discord dev console
1. Discord developer portal - You will need to make sure that you have a discord bot on the discord developer portal at https://discord.com/developers/applications
    - first click new application in the top right and name it whatever you want
    - to create the bot click on "Bot" on the left hand side and then "Add Bot"
    - to give the bot privilages go to "OAuth2" and in scopes click on bot and in text permissions click on "Send Messages" and "view Channels"
    - copy the URL above that and paste it into your browser
    - you can now select the server that you would like the bot to be in
2. Connecting the code - For connecting the code you will need to make a .env file and put your token in there.
this is the safiest way to do it as you dont want just anyone to have access to that token
    - going back to the bot menu the token will be under the name and next to the image copy that and past it into an .env file like this:
    DISCORD_TOKEN={TOKEN PASTED IN HERE AS A STRING}

You should have the discord bot connected!