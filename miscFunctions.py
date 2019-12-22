def helpMessage():
	output="[Hero] to see that hero's abilities.\n"
	output+="[Hero/level] for that hero's talents at that level.\n"
	output+="[Hero/hotkey] for the ability on that hotkey.\n"
	output+="[Hero/searchterm] to search for something in that hero's abilities or talents. & or -- in searchterm for AND and exclusions\n"
	output+="[Hero/info] for hero info\n"
	output+="[build/Hero] for hero builds/guides from Elitesparkle and others.\n"
	output+="[rotation] for free weekly rotation from Gnub.\n"
	output+="Emojis: [:Hero/emotion], where emotion is of the following: happy, lol, sad, silly, meh, angry, cool, oops, love, or wow.\n"
	output+="Mock drafting: [draft/info].\n"
	output+="My public repository: <https://github.com/Asddsa76/Probius>"
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
	userString=userMention.replace(' ','')[2:-1].replace('!','')#Space because discord makes one after mention, ! for nicknames
	user=client.get_user(int(userString))
	await channel.send(user.avatar_url)