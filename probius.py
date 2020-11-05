#A HotS Discord bot
#Call in Discord with [hero/modifier]
#Modifier is hotkey or talent tier
#Data is pulled from HotS wiki
#Project started on 14/9-2019

import asyncio
import io
import aiohttp
import re
import random
import discord
import time
from sys import argv#Where to get the JSONs
from discord.ext import tasks
from discord.ext import commands

from aliases import *			#Spellcheck and alternate names for heroes
from printFunctions import *	#The functions that output the things to print
from heroesTalents import *		#The function that imports the hero pages
from emojis import *			#Emojis
from miscFunctions import*		#Edge cases and help message
from getProbiusToken import *	#The token is in an untracked file because this is a public Github repo
from builds import *			#Hero builds
from rotation import *			#Weekly rotation
from quotes import *			#Lock-in quotes
from draft import *
from pokedex import *
from reddit import *
from sorting import *
from patchNotes import *
from lfg import *
from maps import *

wsReactionRoles={'🇧':577935915448795137,'🇩':664126658084601857,'🇱':693038480783048774}
drafts={}#Outside of client so it doesn't reset on periodic restarts or [restart]
lastDraftMessageDict={}
draftNames={}

async def mainProbius(client,message,texts):
	if message.author.id==410481791204327424:
		pass
		#await message.channel.send('<:bongocat:740080434343444520> Unblock me '+message.author.mention+'! <:bongocat:740080434343444520>')
		#return
	buildsAliases=['guide','build','b','g','builds','guides']
	quotesAliases=['quote','q','quotes']
	rotationAlises=['rotation','rot','sale','sales']
	aliasesAliases=['aliases','names','acronyms','n']
	wikipageAliases=['all','page','wiki']
	randomAliases=['random','ra','rand']
	draftAliases=['draft','d','phantomdraft','pd','mockdraft','md']
	colourAliases=['colour','colours','c','colors','color']
	heroStatsAliases=['stats','info']
	pokedexAliases=['pokedex','main','mains','p']
	updatePokedexAliases=['updatepokedex','up']
	emojiAliases=['emoji','emojis','emote','emotes']
	coinsAliases=['coin','flip','coinflip','cf']
	redditAliases=['reddit','re']
	helpAliases=['help','info']
	talentAliases=['talent','talents']
	rollAliases=['roll','dice']
	patchNotesAliases=['patchnotes','patch','pn','pa']
	deleteAliases=['delete','deletemessages','deletemessage']
	lfgAlises=['lfg','find']
	listAliases=['list','waitlist','wl']
	mapImageAliases=['map','m','battleground','bg']
	restartAliases=['restart','shutdown','stop']
	confidenceAliases=['ci','confidence','confidenceinterval']
	heroAliases=['hero', 'heroes', 'bruiser', 'healer', 'support', 'ranged', 'melee', 'assassin', 'mage', 'marksman', 'tank', 'marksmen']
	for i in draftAliases: #Don't want to log draft commands because they really spam.
		if '['+i+'/' in message.content.lower():
			break
	else:#The elusive for else control flow
		guildname=message.channel.guild.name
		guildname='Nexus school' if guildname=='Nexus Schoolhouse' else guildname#Nexus Schoolhouse is too long 
		guildname='Schuifpui' if guildname=='De Schuifpui Schavuiten' else guildname
		channelName=message.channel.name
		channelName='hots' if channelName=='heroes-got-canceled' else channelName
		loggingMessage=guildname+' '*(15-len(guildname))+channelName+' '+' '*(17-len(channelName))+str(message.author.name)+' '*(18-len(str(message.author.name)))+' '+message.content
		print(loggingMessage)
		await client.get_channel(643231901452337192).send('`'+loggingMessage+'`')

	for text in texts:
		hero=text[0].replace(' ','')
		if hero in ['trait','r','w','e','passive','react','...']:#Do nothing
			continue
		if hero=='name':
			twinkles=[(i.name if not i.nick else i.nick)+(' ('+i.name+')')*int(bool(i.nick)) for i in message.guild.members if text[1].lower() in i.name.lower() or i.nick and text[1].lower() in i.nick.lower()]
			await message.channel.send('\n'.join(twinkles)+'\n'+str(len(twinkles))+' '+text[1].capitalize()+'s')
			continue
		if hero in heroAliases+[i+'s' for i in heroAliases]:
			await heroes(message,text,message.channel,client)
			continue
		if hero=='ping':
			await ping(message.channel)
			continue
		if hero=='membercount':
			await memberCount(message.channel)
			continue
		if hero in confidenceAliases:
			await confidence(message.channel,text)
			continue
		if hero=='exit' and message.author.id==183240974347141120:
			global exitBool
			exitBool=1
			await client.close()
		if hero in restartAliases:
			await client.logout()
		if hero in mapImageAliases:
			await mapImage(message.channel,text[1])
			continue
		if hero=='core':
			await coreAbilities(message.channel,await mapAliases(text[1]))
			continue
		if hero in listAliases:
			await waitList(message,text,client)
			continue
		if hero in lfgAlises:
			await lfg(message.channel,text[1],client)
			continue
		#if hero == 'd' and message.channel.id not in [643996299678449684,643975810256076820,643975833970540555,672921422544502952]: #[D] outside of drafting channel, trait
		#	continue
		if hero in deleteAliases:
			await deleteMessages(message.author,text[1],client)
			continue
		if hero in patchNotesAliases:
			await patchNotes(message.channel,text)
			continue
		if hero in talentAliases:
			await message.channel.send("Call a hero's talent tier with [hero/level]")
			continue
		if hero in updatePokedexAliases:
			if client.isEditingPokedex:
				await message.channel.send('Please wait, the pokedex is already being edited!')
				continue
			client.isEditingPokedex=1
			await updatePokedex(client,text,message)
			client.isEditingPokedex=0
			continue
		if hero in rollAliases:
			await roll(text,message)
			continue
		if hero=='sort':
			await sortFromMessage(text[1],message,client)
			continue
		if hero in pokedexAliases:
			await pokedex(client,message.channel,aliases(text[1]))
			continue
		if hero==':disapproval':
			await message.channel.send('ಠ_ಠ')
			continue
		if hero==':summon':
			if len(text)==1:
				await message.channel.send('༼ つ ◕\\_◕ ༽つ')
			elif '@' in text[1]:
				await message.channel.send('༼ つ ◕\_◕ ༽つ ༼ つ ◕\_◕ ༽つ'+' Summon '+message.author.mention+'! ༼ つ ◕\_◕ ༽つ ༼ つ ◕\_◕ ༽つ')
			else:
				await message.channel.send('༼ つ ◕\_◕ ༽つ ༼ つ ◕\_◕ ༽つ'+' Summon '+message.content.split('[')[1].split('/')[1].split(']')[0] +'! ༼ つ ◕\_◕ ༽つ ༼ つ ◕\_◕ ༽つ')#text[1] is all lowercase etc.
			continue
		if hero in colourAliases:
			await message.channel.send(file=discord.File('WS colours.png'))
			continue
		if message.author.id==183240974347141120:
			if hero=='serverchannels':
				await message.channel.send([channel.name for channel in message.channel.guild.channels])
				continue
			if hero=='repeat' and len(text)==2:
				await message.channel.send(text[1])
				await message.delete()
				continue
		if hero== 'unsorted' and message.channel.guild.name=='Wind Striders':
			if 557521663894224912 in [role.id for role in message.author.roles]:#Olympian
				channel = client.get_channel(557366982471581718)#WSgeneral
				role=channel.guild.get_role(560435022427848705)#UNSORTED
				rulesChannel=channel.guild.get_channel(634012658625937408)#server-rules
				await channel.send('Note to all '+role.mention+': Please read '+rulesChannel.mention+' and type here the info at top **`Region`, `Rank`, and `Preferred Colour`**, separated by commas, to get sorted before Blackstorm purges you <:OrphAYAYA:657172520092565514>')
				await channel.send(content='https://cdn.discordapp.com/attachments/576018992624435220/743917827718905896/sorting.gif',file=discord.File('WS colours.png'))
				continue
		if hero == 'vote':
			await vote(message,text)
			continue
		if hero in coinsAliases:
			await message.channel.send(random.choice(['Heads','Tails']))
			continue
		if hero in redditAliases:
			if len(text)==2:
				cutoff=-int(text[1])
			else:
				cutoff=0
			output='Recent Reddit posts:\n'
			for i in client.forwardedPosts[cutoff:]:
				author=i[1]
				if author in discordnames:
						author=discordnames[author]
				output+='**'+i[0]+'** by '+author+': <'+i[2]+'>\n'
			await printLarge(message.channel,output)
			continue
		if hero in ['avatar','a']:
			await getAvatar(client,message.channel,text[1])
			continue
		if hero=='':#Empty string. Aliases returns Abathur when given this.
			continue
		if hero in draftAliases:
			await draft(drafts,message.channel,message.author,text,lastDraftMessageDict,draftNames)
			continue
		if hero in randomAliases:
			if len(text)==1:
				await message.channel.send(getQuote(random.choice(getHeroes())))
				continue
			hero=random.choice(getHeroes())
		if hero in helpAliases:
			if len(text)==2 and hero in heroStatsAliases:#[info/hero]
				await heroStats(aliases(text[1]),message.channel)
			else:
				await message.channel.send(helpMessage())
			continue
		if hero in buildsAliases:
			if len(text)==2:
				if message.channel.guild.id==535256944106012694 and message.channel.id!=571531013558239238:#In WS, not in #probius
					if message.guild.get_role(571321937821696001) not in message.author.roles:#Not core member
						await message.guild.get_channel(571531013558239238).send(message.author.mention+' <:bonk:761981366744121354>')
						await guide(aliases(text[1]),message.guild.get_channel(571531013558239238))
						continue
				await guide(aliases(text[1]),message.channel)
			else:
				await message.channel.send("Elitesparkle's builds: <https://elitesparkle.wixsite.com/hots-builds>")
			continue
		if hero in rotationAlises:
			await rotation(message.channel)
			continue
		if hero=='goodbot':
			await emoji(client,['Probius','love'],message.channel)
			continue
		if hero=='badbot':
			if message.author.id==183240974347141120:
				await emoji(client,['Probius','sad'],message.channel)
			else:
				await emoji(client,[':pylonbat'],message.channel)
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
			elif text[0]!='q':#Calling [q] alone shouldn't show link, but [q/hero] works, as well as [quotes]
				await message.channel.send('All hero select quotes: <https://github.com/Asddsa76/Probius/blob/master/quotes.txt>')
			continue
		if hero in aliasesAliases:
			await message.channel.send('All hero alternate names: <https://github.com/Asddsa76/Probius/blob/master/aliases.py>')
			continue
		if hero == 'all':
			await printAll(client,message,text[1],True)
			continue
		if hero in emojiAliases:
			await message.channel.send('Emojis: [:hero/emotion], where emotion is of the following: happy, lol, sad, silly, meh, angry, cool, oops, love, or wow.')
			continue
		try:
			if len(text)==1 and hero[0]=='t' and hero[8] ==',':#[t3221323,sam]
				await printBuild(client,message.channel,hero)
				continue
			if len(text)==2 and hero[0]=='t' and len(hero)==8 and hero!='tassadar':#[t3221323/sam]
				await printBuild(client,message.channel,','.join(text))
				continue
		except:
			pass
		#From here it's actual heroes, or a search
		if len(hero)==1 or (len(hero)==2 and ('1' in hero or '2' in hero)):#Patch notes have abilities in []. Don't want spammed triggers again. Numbers for R1, R2, etc.
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
		try:
			(abilities,talents)=client.heroPages[hero]
		except:
			try:#If no results, then "hero" isn't a hero
				await printAll(client,message,text[0])
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
			output='\n'.join(abilities)
			await printLarge(message.channel,quote+output)
			continue
		if output=='':
			if tier.isdigit():#Talent tier
				tier=int(tier)
				output=printTier(talents,int(tier/3)+int(hero=='Chromie' and tier not in [1,18]))#Talents for Chromie come 2 lvls sooner, except lvl 1
			elif tier in ['mount','z']:
				await message.channel.send(printAbility(abilities,'z'))
				return
			elif tier=='extra':
				await message.channel.send(printAbility(abilities,'1'))
				return
			elif tier=='r':#Ultimate
				if hero=='Tracer':#She starts with her heroic already unlocked, and only has 1 heroic
					output=abilities[3]
				else:
					output=printTier(talents,3-2*int(hero=='Varian'))#Varian's heroics are at lvl 4
					if hero=='Deathwing':
						output=abilities[3]+'\n'+output#Deathwing has Cataclysm baseline
			elif len(tier)==1 and tier in 'dqwe':#Ability (dqwe)
				output=printAbility(abilities,tier)
			elif tier=='trait':
				output=printAbility(abilities,'d')
			elif tier in wikipageAliases:#Linking user to wiki instead of printing everything
				await message.channel.send('<https://heroesofthestorm.gamepedia.com/Data:'+hero+'#Skills>')
				continue
			else:
				output=await printSearch(abilities, talents, tier, hero, True)
		
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
						await printLarge(message.channel,output.upper())
					else:
						await printLarge(message.channel,output)

def findTexts(message):
	allTexts=[]
	wholeText=message.content.lower()
	for text in wholeText.split('\n'):
		if '>' in text and '<' not in text:#This line is a quote
			continue
		leftBrackets=[1+m.start() for m in re.finditer('\[',text)]#Must escape brackets when using regex
		rightBrackets=[m.start() for m in re.finditer('\]',text)]
		texts=[text[leftBrackets[i]:rightBrackets[i]].split('/') for i in range(len(rightBrackets))]
		if len(leftBrackets)>len(rightBrackets):#One extra unclosed at end
			texts.append(text[leftBrackets[-1]:].split('/'))
		allTexts+=texts
	return allTexts

class MyClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.seenTitles=[]
		self.forwardedPosts=[]
		self.proxyEmojis={}
		# create the background task and run it in the background
		self.bgTask0 = self.loop.create_task(self.bgTaskSubredditForwarding())
		#self.bgTask1 = self.loop.create_task(self.bgTaskUNSORTED())
		self.heroPages={}
		self.lastWelcomeImage=[]
		self.waitList=[]
		self.isEditingPokedex=0
		self.ready=False#Wait until ready before taking commands

	async def on_ready(self):
		print('Logged on...')
		print('Filling up with Reddit posts...')
		self.forwardedPosts=[]
		self.seenTitles=await fillPreviousPostTitles(self)#Fills seenTitles with all current titles
		print('Fetching proxy emojis...')
		self.proxyEmojis=await getProxyEmojis(client.get_guild(603924426769170433))
		print('Downloading heroes...')
		await downloadAll(self,argv)
		self.ready=True
		print('Ready!')

	async def on_message(self, message):
		pingNames={'lemmie':190529178808877056, 'medicake':160743140901388288}
		pingList=[pingNames[i] for i in pingNames.keys() if '@'+i in message.content.replace(' ','')]
		if pingList:
			await message.channel.send(' '.join(['<@'+str(i)+'>' for i in pingList]))
			
		if message.embeds and message.channel.id==557366982471581718 and 'View tweet' in message.content:#Message with embed in #general
			await message.channel.send(message.embeds[0].thumbnail.url)
			await message.edit(suppress=True)
		if message.author.id==272526395337342977 and message.channel.id==557366982471581718:#Blizztrack posts in general
			try:
				e=message.embeds[0].fields[3]
				if e.name=='Full patch notes at':
					output='Patch notes!\n'+e.value
					await message.channel.send('@everyone '+output)
					await self.get_channel(222817241249480704).send(output)
			except:pass
		if message.author.bot:#Don't respond to bots
			return
		if 560435022427848705 in [role.id for role in message.author.roles]:#Unsorted
			try:
				await sortFromReaction(message,603924594956435491,self)
			except:
				await client.get_channel(576018992624435220).send('***Unsorted message:*** **'+message.author.name+'**: '+message.content+'\n'+message.jump_url)
			return
		if 'baelog' in message.content.lower():
			if message.channel.guild.id==535256944106012694:await client.get_channel(571531013558239238).send(message.author.mention+'Ba**LE**og\nhttps://i.imgur.com/Nrcg11Z.png')
			else:await message.channel.send('https://i.imgur.com/Nrcg11Z.png')
		if self.ready==False:
			return
		if message.content.count('@')>50 and message.channel.guild.id==535256944106012694:
			username=message.author.name
			channel=message.channel
			await message.channel.guild.ban(message.author,reason='Spam: over 50 pings in one message.')
			await channel.send('Banned '+username+' for excessive pings!')
			return

		elif '[' in message.content:
			texts=findTexts(message)
			await mainProbius(self,message,texts)

		await removeEmbeds(message)
		if message.author.id==0:#Birthday cake
			await message.add_reaction('🍰')
		
	async def on_message_edit(self,before, after):
		#Don't respond to ourselves
		if after.embeds and after.channel.id==557366982471581718 and 'New dev tweet!' in after.content:#Message with embed in #general
			await after.channel.send(after.embeds[0].thumbnail.url)
			await after.edit(suppress=True)
		if before.author.bot:
			return
		if '[' in after.content and ']' in after.content:
			try:
				beforeTexts=findTexts(before)
			except:
				beforeTexts=[]
			newTexts=[i for i in findTexts(after) if i not in beforeTexts]
			if newTexts:#Nonempty lists have boolean value true
				await mainProbius(self,after,newTexts)

		await removeEmbeds(after)

	async def on_raw_reaction_add(self,payload):
		member=client.get_user(payload.user_id)
		if member.id==603924594956435491:#Probius did reaction
			return

		print(member.name)
		print(client.get_channel(payload.channel_id).name)
		message=await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
		if message.author.id==670832046389854239:#Advisor wrote message
			return
		if message.id==693380327413907487:
			if str(payload.emoji) in wsReactionRoles:
				await client.get_guild(535256944106012694).get_member(payload.user_id).add_roles(client.get_guild(535256944106012694).get_role(wsReactionRoles[str(payload.emoji)]))

		elif message.author.id==603924594956435491 and str(payload.emoji)=='👎':#Message is from Probius, and is downvoted with thumbs down
			if message.channel.id in [665317972646166538,597140352411107328]:#Message is in reddit posts or pokedex
				output=member.mention+'<:bonk:761981366744121354>'
				await client.get_channel(557366982471581718).send(output)#general
				return
			elif 'reddit.com' in message.content:
				await message.channel.send(member.mention+'<:bonk:761981366744121354>')
				return
			elif '<:bonk:761981366744121354>' in message.content:
				return
			output=member.name+' deleted a message from Probius'
			print(output)
			await client.get_channel(643231901452337192).send('`'+output+'`')
			await message.delete()
			return

		elif message.author.id==603924594956435491 and 'React to ping' in message.content and str(payload.emoji)=='👍':#Message from Probius, pings Pokedex:
			output=member.name+' started a balance discussion'
			print(output)
			await client.get_channel(643231901452337192).send('`'+output+'`')
			await pingPokedex(self,message,member)
			return
		elif str(payload.emoji)=='⚽' and message.channel.id==557366982471581718:
			await sortFromReaction(message,member.id,self)
			return

		if member.id==183240974347141120:#Reaction copying
			await message.add_reaction(payload.emoji)

	async def on_raw_reaction_remove(self,payload):
		member=client.get_user(payload.user_id)
		message=await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
		if message.id==693380327413907487:
			if str(payload.emoji) in wsReactionRoles:
				await client.get_guild(535256944106012694).get_member(payload.user_id).remove_roles(client.get_guild(535256944106012694).get_role(wsReactionRoles[str(payload.emoji)]))

	async def on_member_join(self,member):
		guild=member.guild
		if guild.name=='Wind Striders':
			await member.add_roles(guild.get_role(560435022427848705))#UNSORTED role
			print(member.name+' joined')
			channel=guild.get_channel(557366982471581718)#general
			rulesChannel=guild.get_channel(634012658625937408)#server-rules
			await channel.send('Welcome '+member.mention+'! Please read '+rulesChannel.mention+' and type here the info at top **`Region`, `Rank`, and `Preferred Colour`** separated with commas, to get sorted and unlock the rest of the channels <:OrphAYAYA:657172520092565514>')
			try:
				for i in self.lastWelcomeImage:
					await i.delete()
			except:
				pass
			self.lastWelcomeImage =[await channel.send(file=discord.File('WS colours.png'))]
			self.lastWelcomeImage.append(await channel.send('https://cdn.discordapp.com/attachments/576018992624435220/743917827718905896/sorting.gif'))
			#await memberCount(channel)

	async def on_member_remove(self,member):
		guild=member.guild
		if guild.name=='Wind Striders':
			unsorted=guild.get_role(560435022427848705)
			if unsorted in member.roles:	
				print(member.name+' left (unsorted)')
				channel=guild.get_channel(557366982471581718)#general
				await channel.send(member.name+' (unsorted) left <:samudab:578998204142452747>')
				return
			#core=guild.get_role(571321937821696001)
			#if core not in member.roles: return
			print(member.name+' left')
			channel=guild.get_channel(616617012948631552)#super-secret-cabal
			await channel.send(member.name+' left the server <:samudab:578998204142452747>')
			await removePokedex(self,member.id)

	async def bgTaskSubredditForwarding(self):
		await self.wait_until_ready()
		channel = self.get_channel(557366982471581718)#WS general
		while not self.is_closed():
			await asyncio.sleep(60)#Check for new posts every minute
			try:
				await redditForwarding(self)
			except:
				pass

	async def on_member_update(self,before,after):
		if after.guild.id==535256944106012694:
			core=after.guild.get_role(571321937821696001)
			olympian=after.guild.get_role(557521663894224912)
			if core in after.roles and core not in before.roles:
				await self.get_channel(607922629902598154).send('Welcome '+after.mention+'!')
			if olympian in after.roles and olympian not in before.roles:
				await self.get_channel(576018992624435220).send('Welcome '+after.mention+'!')
				
	'''async def bgTaskUNSORTED(self):
		await self.wait_until_ready()
		channel = self.get_channel(557366982471581718)#WSgeneral
		role=channel.guild.get_role(560435022427848705)#UNSORTED
		rulesChannel=channel.guild.get_channel(634012658625937408)#server-rules
		while not self.is_closed():
			await asyncio.sleep(60*60*24)#Sleep 24 hours
			await channel.send('Note to all '+role.mention+': Please read '+rulesChannel.mention+' and ping **Olympian(mod)** with the **bolded** info at top **`Region`, `Rank`, and `Preferred Colour`** separated with commas, to get sorted and unlock the rest of the channels Blackstorm purges you <:peepoLove:606862963478888449>')
'''
exitBool=0
while 1: #Restart
	intents = discord.Intents.default()  # All but the two privileged ones
	intents.members = True  # Subscribe to the Members intent

	asyncio.set_event_loop(asyncio.new_event_loop())
	client = MyClient(command_prefix='!', intents=intents)
	client.run(getProbiusToken())
	if exitBool:break
