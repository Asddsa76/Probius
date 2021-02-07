from discordIDs import *

def helpMessage():
	output="""[Hero] to see that hero's abilities.
[Hero/level] for that hero's talents at that level.
[Hero/hotkey] for the ability on that hotkey.
[Hero/searchterm] to search for something in that hero's abilities or talents. & or -- in searchterm for AND and exclusions
[Hero/info] for hero info
[build/Hero] for hero builds/guides from Elitesparkle and others.
[rotation] for free weekly rotation from Gnub.
[patchnotes/hero] for patch notes from <https://heroespatchnotes.com>
Emojis: [:Hero/emotion], where emotion is of the following: happy, lol, sad, silly, meh, angry, cool, oops, love, or wow.
Mock drafting: [draft/info].
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
	u=userMention.replace(' ','').replace('!','').replace('<','').replace('>','').replace('@','').lower()
	if u.isnumeric():
		user=client.get_user(int(u))
	else:
		try:
			user=[i for i in channel.guild.members if i.name.lower().replace(' ','')==u or i.nick and i.nick.lower().replace(' ','')==u][0]
		except:
			return
	await channel.send(user.avatar_url)

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
		for i in ['forums.blizzard.com','psionic-storm.com','heroespatchnotes.com','#']:#Forum embeds are huge image, psionic-storm builds/talent/# embeds link to wrong build number or blank calculator
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
		a=1.96*(wr*(100-wr)/n)**0.5
		lower=str(wr-a)[:4]
		upper=str(wr+a)[:4]
		await channel.send('We are 95% confident that the winrate is between '+lower+'% and '+upper+'%.')
	except:
		await channel.send('Find a 95% confidence interval with [ci/winrate,games] \n<https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval>')

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