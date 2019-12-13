def extraD(abilities,hero):#Some heroes have weird text in D after < brackets. 
	if hero =='Samuro':
		abilities[0]+='\n'+"    **Advancing Strikes:** Basic Attacks against enemy Heroes increase Samuro's Movement Speed by 25% for 2 seconds."
	elif hero=='Sylvanas':
		abilities[0]+="\n**Banshee's Curse:** Basic Attacks infect enemies with Banshee's Curse for 3 seconds, stacking up to 3 times. Deal 25% more damage to enemies with 3 stacks."
	elif hero=='Tassadar':
		abilities[0]+='\n'+"    **Distortion Beam:** Tassadar's Basic Attack is a Distortion Beam that slows enemy units by 25%."
	elif hero=="Zul'jin":
		abilities[0]=abilities[0][:-14]+' **You Want Axe?** ***\n    ❢ Quest:*** Every 5 Basic Attacks against Heroes permanently increases Basic Attack damage by 1. '
		abilities[0]+='\n    ***? Reward:*** After attacking 75 times, Basic Attack range is increased by 1.1. '
		abilities[0]+='\n    ***? Reward:*** After attacking 150 times, Twin Cleave now revolves twice.'
	return abilities

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
	return ['Abathur', 'Alarak', 'Alexstrasza', 'Ana', 'Anduin', "Anub'arak", 'Artanis', 'Arthas', 'Auriel', 'Azmodan', 'Blaze', 'Brightwing', 'Cassia', 'Chen', 'Cho', 'Chromie', 'D.Va', 'Deathwing', 'Deckard', 'Dehaka', 'Diablo', 'E.T.C.', 'Falstad', 'Fenix', 'Gall', 'Garrosh', 'Gazlowe', 'Genji', 'Greymane', "Gul'dan", 'Hanzo', 'Illidan', 'Imperius', 'Jaina', 'Johanna', 'Junkrat', "Kael'thas", "Kel'Thuzad", 'Kerrigan', 'Kharazim', 'Leoric', 'Li-Ming', 'Li_Li', 'Lt._Morales', 'Lúcio', 'Lunara', 'Maiev', "Mal'Ganis", 'Malfurion', 'Malthael', 'Medivh', 'Mephisto', 'Muradin', 'Murky', 'Nazeebo', 'Nova', 'Orphea', 'Probius', 'Qhira', 'Ragnaros', 'Raynor', 'Rehgar', 'Rexxar', 'Samuro', 'Sgt._Hammer', 'Sonya', 'Stitches', 'Stukov', 'Sylvanas', 'Tassadar', 'The_Butcher', 'The_Lost_Vikings', 'Thrall', 'Tracer', 'Tychus', 'Tyrael', 'Tyrande', 'Uther', 'Valeera', 'Valla', 'Varian', 'Whitemane', 'Xul', 'Yrel', 'Zagara', 'Zarya', 'Zeratul', "Zul'jin"]

def addHotkeys(hero,abilities):
	if hero=='Abathur':
		hotkeys=['D','Q','QQ','QW','QE','W','R','R','Z']
	elif hero=='Greymane':
		hotkeys=['D','Q','Q','W','E','E','R','R']
	elif hero=='Leoric':
		hotkeys=['D','Q','DQ','W','DW','E','R','R']
	elif hero=='Tracer':
		hotkeys=['D','Q','W','E','R']
	elif hero in ['Ragnaros','Alexstrasza','Valeera']:
		hotkeys=['D','Q','DQ','W','DW','E','DE','R','R']
	elif hero=='The_Lost_Vikings':
		hotkeys=['D','1','2','3','4','R','R','Z']
	elif hero=='Gall':
		hotkeys=['D','Q','W','E','R','RR','R','1','Z']
	elif hero=='D.Va':
		hotkeys=['D','D','Q','W','E','E','R','R','Z']
	elif hero=='Blaze':
		hotkeys=['D','Q','W','E','R','RQ','R']
	elif hero=='Fenix':
		hotkeys=['D','Q','W','W','E','R','R']
	elif hero in ['Ana']:#2nd heroic has extra button
		hotkeys=['D','Q','W','E','R','R','RQ']
	elif hero=='Junkrat':
		hotkeys=['D','Q','W','E','R','RQ','RR','R']
	elif hero =='Nazeebo':#Varian has 3 heroics, Naz's Garry's stomp is listed under R
		hotkeys=['D','Q','W','E','R','RR','R']
	elif hero=='Varian':#Varian has 3 heroics, Naz's Garry's stomp is listed under R
		hotkeys=['D','Q','W','E','R','R','R']
	elif hero=='Uther':
		hotkeys=['D','Q','DQ','W','E','R','R']
	elif hero=='Stitches':
		hotkeys=['D','Q','1','W','E','R','R']
	elif hero=='Lt._Morales':
		hotkeys=['D','Q','QQ','W','E','R','R']
	elif hero=='Lunara':#Wisp relocate
		hotkeys=['D','Q','W','E','EE','R','R','Z']
	elif hero=='Chen':
		hotkeys=['D','Q','W','W','E','R','R','RQ','RW','RE']
	elif hero=='Tychus':
		hotkeys=['D','Q','RQ','W','RW','E','RE','R','R']
	elif hero=='Deathwing':
		hotkeys=['D','1','Q','DQ','W','W','DW','E','E','R','Z']
	elif len(abilities)>6:
		if hero in ['Medivh','Rehgar','Sgt._Hammer','Probius','Brightwing','Dehaka','Falstad','Lucio']:#Z/Mount
			hotkeys=['D','Q','W','E','R','R','Z']
		elif hero in ['Zeratul','Gazlowe','Nova','Whitemane',"Kel'Thuzad"]:#Wiki lists their extra last
			hotkeys=['D','Q','W','E','R','R','1']
		else:
			hotkeys=['D','1','Q','W','E','R','R']#Extra button
	else:
		hotkeys=['D','Q','W','E','R','R']#Normal hero
	i=0
	for hotkey in hotkeys:
		abilities[i]='**['+hotkey+']** '+abilities[i]
		i+=1
	return abilities