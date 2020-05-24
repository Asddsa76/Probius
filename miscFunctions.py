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

def getHeroes():#Returns an alphabetically sorted list of all heroes.
	return ['Abathur', 'Alarak', 'Alexstrasza', 'Ana', 'Anduin', "Anub'arak", 'Artanis', 'Arthas', 'Auriel', 'Azmodan', 'Blaze', 'Brightwing', 
	'Cassia', 'Chen', 'Cho', 'Chromie', 'D.Va', 'Deathwing', 'Deckard', 'Dehaka', 'Diablo', 'E.T.C.', 'Falstad', 'Fenix', 'Gall', 'Garrosh', 
	'Gazlowe', 'Genji', 'Greymane', "Gul'dan", 'Hanzo', 'Illidan', 'Imperius', 'Jaina', 'Johanna', 'Junkrat', "Kael'thas", "Kel'Thuzad", 
	'Kerrigan', 'Kharazim', 'Leoric', 'Li-Ming', 'Li_Li', 'Lt._Morales', 'Lúcio', 'Lunara', 'Maiev', "Mal'Ganis", 'Malfurion', 'Malthael', 
	'Medivh', 'Mephisto', 'Muradin', 'Murky', 'Nazeebo', 'Nova', 'Orphea', 'Probius', 'Qhira', 'Ragnaros', 'Raynor', 'Rehgar', 'Rexxar', 
	'Samuro', 'Sgt._Hammer', 'Sonya', 'Stitches', 'Stukov', 'Sylvanas', 'Tassadar', 'The_Butcher', 'The_Lost_Vikings', 'Thrall', 'Tracer', 
	'Tychus', 'Tyrael', 'Tyrande', 'Uther', 'Valeera', 'Valla', 'Varian', 'Whitemane', 'Xul', 'Yrel', 'Zagara', 'Zarya', 'Zeratul', "Zul'jin"]

async def roll(text,message):
	if len(text)==1:
		n=6
	else:
		n=int(text[1])
	from random import randint
	from random import seed
	seed()
	await message.channel.send(str(randint(1,n)))

async def getAvatar(client,channel,userMention):
	if '<' not in userMention:
		await channel.send('Need a ping')
		return
	userString=userMention.replace(' ','')[2:-1].replace('!','')
	user=client.get_user(int(userString))
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
	guild=client.get_guild(535256944106012694)#Wind Striders
	if 557521663894224912 not in [role.id for role in author.roles]:
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
	await guild.get_channel(576018992624435220).send('Deleted '+str(deletedCount)+' messages from '+ping)

async def removeEmbeds(message):#Some embeds are instant, others are edited in by discord. Call in both on_message and on_message_edit
	if message.embeds:
		for i in ['forums.blizzard.com','psionic-storm.com','heroespatchnotes.com']:#Forum embeds are huge image, psionic-storm builds/talent embeds link to wrong build number or blank calculator
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
		a=1.96*(wr*(100-wr)/n)
		lower=str(wr-a)[:4]
		upper=str(wr+a)[:4]
		await channel.send('We are 95% confident that the winrate is between '+lower+'% and '+upper+'%.')
	except:
		await channel.send('Find a 95% confidence interval with [ci/winrate,games]')