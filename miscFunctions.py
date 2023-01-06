from discordIDs import *
from printFunctions import *
from random import randint
from random import choice
import time
import datetime
import asyncio
import aiohttp
import scipy.stats

def helpMessage():
	output="""[Hero] to see that hero's abilities
[Hero/level] for that hero's talents at that level
[Hero/hotkey] for the ability on that hotkey
[Hero/searchterm] to search for something in that hero's abilities or talents. & or -- in searchterm for AND and exclusions
[Hero/info] for hero info
[build/Hero] for hero builds/guides
[rotation] for free weekly rotation from <https://nexuscompendium.com/>
[patchnotes/hero] for patch notes from <https://heroespatchnotes.com>
Emojis: [:Hero/emotion], where emotion is of the following: happy, lol, sad, silly, meh, angry, cool, oops, love, or wow
Mock drafting: [draft/info]
[battleground/X] and [core/X], where X is a battleground, for a map or a description of the core's abilities
My public repository: <https://github.com/Asddsa76/Probius>"""
	return output

async def roll(text,message):
	n=6 if len(text)==1 else int(text[1])
	from random import randint
	from random import seed
	seed()
	await message.channel.send(str(randint(1,n)))

async def getAvatar(client,channel,userMention):
	#Change from client.get_user to guild.get_member
	#check for guild-specific avatar url
	u=userMention.replace(' ','').replace('!','').replace('<','').replace('>','').replace('@','').lower()
	if u.isnumeric():
		user=client.get_user(int(u))
	else:
		try:
			user=[i for i in channel.guild.members if i.name.lower().replace(' ','')==u or i.nick and i.nick.lower().replace(' ','')==u][0]
		except:
			return
	return str(user.avatar_url)

async def vote(message,text):
	if len(text)==2:
		n=int(text[1])
		if n<1 or n>9:
			await message.channel.send('Out of range')
			return
		for i in range(1,n+1):
			await message.add_reaction(str(i)+'\N{combining enclosing keycap}')
	else:
		await message.add_reaction('\U0001f44d')
		await message.add_reaction('\U0001f44e')

async def deleteMessages(author,ping,client):
	guild=client.get_guild(DiscordGuildIDs['WindStriders'])#Wind Striders
	if DiscordRoleIDs['Olympian'] not in [role.id for role in author.roles]:
		return
		
	userId=int(ping.replace(' ','').replace('!','')[2:-1])
	deletedCount=0
	for channel in guild.text_channels:
		try:
			async for message in channel.history(limit=20):
				if message.author.id==userId:
					await message.delete()
					deletedCount+=1
		except:
			pass
	await guild.get_channel(DiscordChannelIDs['Pepega']).send('Deleted '+str(deletedCount)+' messages from '+ping)

async def removeEmbeds(message):#Some embeds are instant, others are edited in by discord. Call in both on_message and on_message_edit
	if message.embeds:
		for i in ['forums.blizzard.com','psionic-storm.com','heroespatchnotes.com','#', 'twitch.tv', 'youtube.com/shorts']:#Forum embeds are huge image, psionic-storm builds/talent/# embeds link to wrong build number or blank calculator
			if i in message.content:
				try:
					await message.edit(suppress=True)
				except:
					return

async def waitList(message,text,client):
	if len(text)==1:
		await message.channel.send('Wait list: '+' ,'.join([i.name for i in client.waitList]))
	elif text[1] in ['join','next']:
		client.waitList.append(message.author)
		await message.channel.send(message.author.name+' has been added to the wait list.')
	elif text[1] in ['ping','here']:
		await message.channel.send('Wait list: '+', '.join([i.mention for i in client.waitList]))
	elif text[1]=='clear':
		client.waitList=[]
	elif text[1] in ['leave','unnext']:
		del client.waitList[client.waitList.index(message.author)]

async def confidence(channel,text):
	try:
		wr,n=text[1].replace(' ','').split(',')
		wr=float(wr)
		n=int(n)
		if n<=1000000: # Shouldn't let n be too large or the exact computation could be expensive
			interval=scipy.stats.binomtest(round(wr/100*n),n).proportion_ci()
			lower=round(interval.low*100,1)
			upper=round(interval.high*100,1)
		else:
			a=1.96*(wr*(100-wr)/n)**0.5
			lower=str(wr-a)[:4]
			upper=str(wr+a)[:4]
		await channel.send('We are 95% confident that the winrate is between '+str(lower)+'% and '+str(upper)+'%.')
	except:
		await channel.send('Input success rate as a percentage from 0 to 100, then sample size (at least 1)')

async def memberCount(channel):
	await channel.send(channel.guild.name+' has '+str(len(channel.guild.members))+' members!')

async def ping(channel):
	await channel.send("""In game: ctrl+alt+F
In cmd.exe:
		`US West:    ping 24.105.30.129`
		`US Central: ping 24.105.62.129`
		`Brazil:     ping 54.207.104.145`
		`EU:         ping 185.60.112.157`""")

async def sortList(message):
	a=message.content.split(']\n')[1].split('\n')
	a.sort(key=lambda i:-int(i.split(': ')[1]))
	await message.channel.send('\n'.join(a))

async def schedule(message):
	await message.channel.send('''Monday: PTR patch
Tuesday: Content patch (for NA. Early wednesday morning for EU)
Wednesday: Balance patch''')

def findMentions(message):
	return ['<@'+i[:i.index('>')+1] for i in message.content.replace('!','').split('<@')[1:]]

async def coaching(message):
	if 859488289559805972 in [i.id for i in message.author.roles]:
		await message.channel.send('<@&860563593090564107> Coach '+message.author.mention+' is running a live session! Head down to <#859854861750763570> to check it out!')
	else:
		await message.channel.send(message.author.mention+' you must be a coach to host coaching sessions.')

async def wrongChannelBuild(message):
	await message.guild.get_channel(DiscordChannelIDs['Probius']).send(message.author.mention+' Please call builds in this channel to avoid cluttering the other channels!')
	await message.guild.get_channel(DiscordChannelIDs['Probius']).send('https://cdn.discordapp.com/attachments/604394753722941451/892843516722569266/help_probius_clean_up1.png')

async def randomBuild(client, channel, hero):
	if hero=='Random':
		hero=choice(getHeroes())
	else:
		try:#Roles
			hero=choice(await getRoleHeroes(hero.lower()))
		except:
			pass

	(abilities,talents)=client.heroPages[hero]
	text='T'
	for tier in talents[:-1]:
		text+=str(randint(1,len(tier)))

	#Storm tier: 1 less option. If ult conflict, choose last talent.
	#Todo: Varian, Maiev, Alarak, Tracer, Deathwing, Garrosh, Fenix, Imperius?, Junkrat, LM?, Morales?
	a=randint(1,len(talents[-1])-1)
	if (a<=2) and (a!=int(text[4])):
		text+=str(len(talents[-1]))
	else:
		text+=str(a)

	text+=','+hero
	await printCompactBuild(client,channel,text)

async def countdown(message,text):
	if len(text)==1:
		await message.channel.send('<t:'+str(int(time.time()))+'>')
	elif text[1] in ['pa','patch']:
		async with aiohttp.ClientSession() as session:
			async with session.get('https://heroespatchnotes.com/patch/') as response:
				page = await response.text()
		page=page.split('<h1>Heroes of the Storm Patch List</h1>')[1].split('<h3>')[1].split('</small></h3>')[0]
		a,version=page.split('<small class="hidden-xs">v ')
		patchType=a[11:]

		date=a[:10]
		d=time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
		daysSincePatch=int((time.time()-d)/86400)
		weeks=str(daysSincePatch//7)
		days=str(daysSincePatch%7)

		await message.channel.send('Previous patch: **v'+version+' '+patchType+'**'+date+' ('+weeks+' weeks and '+days+' days ago) \nPatch list: <https://heroespatchnotes.com/patch/>')
	else:
		words=text[1].lower().replace(',',' ').replace('  ',' ').split(' ')
		a={'s':1, 'm':60, 'h':3600, 'd':86400}
		t=int(time.time())
		for i in words:
			for j in a.keys():
				if j in i:
					t+=a[j]*int(i.replace(j,''))
					break
		t=str(t)
		await message.channel.send('<t:'+t+'> (<t:'+t+':R>)')

async def iAmName(message):
	if message.channel.guild.id!=535256944106012694 or message.author.id!=224975834346291210:
		return

	index=message.content.lower().find("i'm ")+4
	if index==3:#no result
		index=message.content.lower().find("i am ")+5
		if index==4:#no result
			return

	#Discord names must be between 2 and 32 characters
	wordList=message.content[index:].split(' ')
	newName=wordList.pop(0)
	for word in wordList:
		proposedName=f"{newName} {word}"
		if len(proposedName)<32:
			newName=proposedName
		else:
			break

	if len(newName)<=2:return
	await message.author.edit(nick=newName)