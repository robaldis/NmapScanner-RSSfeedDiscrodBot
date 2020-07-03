# bot.py
import os
import random
import json
import asyncio

import feedparser
import time

import pyjokes
from pyinsults import insults

from discord.ext import commands
import discord
from dotenv import load_dotenv

import nmap

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

nm = nmap.PortScanner()

bot = commands.Bot(command_prefix='!')

# create the rss feed array
# if there is a file for the array populate the array, if not file then do nothing
# the file will get created when an rss feed is made
try:
    with open('rss_feeds.json', 'r') as rss_file:
        rss_feeds = json.load(rss_file)
        rss_file.close() 
except FileNotFoundError:
    print('no file was found, file will be created when you make an rss feed')
    rss_feeds = []


@bot.event
async def on_ready():
    print(f'{bot.user} is connected')
    await rss_feed()


@bot.command(name='nmap', help='Makes an nmap scan')
async def nmpaScan(ctx, ip_addr):
    print("starting nmap response")
    scanner = nmap.PortScanner()
    
    response = ''

    scanner.scan(ip_addr)
    # run a loop to print all the found result about the ports
    for host in scanner.all_hosts():
        response += ('Host : %s (%s)\n' % (host, scanner[host].hostname()))
        response += ('State : %s\n' % scanner[host].state())
        for proto in scanner[host].all_protocols():
            response += ('----------\n')
            response += ('Protocol : %s\n' % proto)
 
            lport = scanner[host][proto].keys()
            for port in lport:
                response += (f'port : {port}\tname : {scanner[host][proto][port]["name"]}\n')
    await ctx.send(f'```{response}```')
    print('Nmap scan done!')


@bot.command(name='joke', help='tells a random joke')
async def joke(ctx):
    await ctx.send(pyjokes.get_joke())
    print('Telling a joke')




@bot.command(name='insult', help='tells a random insult')
async def insult(ctx):
    await ctx.send(insults.long_insult())
    print('Telling an insult')


@bot.command(name='members', help='Shows how many members on in the server') # 
async def members(ctx):
    users = 0
    bots = 0
    for member in ctx.channel.members:
        if member.bot:
            bots += 1
        else:
            users += 1
    await ctx.send(f'there are {users} members and {bots} bots in the server')
    print('members count')



@bot.command(name="create_rss_feed", help="creates an rss feed with (FEED_NAME, FEED_CHANNEL, FEED_URL)")
async def create_rss_feed(ctx,name,channel,url):
#   rss feed object structure
#-----------------------------------------------------------------
#   {
#       "name"  :   "FEED_NAME",
#       "channel"   :   "FEED_CHANNEL",
#       "url"   :   "FEED_URL",
#       "time"  :   "time of last post/when its created whatever comes first"
#   }
#------------------------------------------------------------------
    # create the rss_feed object with all the infromation needed
    rss_feed={
        "name" : name,
        "channel" : channel,
        "url" : url,
        "time" : time.strftime ("%s",time.localtime())
    }
    # add to the array of rss feeds
    rss_feeds.append(rss_feed)
    # save the rss_feed object to a json file
    # if there is no file create one
    rss_save()

    await ctx.send("RSS feed created succesfully!")

@bot.command(name="rss_update", help="updates the rss feed that you want(name , ID, value)")
async def rss_update(ctx, name, id, value):
    success = ''
    if len(rss_feeds) == 0:
        success = 'no_feed'
    # find the rss object by name
    # update the id specified
    for rss_feed in rss_feeds:
        if (rss_feed['name'] == name):
            if (id == 'name'):
                rss_feed['name'] = value
                success = 'done'
            elif (id == 'channel'):
                rss_feed['channel'] = value
                success = 'done'
            elif (id == 'url'):
                rss_feed['url'] = value
                success = 'done'
            else:
                #responsd with you a big dumb
                success = 'id'

    
    if success == 'done':
        await ctx.send('ID updated sucessfully')
        rss_save()
    elif success == '':
        await ctx.send(f'There is no feed with the name {name}')
    elif success == 'id':
        await ctx.send('ID is not apart of the rss feed')
    elif success == 'no_feed':
        await ctx.send('You do not have any feeds at the moment, run !create_rss_feed to create one')



@bot.command(name='rss_feeds', help='shows all the rss feed names that are currecntly saved')
async def rss_feed_names (ctx):
    response = 'These are the rss feeds currently in use:\n'
    for rss_feed in rss_feeds:
        response = response + f'- {rss_feed["name"]} \n'
    await ctx.send(response)

@bot.command(name='rss_delete', help='Deletes the rss feed give it a name and it will delete that feed')
async def rss_delete(ctx, name):
    delete = False
    for rss_feed in rss_feeds:
        if rss_feed['name'] == name:
            deleted = True
            # splice that rss_feed out of the array and save the array again.
            rss_feeds.remove(rss_feed)
        rss_save()
    if deleted:
        await ctx.send("feed has been delted")
    else:
        await ctx.send("feed could not be deleted")

async def rss_feed():
    twodays = 86400/24
    posted = False
    while True:
        for rss_feed in rss_feeds:
            # parse the url to get the results
            feed = feedparser.parse(rss_feed['url'])
            items = []
            for newsitem in feed['items']:
                # time of the post
                t = newsitem['published_parsed']
                item = {
                    'title': '',
                    'date':   '',
                    'url':    ''
                }
                if int(rss_feed['time']) < time.mktime(t):
                    

                    try:
                        channel = discord.utils.find(lambda c: c.name == rss_feed['channel'], bot.get_all_channels())
                        # find the right channel for the post
                        await channel.send(newsitem['links'][0]['href'])
                        posted = True
                        

                    except AttributeError:
                        # the channel has not been found
                        print ("No channel found. make sure the name of the channel is in your server")
            if posted:
                rss_feed['time'] = time.strftime ("%s",time.localtime())
                # Save the file
                rss_save()
            
        await asyncio.sleep(10)


def rss_save():
    with open('rss_feeds.json', 'w+') as rss_file:
        rss_file.seek(0)
        rss_file.write(json.dumps(rss_feeds))
        rss_file.close()


bot.run(TOKEN)