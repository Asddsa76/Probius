from aliases import *
from miscFunctions import *
from maps import *
from emojis import emoji
import discord

banEmojis={'Ana':'🍌',
'Samuro':'<:banned:557364849940758528>',
'Tassadar':'<:bannedLogan:673197798786596864>',
'Valeera':'<:bannedVal:679014495447678998>'}

def simplifyName(hero):#Shorten all names with 10+ letters, and turn underscores into spaces
	hero=hero.replace('_',' ')
	return hero
	if hero=='The Lost Vikings':
		return 'TLV'
	elif hero=='The Butcher':
		return 'Butcher'
	elif hero=='Sgt. Hammer':
		return 'Hammer'
	elif hero=='Lt. Morales':
		return 'Morales'
	elif hero=='Alexstrasza':
		return 'Alex'
	elif hero=='Brightwing':
		return 'BW'
	elif hero=="Kel'Thuzad":
		return 'KTZ'
	else:
		return hero

async def printDraft(client,channel,draftList):#Print state, and the next action to be done
	if channel.id not in client.drafts:
		await channel.send(channel.id+' does not currently have an active draft.')
		return
	if not draftList:
		await channel.send('Pick a map')
		return

	#Order and map have been picked now
	order='mABABabbaaBAbbaab'#map, order. AB bans, ab picks
	bansA=[]
	bansB=[]
	picks=''
	whitespaceAmount=32
	for i in range(1,len(draftList)):
		if order[i]=='A':
			bansA.append(draftList[i])
		elif order[i]=='B':
			bansB.append(draftList[i])
		elif order[i]=='a':
			picks+=draftList[i]+'\n'
		elif order[i]=='b':
			picks+=' '*whitespaceAmount+draftList[i]+'\n'
	output='```Map: '+draftList[0]+'\n\n'
	output+='Team A'+' '*(whitespaceAmount-6)+'Team B\n'
	output+='Bans: '+' '*(whitespaceAmount-6)+'Bans: \n'
	output+=', '.join(bansA)+' '*(whitespaceAmount-len(', '.join(bansA)))+', '.join(bansB)+'\n'+'-'*(whitespaceAmount+15)+'\n'
	output+='Picks:'+' '*(whitespaceAmount-6)+'Picks:\n'+picks+'\n'

	if len(draftList)==17:
		output+='Draft complete'
	else:
		nextAction=order[len(draftList)]
		nextTurnIsTeamB=1
		if nextAction.lower()=='a':
			output+='<---------- '
			nextTurnIsTeamB=0
		if nextAction==nextAction.upper():
			nextAction='BAN for team '+nextAction
		else:
			nextAction='Pick for team '+nextAction.upper()
		output+='Next action: '+nextAction
		if nextTurnIsTeamB:
			output+=' ---------->'
	await channel.send(output+'```')

async def draft(client,channel,text):
	try:
		draftList=client.drafts[channel.id]
	except:
		client.drafts[channel.id]=[]
		draftList=client.drafts[channel.id]
	if len(text)==2:
		if text[1] in ['help','info']:
			output='''MOCK DRAFTING GUIDE

[Draft] will show the current state of the draft.
[Flip] will toss a coin that can be used to randomly select who will go for first pick or Map choice after writing your head or tail preference in chat.

[Draft/<Map>] will set the Map at the beginning of the draft.
[Draft/<Hero>] will pick or ban a Hero based on the in-game drafting order.
[Draft/<Command>] will let you use a Command listed below.

Commands:
- "Help" will show this guide.
- "Reset" will reset the draft.
- "Undo" will revert the previous input.'''
			await channel.send(output)
			return
		if await mapAliases(text[1]) in await getMaps() and len(draftList) in [0,17]:
			battleground=await mapAliases(text[1])
			draftList.append(await mapString(battleground))
			await channel.send(file=discord.File('Maps/'+battleground+'.jpg'))
			await printDraft(client,channel,draftList)
			return
	if len(text)==1: #[draft] with no second part. To call status
		await printDraft(client,channel,draftList)
		return
	text=text[1]
	if text in ['new','start','n','s','reset','r']:
		client.drafts[channel.id]=[]
		await channel.send('New draft started! Choose map')
		return
	if text in ['undo','u']:
		await channel.send('Undid '+draftList.pop())
		await printDraft(client,channel,draftList)
		return
	if len(draftList)<17:
		if simplifyName(aliases(text)) in draftList:
			await channel.send(simplifyName(aliases(text))+' has already been picked/banned. Choose another!')
		else:
			if len(draftList)==0:#Map name doesn't need check
				try:
					battleground=await mapAliases(text)
				except:
					await channel.send('`Unrecognized battleground!`')
					return
				draftList.append(await mapString(battleground))
				await channel.send(file=discord.File('Maps/'+battleground+'.jpg'))
			else:
				hero=aliases(text)
				if hero in getHeroes():
					draftList.append(simplifyName(hero))
					if len(draftList) in [2,3,4,5,11,12]:#Numbers are the bans
						if hero in banEmojis.keys():
							await channel.send(banEmojis[hero])
						else:
							await emoji(client,[hero,'sad'],channel)
					else:
						await emoji(client,[hero,'happy'],channel)
				else:
					await channel.send('Invalid hero!')

	await printDraft(client,channel,draftList)