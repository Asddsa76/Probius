#A HotS Discord bot
#Call in Discord with [hero/modifier]
#Modifier is hotkey or talent tier
#Data is pulled from HotS wiki
#Project started on 14/9-2019

import discord
import io
import aiohttp

from aliases import *#Spellcheck and alternate names for heroes
from trimBrackets import *#Trims < from text
from printFunctions import *#The functions that output the things to print
from heroPage import *#The function that imports the hero pages
from emojis import *#Emojis
from miscFunctions import*#Edge cases and help message
from getDiscordToken import *#The token is in an untracked file because this is a public Github repo

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as', self.user)

	async def on_message(self, message):
		#Don't respond to ourselves
		if message.author == self.user:
			return

		if '[' in message.content and ']' in message.content:
			print(message.channel.name+' '+str(message.author)+': '+message.content)
			text=message.content.lower()
			if text in ['[help]','[info]']:
				await message.channel.send(helpMessage())
				return
			elif ':' in text:
				await emoji(text[text.index('[')+1:text.index(']')].replace(':','').split('/'),message.channel)
				return
			text=text[text.index('[')+1:text.index(']')].split('/')
			hero=text[0]
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
				await emoji([text[0],'happy'],message.channel)
			if output=='':
				if tier.isdigit():#Talent tier
					tier=int(tier)
					output=printTier(talents,int(tier/3)+int(hero=='Chromie' and tier!=1))#Talents for Chromie come 2 lvls sooner, except lvl 1
				elif tier=='mount':
					output=abilities[-1]#Last ability. It's heroic if the hero has normal mount, but that's an user error
				elif tier=='extra':
					if hero=='Zeratul':
						output=abilities[-1]
					elif hero=='Gall':
						output=abilities[-2]
					else:
						output=abilities[1]
				elif tier=='r':#Ultimate
					if hero=='Tracer':#She starts with her heroic already unlocked, and only has 1 heroic
						output=abilities[4]
					else:
						output=printTier(talents,3-2*int(hero=='Varian'))#Varian's heroics are at lvl 4
				elif len(tier)==1 and tier in 'dqwe':#Ability (dqwe)
					output=printAbility(abilities,tier,hero)
				elif tier.lower()=='trait':
					output=printAbility(abilities,'d',hero)
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
							await message.channel.send('ERROR: NO RESULTS')
						else:
							await message.channel.send('Error: no results')
						print('No results')
					else:
						if message.channel.name=='rage':
							await message.channel.send("ERROR: EXCEEDED DISCORD'S 2000 CHARACTER LIMIT. BE MORE SPECIFIC")
						else:
							await message.channel.send("Error: exceeded Discord's 2000 character limit. Be more specific")
						print('2000 limit')
			
client = MyClient()
client.run(getDiscordToken())