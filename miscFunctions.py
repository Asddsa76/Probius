def extraD(abilities,hero):#Some heroes have weird text in D after < brackets. 
	if hero =='Samuro':
		abilities[0]+='\n'+"**Advancing Strikes:** Basic Attacks against enemy Heroes increase Samuro's Movement Speed by 25% for 2 seconds."
	elif hero=='Tassadar':
		abilities[0]+='\n'+"**Distortion Beam:** Tassadar's Basic Attack is a Distortion Beam that slows enemy units by 25%."
	elif hero=="Zul'jin":
		abilities[0]=abilities[0][:-14]+' **You Want Axe?** ***❢ Quest:*** Every 5 Basic Attacks against Heroes permanently increases Basic Attack damage by 1. '
		abilities[0]+='***? Reward:*** After attacking 75 times, Basic Attack range is increased by 1.1. '
		abilities[0]+='***? Reward:*** After attacking 150 times, Twin Cleave now revolves twice.'
	return abilities

def helpMessage():
	output="[Hero] to see that hero's abilities.\n"
	output+="[Hero/level] for that hero's talents at that level.\n"
	output+="[Hero/hotkey] for the ability on that hotkey.\n"
	output+="[Hero/searchterm] to search for something in that hero's abilities or talents.\n"
	output+="Emojis: [:Hero/emotion], where emotion is of the following: happy, lol, sad, silly, meh, angry, cool, oops, love, or wow.\n"
	output+="Builds: [guide/Hero] for hero guide from Elitesparkle.\n"
	output+="My public repository: https://github.com/Asddsa76/Probius"
	return output

def getHeroes():#Returns an alphabetically sorted list of all heroes.
	return ['Abathur', 'Arthas', "Anub'arak", 'Artanis', 'Alarak', 'Anduin', 'Azmodan', 'Alexstrasza', 'Ana', 'Auriel', 'Brightwing', 'Blaze', 'Cassia', 'Chromie', 'Cho', 'Chen', 'Diablo', 'Dehaka', 'Deckard', 'D.va', 'E.t.c.', 'Falstad', 'Fenix', 'Genji', "Gul'dan", 'Greymane', 'Garrosh', 'Gazlowe', 'Gall', 'Hanzo', 'Imperius', 'Illidan', 'Johanna', 'Junkrat', 'Jaina', 'Kerrigan', 'Kharazim', "Kel'thuzad", "Kael'thas", 'Lúcio', 'Lt._morales', 'Li_li', 'Leoric', 'Lunara', 'Li-Ming', 'Murky', 'Mephisto', 'Muradin', "Mal'Ganis", 'Malfurion', 'Malthael', 'Maiev', 'Medivh', 'Nova', 'Nazeebo', 'Orphea', 'Probius', 'Qhira', 'Raynor', 'Rehgar', 'Rexxar', 'Ragnaros', 'Stukov', 'Samuro', 'Sgt._hammer', 'Stitches', 'Sylvanas', 'Sonya', 'Tychus', 'Thrall', 'Tyrael', 'Tracer', 'Tyrande', 'The_butcher', 'Tassadar', 'The_Lost_Vikings', 'Uther', 'Valla', 'Varian', 'Valeera', 'Whitemane', 'Xul', 'Yrel', "Zul'jin", 'Zagara', 'Zeratul', 'Zarya']