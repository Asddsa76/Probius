from aliases import *
from printFunctions import *
from maps import *
from emojis import emoji
import asyncio
import discord

banEmojis={'Ana':'🍌',
'Samuro':'<:banned:557364849940758528>',
'Tassadar':'<:bannedLogan:673197798786596864>',
'Valeera':'<:bannedVal:679014495447678998>'}

banEmojis={}

def simplifyName(hero):#Turn underscores into spaces
	hero=hero.replace('_',' ')
	return hero

async def getWhiteSpaceLength(draftList):
	order='mABABabbaaBAbbaab'
	bansA=[]
	for i in [1,3,11]:
		try: bansA.append(draftList[i])
		except:pass
	return max(25,3+len(', '.join(bansA)))

async def printDraft(drafts,channel,draftList,lastDraftMessageDict,draftNames):#Print state, and the next action to be done
	if channel.id not in drafts:
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
	#whitespaceAmount=32
	whitespaceAmount=await getWhiteSpaceLength(draftList)
	teamA='Team A'
	teamB='Team B'
	try:
		teamA+=' ('+draftNames[channel.id][0]+')'
		teamB+=' ('+draftNames[channel.id][1]+')'
	except:pass
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
	output+=teamA+' '*(whitespaceAmount-len(teamA))+teamB+'\n'
	output+='Bans: '+' '*(whitespaceAmount-6)+'Bans: \n'
	output+=', '.join(bansA)+' '*(whitespaceAmount-len(', '.join(bansA)))+', '.join(bansB)+'\n'+'-'*(whitespaceAmount+15)+'\n'
	output+='Picks:'+' '*(whitespaceAmount-6)+'Picks:\n'+picks+'\n'

	completeDraft=0
	if len(draftList)==17:
		output+='Draft complete'
		completeDraft=1
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
		try:
			output+=' ('+draftNames[channel.id][nextTurnIsTeamB]+')'
		except:
			pass
		if nextTurnIsTeamB:
			output+=' ---------->'

	if len(draftList)>1:
		hero=aliases(draftList[-1]).replace('_',' ').replace('The Butcher','Butcher').capitalize()
		fileName=''
		fileExtension='.PNG' if hero=='Maiev' else '.png'
		if len(draftList) in [2,3,4,5,11,12]:#Numbers are the bans
			if hero in banEmojis.keys():
				output=banEmojis[hero]+'\n'+output
			else:
				if channel in lastDraftMessageDict:
					await lastDraftMessageDict[channel].delete()
				lastDraftMessageDict[channel]=await channel.send(output+'```',file=discord.File('Emojis/'+hero+' sad'+fileExtension))
				return
		else:
			if channel in lastDraftMessageDict:
				await lastDraftMessageDict[channel].delete()
			lastDraftMessageDict[channel]=await channel.send(output+'```',file=discord.File('Emojis/'+hero+' happy'+fileExtension))
			return

	if channel in lastDraftMessageDict:
		await lastDraftMessageDict[channel].delete()
	lastDraftMessageDict[channel]=await channel.send(output+'```')
	if completeDraft:
		await lastDraftMessageDict[channel].add_reaction('🇦')
		await lastDraftMessageDict[channel].add_reaction('🇧')

async def draft(drafts,channel,member,text,lastDraftMessageDict,draftNames,printDraftBool=True):
	try:
		draftList=drafts[channel.id]
	except:
		drafts[channel.id]=[]
		draftList=drafts[channel.id]
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
			drafts[channel.id]=[]
			draftList=drafts[channel.id]
			if channel in lastDraftMessageDict:del lastDraftMessageDict[channel]
			battleground=await mapAliases(text[1])
			draftList.append(await mapString(battleground))
			await channel.send('New draft started!')
			await mapImage(channel,battleground)
			draftNames[channel.id]=[]
			if printDraftBool:await printDraft(drafts,channel,draftList,lastDraftMessageDict,draftNames)
			return
	if len(text)==1: #[draft] with no second part. To call status
		await printDraft(drafts,channel,draftList,lastDraftMessageDict,draftNames)
		return
	text=text[1]
	if text.count(','):
		for i in text.split(','):
			await draft(drafts,channel,member,['d',i],lastDraftMessageDict,draftNames,False)
		await channel.send('Draft filled! Type [d] to view')
		return
	if text in ['new','start','n','s','reset','r']:
		drafts[channel.id]=[]
		if channel in lastDraftMessageDict:del lastDraftMessageDict[channel]
		await channel.send('New draft started! Choose map')
		draftNames[channel.id]=[]
		return
	if text in ['undo','u']:
		await channel.send('Undid '+draftList.pop())
	elif len(draftList)<17:
		if len(draftList)==1:
			draftNames[channel.id]=[member.nick or member.name]
		elif len(draftList)==2:
			draftNames[channel.id].append(member.nick or member.name)

		if simplifyName(aliases(text)) in draftList:
			await channel.send(simplifyName(aliases(text))+' has already been picked/banned. Choose another!')
			return
		else:
			if len(draftList)==0:#Map name doesn't need check
				try:
					battleground=await mapAliases(text)
				except:
					await channel.send('`Unrecognized battleground!`')
					return
				draftList.append(await mapString(battleground))
				await mapImage(channel,battleground)
			else:
				hero=aliases(text)
				if hero in getHeroes():
					draftList.append(simplifyName(hero))
				else:
					await channel.send('Invalid hero!')
					return

	if printDraftBool:await printDraft(drafts,channel,draftList,lastDraftMessageDict,draftNames)