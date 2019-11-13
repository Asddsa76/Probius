from aliases import *

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
	for i in range(1,len(draftList)):
		if order[i]=='A':
			bansA.append(draftList[i])
		elif order[i]=='B':
			bansB.append(draftList[i])
		elif order[i]=='a':
			picks+=draftList[i]+'\n'
		elif order[i]=='b':
			picks+=' '*40+draftList[i]+'\n'
	output='```Map: '+draftList[0]+'\n\n'
	output+='Team A'+' '*34+'Team B\n'
	output+='Bans: '+' '*34+'Bans: \n'
	output+=', '.join(bansA)+' '*(40-len(', '.join(bansA)))+', '.join(bansB)+'\n'+'-'*50+'\n'
	output+='Picks:'+' '*34+'Picks:\n'+picks+'\n'

	if len(draftList)==17:
		output+='Draft complete'
		if channel.guild.id==623202246062243861:#Hydeout
			await channel.guild.get_channel(643976359303184404).send(output+'```')#discussion
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
	if len(text)==2:
		if text[1] in ['help','info']:
			await channel.send('[Draft/command] to access these commands.\nNo command to view state. Hero or map to pick/ban.\nReset to reset the draft. Undo to undo most recent action.')
			return
	try:
		draftList=client.drafts[channel.id]
	except:
		client.drafts[channel.id]=[]
		await channel.send('New draft started! Choose map')
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
		if aliases(text) in draftList:
			await channel.send(aliases(text)+' has already been picked/banned. Choose another!')
		else:
			draftList.append(aliases(text))
			if aliases(text)=='Samuro':#Bots can use emojis from all servers the bot is in! :D
				await channel.send('<:banned:557364849940758528>')#It's sent when Sam is picked as well, not just banned. Too lazy to fix

	await printDraft(client,channel,draftList)