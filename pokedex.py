from miscFunctions import *

async def pokedex(client,channel,hero):
	pokedex=client.pokedex
	if hero=='Test':
		for hero in getHeroes():
			if hero.replace('_',' ') not in pokedex:
				print(hero.replace('_',' '))
		return
	if hero not in getHeroes():
		await channel.send('No hero "'+hero+'"')
		return

	hero=hero.replace('_',' ')
	mains=pokedex.split(hero)[1].split('\n')[0]
	if mains:
		names=[client.get_user(int(i)).name.capitalize() for i in mains.replace('>','').replace(' ','').replace('!','').split('<@')[1:]]
		message=await channel.send(hero+' discussion! Our mains are **'+', '.join(names)+'.** React to ping them.')
	else:
		message=await channel.send(hero+" discussion! We don't have any mains for this hero, ping <@329447886465138689> if you know any. React to ping Balance team.")
	await message.add_reaction('\U0001f44d')

async def pingPokedex(client,message,member):
	vowels='AEIOU'
	if 'Balance team' in message.content:
		await message.channel.send(member.mention+' wants to start a'+'n'*(message.content[0] in vowels)+' '+message.content.split('We ')[0]+'<@&577935915448795137>')
	else:
		pokedex=client.pokedex
		hero=message.content.split(' discussion!')[0]
		mains=pokedex.split(hero)[1].split('\n')[0]
		await message.channel.send(member.mention+' wants to start a'+'n'*(message.content[0] in vowels)+' '+message.content.split('Our ')[0]+mains)
	await message.delete()