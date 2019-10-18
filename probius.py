#A HotS Discord bot
#Call in Discord with [hero/modifier]
#Modifier is hotkey or talent tier
#Data is pulled from HotS wiki
#Project started on 14/9-2019

import discord
import io
import aiohttp
import re

from aliases import *			#Spellcheck and alternate names for heroes
from trimBrackets import *		#Trims < from text
from printFunctions import *	#The functions that output the things to print
from heroPage import *			#The function that imports the hero pages
from emojis import *			#Emojis
from miscFunctions import*		#Edge cases and help message
from getDiscordToken import *	#The token is in an untracked file because this is a public Github repo
from elitesparkleBuilds import *#Hero builds
from rotation import *			#Weekly rotation

def findTexts(message):
	text=message.content.lower()
	leftBrackets=[1+m.start() for m in re.finditer('\[',text)]#Must escape brackets when using regex
	rightBrackets=[m.start() for m in re.finditer('\]',text)]
	texts=[text[leftBrackets[i]:rightBrackets[i]].split('/') for i in range(len(leftBrackets))]
	return texts

async def mainProbius(message,texts):
	print(message.channel.name+' '+str(message.author)+': '+message.content)
	for text in texts:
		hero=text[0]
		if hero in ['help','info']:
			await message.channel.send(helpMessage())
			continue
		if hero in ['guide','guides','elitesparkle','build']:
			await guide(aliases(text[1]),message.channel)
			continue
		if hero=='rotation':
			await message.channel.send(rotation())
			continue
		if hero=='good bot':
			await message.channel.send(':heart:')
			continue
		if hero=='bad bot':
			await emoji(['Probius','sad'],message.channel)
			continue
		if ':' in hero:
			await emoji([hero.replace(':',''),text[1]],message.channel)
			continue

		hero=aliases(hero)
		[abilities,talents]=heroAbilitiesAndTalents(hero)
		abilities=extraD(abilities,hero)
		if hero in ['Chogall',"Cho'gall",'Cg','Cho gall','Cho-gall']:
			await message.channel.send("Cho and Gall are 2 different heroes. Choose one of them")
			print('Dual hero')
			return
		if abilities==404:
			try:#If no results, it's probably an emoji with : forgotten. Prefer to call with : to avoid loading abilities and talents page
				await emoji([hero,text[1]],message.channel)
				return
			except:
				pass
			output='No hero "'+hero+'"'
			if message.channel.name=='rage':
				output=output.upper()
			await message.channel.send(output)
			print('No hero')
			return
		
		output=''
		try:
			tier=text[1]#If there is no identifier, then it throws exception
		except:
			output=printAbilities(abilities)
			#await emoji([text[0],'happy'],message.channel)
		if output=='':
			if tier.isdigit():#Talent tier
				tier=int(tier)
				output=printTier(talents,int(tier/3)+int(hero=='Chromie' and tier!=1))#Talents for Chromie come 2 lvls sooner, except lvl 1
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
			elif tier.lower()=='trait':
				output=printAbility(abilities,'d')
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
						await emoji([hero,tier],message.channel)
						return
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

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as', self.user)

	async def on_message(self, message):
		#Don't respond to ourselves
		if message.author == self.user:
			return
		if '[' in message.content and ']' in message.content:
			texts=findTexts(message)
			await mainProbius(message,texts)
		
	async def on_message_edit(self,before, after):
		if '[' in after.content and ']' in after.content:
			beforeTexts=findTexts(before)
			newTexts=[i for i in findTexts(after) if i not in beforeTexts]
			if newTexts:#Nonempty lists have boolean value true
				await after.channel.send('**------After edit------**')
				await mainProbius(after,newTexts)

	async def on_raw_reaction_add(self,payload):
		if client.get_user(payload.user_id).name=='Asddsa76':
			await (await (client.get_channel(payload.channel_id)).fetch_message(payload.message_id)).add_reaction(payload.emoji)
client = MyClient()
client.run(getDiscordToken())