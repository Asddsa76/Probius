def edgeCases(abilities,hero):#Some heroes have weird text in D after < brackets. 
	if hero =='Samuro':
		abilities[0]+='\n'+"**Advancing Strikes:** Basic Attacks against enemy Heroes increase Samuro's Movement Speed by 25% for 2 seconds."
	elif hero=='Tassadar':
		abilities[0]+='\n'+"**Distortion Beam:** Tassadar's Basic Attack is a Distortion Beam that slows enemy units by 25%."
	return abilities

def helpMessage():
	output="[Hero] to see that hero's abilities.\n"
	output+="[Hero/level] for that hero's talents at that level.\n"
	output+="[Hero/hotkey] for the ability on that hotkey.\n"
	output+="[Hero/searchterm] to search for something in that hero's abilities or talents. \n"
	output+="Emojis: [:Hero/emotion], where emotion is of the following: happy, lol, sad, silly, meh, angry, cool, oops, love, or wow."
	return output