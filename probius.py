#A HotS Discord bot
#Call in Discord with [hero/modifier]
#Modifier is hotkey or talent tier
#Data is pulled from HotS wiki
#Project started on 14/9-2019

import discord
import asyncio
import io
import aiohttp
import re
import random

from aliases import *			#Spellcheck and alternate names for heroes
from trimBrackets import *		#Trims < from text
from printFunctions import *	#The functions that output the things to print
from heroPage import *			#The function that imports the hero pages
from emojis import *			#Emojis
from miscFunctions import*		#Edge cases and help message
from getDiscordToken import *	#The token is in an untracked file because this is a public Github repo
from builds import *			#Hero builds
from rotation import *			#Weekly rotation
from quotes import *			#Lock-in quotes
from draft import *
from pokedex import *

async def mainProbius(client,message,texts):
	buildsAliases=['guide','build','b','g','builds','guides']
	quotesAliases=['quote','q','quotes']
	rotationAlises=['rotation','rot','r']
	aliasesAliases=['aliases','names','acronyms','a','n']
	wikipageAliases=['all','page','wiki']
	randomAliases=['random','ra','rand']
	draftAliases=['draft','d','phantomdraft','pd','mockdraft','md']
	colourAliases=['colour','colours','c','colors','color']
	heroStatsAliases=['stats','info']
	pokedexAliases=['pokedex','main','mains','p','m']
	for i in draftAliases: #Don't want to log draft commands because they really spam.
		if '['+i+'/' in message.content.lower():
			break
	else:#The elusive for else control flow
		loggingMessage=message.channel.guild.name+' '*(15-len(message.channel.guild.name))+message.channel.name+' '+' '*(17-len(message.channel.name))+str(message.author)+' '*(18-len(str(message.author)))+' '+message.content
		print(loggingMessage)
		await client.get_channel(643231901452337192).send('`'+loggingMessage+'`')

	for text in texts:
		hero=text[0]
		if hero in pokedexAliases:
			await pokedex(client,message.channel,aliases(text[1]))
			continue
		if hero==':summon':
			await message.channel.send('༼ つ ◕_◕ ༽つ')
			continue
		if hero in colourAliases:
			await message.channel.send(file=discord.File('WS colours.png'))
			continue
		if message.author.id==183240974347141120:
			if hero=='serverchannels':
				await message.channel.send([channel.name for channel in message.channel.guild.channels])
				continue
		if hero== 'unsorted' and message.channel.guild.name=='Wind Striders':
			if 557521663894224912 in [role.id for role in message.author.roles]:#Olympian
				channel = client.get_channel(557366982471581718)#WSgeneral
				role=channel.guild.get_role(560435022427848705)#UNSORTED
				rulesChannel=channel.guild.get_channel(634012658625937408)#server-rules
				await message.channel.send('Note to all '+role.mention+': Please read '+rulesChannel.mention+' and ping **Olympian(mod)** with the **bolded** info at top **(`Region`, `Rank`, and `Preferred Colour`)** to get sorted before Blackstorm purges you <:peepoLove:606862963478888449>')
				continue
		if hero == 'vote':
			await message.add_reaction('\U0001f44d')
			await message.add_reaction('\U0001f44e')
			continue
		if hero in ['coin','flip','coinflip','cf']:
			await message.channel.send(random.choice(['Heads','Tails']))
			continue
		if hero in ['reddit','re']:
			if len(text)==2:
				cutoff=-int(text[1])
			else:
				cutoff=0
			output='Recent Reddit posts by Wind Striders:\n'
			for i in client.forwardedPosts[cutoff:]:
				output+='**'+i[0]+'** by '+i[1]+': <'+i[2]+'>\n'
			await printLarge(message.channel,output)
			continue
		if hero == 'avatar':
			await client.getAvatar(message.channel,text[1])
			continue
		if hero=='':#Empty string. Aliases returns Abathur when given this.
			continue
		if hero in draftAliases:
			await draft(client,message.channel,text)
			continue
		if hero in randomAliases:
			hero=random.choice(getHeroes())
		if hero in ['help','info']:
			await message.channel.send(helpMessage())
			continue
		if hero in buildsAliases:
			if len(text)==2:
				await guide(aliases(text[1]),message.channel)
			else:
				await message.channel.send("Elitesparkle's builds: <https://elitesparkle.wixsite.com/hots-builds>")
			continue
		if hero in rotationAlises:
			await rotation(message.channel)
			continue
		if hero=='good bot':
			await emoji(client,['Probius','love'],message.channel)
			continue
		if hero=='bad bot':
			await emoji(client,['Probius','sad'],message.channel)
			continue
		if ':' in hero:
			await emoji(client,text,message.channel,message)
			continue
		if ']' in hero:
			continue
		if hero in ['chogall',"cho'gall",'cg','cho gall','cho-gall']:
			await message.channel.send("Cho and Gall are 2 different heroes. Choose one of them")
			print('Dual hero')
			continue
		if hero in quotesAliases:
			if len(text)==2:
				await message.channel.send(getQuote(aliases(text[1])))
			else:
				await message.channel.send('All hero select quotes: <https://github.com/Asddsa76/Probius/blob/master/quotes.txt>')
			continue
		if hero in aliasesAliases:
			await message.channel.send('All hero alternate names: <https://github.com/Asddsa76/Probius/blob/master/aliases.py>')
			continue
		if hero == 'all':
			await printAll(message,text[1])
			continue
		if hero in ['emoji','emojis','emote','emotes']:
			await message.channel.send('Emojis: [:hero/emotion], where emotion is of the following: happy, lol, sad, silly, meh, angry, cool, oops, love, or wow.')
			continue
		#From here it's actual heroes
		if len(hero)==1:#Patch notes have abilities in []. Don't want spammed triggers again
			continue
		hero=aliases(hero)
		if len(text)==2:#If user switches to hero first, then build/quote
			if text[1] in buildsAliases:
				await guide(hero,message.channel)
				continue
			if text[1] in quotesAliases and text[1]!='q':
				await message.channel.send(getQuote(hero))
				continue
			if text[1] in heroStatsAliases:
				await heroStats(hero,message.channel)
				continue

		[abilities,talents]=heroAbilitiesAndTalents(hero)
		abilities=extraD(abilities,hero)
		if abilities==404:
			try:#If no results, then "hero" isn't a hero
				await printAll(message,text[0])
			except:
				pass
			continue
		
		output=''
		try:
			tier=text[1]#If there is no identifier, then it throws exception
			if tier in randomAliases:
				await message.channel.send(printTier(talents,random.randint(0,6)))
				return
		except:
			quote=getQuote(hero)
			output=printAbilities(abilities)
			if len(output)!=2:
				output=quote+output
			else:
				output[0]=quote+output[0]
		if output=='':
			if tier.isdigit():#Talent tier
				tier=int(tier)
				output=printTier(talents,int(tier/3)+int(hero=='Chromie' and tier not in [1,18]))#Talents for Chromie come 2 lvls sooner, except lvl 1
			elif tier in ['mount','z']:
				output=abilities[-1]#Last ability. It's heroic if the hero has normal mount, but that's an user error
			elif tier=='extra':
				if hero in ['Zeratul','Gazlowe','Nova','Whitemane']:#Some heroes have the entry for 1 button between D and Q, these have them last
					output=abilities[-1]
				elif hero=='Gall':#Gall has extra and a special mount
					output=abilities[-2]
				elif hero=='Stitches':#Hook is after Q
					output=abilities[2]
				else:
					output=abilities[1]
			elif tier=='r':#Ultimate
				if hero=='Tracer':#She starts with her heroic already unlocked, and only has 1 heroic
					output=abilities[4]
				else:
					output=printTier(talents,3-2*int(hero=='Varian'))#Varian's heroics are at lvl 4
			elif len(tier)==1 and tier in 'dqwe':#Ability (dqwe)
				output=printAbility(abilities,tier)
			elif tier=='trait':
				output=printAbility(abilities,'d')
			elif tier in wikipageAliases:#Linking user to wiki instead of printing everything
				await message.channel.send('<https://heroesofthestorm.gamepedia.com/Data:'+hero+'#Skills>')
				continue
			else:
				tier=abilityAliases(hero,tier)
				output=printSearch(abilities, talents, tier, hero)
		
		if len(output)==2:#If len is 2, then it's an array with output split in half
			if message.channel.name=='rage':
				await message.channel.send(output[0].upper())
				await message.channel.send(output[1].upper())
			else:
				await message.channel.send(output[0])
				await message.channel.send(output[1])
		else:
			if message.channel.name=='rage':
				output=output.upper()
			try:
				await message.channel.send(output)
			except:
				if output=='':
					try:#If no results, it's probably an emoji with : forgotten. Prefer to call with : to avoid loading abilities and talents page
						await emoji(client,[hero,tier],message.channel)
						continue
					except:
						pass
					if message.channel.name=='rage':
						await message.channel.send('ERROR: '+hero.upper()+' DOES NOT HAVE "'+tier.upper()+'".')
					else:
						await message.channel.send('Error: '+hero+' does not have "'+tier+'".')
					print('No results')
				else:
					if message.channel.name=='rage':
						await message.channel.send("ERROR: EXCEEDED DISCORD'S 2000 CHARACTER LIMIT. BE MORE SPECIFIC")
					else:
						await message.channel.send("Error: exceeded Discord's 2000 character limit. Be more specific")
					print('2000 limit')

async def welcome(member):
	guild=member.guild
	if guild.name=='Wind Striders':
		print(member.name+' joined')
		channel=guild.get_channel(557366982471581718)#general
		rulesChannel=guild.get_channel(634012658625937408)#server-rules
		await channel.send('Welcome '+member.mention+'! Please read '+rulesChannel.mention+' and ping **Olympian(mod)** with the **bolded** info at top **(`Region`, `Rank`, and `Preferred Colour`)** to get sorted <:peepoLove:606862963478888449>')
		await member.add_roles(guild.get_role(560435022427848705))#UNSORTED role

def findTexts(message):
	text=message.content.lower()
	leftBrackets=[1+m.start() for m in re.finditer('\[',text)]#Must escape brackets when using regex
	rightBrackets=[m.start() for m in re.finditer('\]',text)]
	texts=[text[leftBrackets[i]:rightBrackets[i]].split('/') for i in range(len(leftBrackets))]
	return texts

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def getPostInfo(post):
	title=post.split('", "')[0]
	post=post.split('"author": "')[1]
	author=post.split('"')[0]
	post=post.split('"permalink": "')[1]
	shortUrl=post.split('"')[0]
	url='https://old.reddit.com'+shortUrl
	return [title,author,url]

class MyClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.seenTitles=[]
		self.forwardedPosts=[]
		self.drafts={}
		self.proxyEmojis={}
		self.pokedex=''
		self.RedditWS=['Asddsa76', 'Blackstar_9', 'Spazzo965', 'SomeoneNew666', 'joshguillen', 'SotheBee', 'AnemoneMeer', 'jdelrioc', 'Pscythic', 'Elitesparkle', 'slapperoni', 
		'secret3332', 'Carrygan_', 'Archlichofthestorm', 'Gnueless', 'ThatDoomedStudent', 'InfiniteEarth', 'SamiSha_', 'twinklesunnysun', 'zanehyde', 'Pelaberus', 'KillMeWithMemes', 
		'ridleyfire','bran76765','MarvellousBee','Naturage','derenash','Riokaii','D0ctorLogan','Demon_Ryu','hellobgs','Beg_For_Mercy']
		# create the background task and run it in the background
		self.bgTask0 = self.loop.create_task(self.bgTaskSubredditForwarding())
		self.bgTask1 = self.loop.create_task(self.bgTaskUNSORTED())

	async def fillPokedex(self):
		pokedexChannel=client.get_channel(597140352411107328)
		self.pokedex=((await pokedexChannel.fetch_message(597433561112641536)).content+'\n'+(await pokedexChannel.fetch_message(620339772833136640)).content+'\n').replace(':','')

	async def fillPreviousPostTitles(self):
		await self.wait_until_ready()
		async with aiohttp.ClientSession() as session:
			page = await fetch(session, 'https://old.reddit.com/r/heroesofthestorm/new.api?limit=100&sort=new')
			posts=page.split('"clicked": false, "title": "')[1:]
			output=[]
			for post in posts:
				[title,author,url] = await getPostInfo(post)#Newest post that has been checked
				output.append(title)
				if author in self.RedditWS:
					title=title.replace('&amp;','&').replace('\u2013','-').replace('\u0336','')
					self.forwardedPosts.append([title,author,url])
			self.forwardedPosts=self.forwardedPosts[::-1]
			return output

	async def on_ready(self):
		print('Logged on as', self.user)
		self.seenTitles=await self.fillPreviousPostTitles()		#Fills seenTitles with all current titles
		self.proxyEmojis=await getProxyEmojis(client.get_guild(603924426769170433))
		await self.fillPokedex()

	async def on_message(self, message):
		#Don't respond to ourselves
		if message.author == self.user:
			return
		ignoredUsers=['Rick Astley','PogChamp',"Swann's Helper"]
		if message.author.name in ignoredUsers:
			return
		if '[' in message.content and ']' in message.content:
			texts=findTexts(message)
			await mainProbius(self,message,texts)
		elif '[' in message.content:
			await mainProbius(self,message,[message.content.split('[')[1].lower().split('/')])
		
	async def on_message_edit(self,before, after):
		if '[' in after.content and ']' in after.content:
			try:
				beforeTexts=findTexts(before)
			except:
				beforeTexts=[]
			newTexts=[i for i in findTexts(after) if i not in beforeTexts]
			if newTexts:#Nonempty lists have boolean value true
				await mainProbius(self,after,newTexts)

	async def on_raw_reaction_add(self,payload):
		member=client.get_user(payload.user_id)
		if member.id==603924594956435491:#Probius did reaction
			return

		message=await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
		if message.author.id==603924594956435491 and str(payload.emoji)=='👎':#Message is from Probius, and is downvoted with thumbs down
			output=member.name+' deleted a message from Probius'
			print(output)
			await client.get_channel(643231901452337192).send('`'+output+'`')
			await message.delete()
			return
		elif message.author.id==603924594956435491 and 'React to ping' in message.content:#Message from Probius, pings Pokedex:
			output=member.name+' started a balance discussion'
			print(output)
			await client.get_channel(643231901452337192).send('`'+output+'`')
			await pingPokedex(self,message,member)
			return

		if member.name=='Asddsa76':#Reaction copying
			await message.add_reaction(payload.emoji)

		if payload.channel_id==643972679132774410:#ZH Mockdrafting-role
			await client.get_guild(623202246062243861).get_member(payload.user_id).add_roles(client.get_guild(623202246062243861).get_role(643975988023394324))

	async def on_raw_reaction_remove(self,payload):
		member=client.get_user(payload.user_id)
		if payload.channel_id==643972679132774410:#ZH Mockdrafting-role
			await client.get_guild(623202246062243861).get_member(payload.user_id).remove_roles(client.get_guild(623202246062243861).get_role(643975988023394324))

	async def on_member_join(self,member):
		await welcome(member)

	async def getAvatar(self,channel,userMention):
		userString=userMention.replace('\\','').replace(' ','')[2:-1].replace('!','')#\ to not ping them, space because discord makes one after mention, ! for nitro users with custom
		user=self.get_user(int(userString))
		await channel.send(user.avatar_url)

	async def bgTaskSubredditForwarding(self):
		await self.wait_until_ready()
		channel = self.get_channel(557366982471581718)#WS general
		#channel = self.get_channel(604394753722941451)#PT general-2
		while not self.is_closed():
			await asyncio.sleep(60)#Check for new posts every minute
			async with aiohttp.ClientSession() as session:
				try:
					page = await fetch(session, 'https://old.reddit.com/r/heroesofthestorm/new.api')#Screw JSON parsing, I'll do it myself
					posts=page.split('"clicked": false, "title": "')[1:]
					for post in posts:
						[title,author,url] = await getPostInfo(post)
						if author in self.RedditWS:
							if title not in self.seenTitles:#This post hasn't been processed before
								self.seenTitles.append(title)
								title=title.replace('&amp;','&').replace('\u2013','-').replace('\u0336','')
								self.forwardedPosts.append([title,author,url])
								await channel.send('**'+title+'** by '+author+': '+url)
								await self.get_channel(643231901452337192).send('`'+title+' by '+author+'`')#log
								print(title+' by '+author)
								if author=='Gnueless':
									await rotation(channel)
				except:
					await self.get_channel(643231901452337192).send('Something went wrong with subreddit forwarding')
					print('Something went wrong with subreddit forwarding')

	async def bgTaskUNSORTED(self):
		await self.wait_until_ready()
		channel = self.get_channel(557366982471581718)#WSgeneral
		role=channel.guild.get_role(560435022427848705)#UNSORTED
		rulesChannel=channel.guild.get_channel(634012658625937408)#server-rules
		while not self.is_closed():
			await asyncio.sleep(60*60*24)#Sleep 24 hours
			await channel.send('Note to all '+role.mention+': Please read '+rulesChannel.mention+' and ping **Olympian(mod)** with the **bolded** info at top **(`Region`, `Rank`, and `Preferred Colour`)** to get sorted before Blackstorm purges you <:peepoLove:606862963478888449>')

client = MyClient()
client.run(getDiscordToken())