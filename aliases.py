def aliasTrim(hero):
	return hero.lower().replace('_','').replace('.','').replace(' ','').replace("'","").replace('-','').replace('[','').replace('\n','')

def aliases(hero):
	hero=aliasTrim(hero)
	aliasDict={
	'Abathur':['slug','snail','malarialarva'],
	'Alarak':['highlord','sith','sithlord','edgelord'],
	'Alexstrasza':['alexstrazsa','dragonmom','alextraza','alexstraza'],
	"Anub'arak":['beetle','anubarak','bug'],
	'Artanis':['zealot'],
	'Arthas':['lichking','lk'],
	'Azmodan':['dunklord','azmodunk'],
	'Blaze':['firebat'],
	'Brightwing':['bw','faeriedragon'],
	'Deckard':['cain','deckardcain'],
	'Cassia':['amazon'],
	'Chromie':['sandgnome','sandhitler'],
	'Dehaka':['yoshi'],
	'Diablo':['dibbles'],
	'Deathwing':['dw','destroyer','neltharion'],
	'D.Va':['dva','gremlin'],
	'E.T.C.':['etc','cow'],
	'Falstad':['bird','falsedad'],
	'Garrosh':['garry','hellscream'],
	'Gazlowe':['gazlord','gazlove'],
	'Greymane':['graymane','gm'],
	'Genji':['besthero','lowestwinrate','madamada','weaboo','ineedhealing','weeb'],
	'Cho':['cg','chogall'],
	"Gul'dan":['guldan','gd','ghouldan','daniel','warlock','guldangerous'],
	'Hanzo':['bowgenji'],
	'Illidan':['ilidan','illidumb'],
	"Jaina":['dreadlord'],
	'Johanna':['jojo','johnna','johannajoestar','crusader'],
	'Junkrat':['jr'],
	"Kael'thas":['kt','kaelthas'],#He came to HotS first. Use KTZ for your beloved lich.
	"Kel'Thuzad":['ktz','kelthuzad','lich'],
	'Kerrigan':['sarah'],
	'Kharazim':['karazhim','monk','karazim'],
	'Leoric':['janitor'],
	'Li_Li':['lili','li-li'],
	'Li-Ming':['lm','liming','wizard'],
	'Lt._Morales':['medic','ltmorales'],
	'Lúcio':['dj','lucio'],
	'Lunara':['deer','bambi','33elk','lulnara'],
	'Maiev':['warden','mommywarden'],
	"Mal'Ganis":['malganis','mg','turtle'],
	'Medivh':['medihv','raven','memedivh'],
	'Mei':['mai','may','mey'],
	'Murky':['fish','murloc'],
	'Nazeebo':['witchdoctor','brap','aieee'],
	'Orphea':['voreloli','nexusoc'],
	'Probius':['probe'],
	'Raynor':['jimmy'],
	'Ragnaros':['firelord'],
	'Rehgar':['reghar','rhegar','wolf','shaman'],
	'Rexxar':['misha'],
	'Samuro':['worsthero','uselesshero','grandpa','blademaster'],
	'Sgt._Hammer':['sgthammer'],
	'Sonya':['barbarian'],
	'Stitches':['stiches','stitces','fatty'],
	'Sylvanas':['sylvannas'],
	'Tassadar':['executor','templar'],
	'The_Butcher':['thebutcher'],
	'The_Lost_Vikings':['tlv','thelostvikings','lostvikings'],
	'Tracer':['lena','oxton','lenaoxton','mosquito'],
	'Tyrael':['tyrone','tyreal'],
	'Valla':['demonhunter','vala'],
	'Whitemane':['wm'],
	'Xul':['necromancer'],
	'Yrel':['goat','spacegoat'],
	'Zeratul':['zerathul'],
	"Zul'jin":["zj",'zuljin','troll','luljin']}
	for i in aliasDict:
		if hero in aliasDict[i]:
			return i
		
	from printFunctions import getHeroes
	for i in getHeroes():#Substring
		if hero in aliasTrim(i):
			return i
	return hero.capitalize().replace(' ','_')#Emoji pages are case sensitive

def abilityAliases(hero,name):#Spell hero with correct capitalization, then rest lowercase
	abilityAliasDict={
	'Ana':{'nano boost':['nanoboost']},
	'Anduin':{'leap of faith':['lifegrip']},
	'Azmodan':{'demonic invasion':['sieging wrath']},
	'Cassia':{'ball lightning':['volleyball','tetherball']},
	'Fenix':{'purification salvo':['aiur noon']},
	'E.T.C.':{'loud speakers':['lewd speakers']},
	'Genji':{'dragonblade':['dblade'],
		'dragon claw':['dc','claw']},
	'Hanzo':{'play of the game':['potg']},
	'Leoric':{'drain hope':['spooky hand']},
	'Lúcio':{'soundwave':['boop']},
	'Lt._Morales':{'stim drone':['stimdrone']},
	'Malfurion':{'vengeful roots':['broccoli'],
		'emerald dreams':['sleepy lawn']},
	"Mal'Ganis":{'dark conversion':['lifeswap']},
	'Nova':{'precision strike':['walmart lava wave','discount lava wave']},
	'Ragnaros':{'living meteor':['meatball']},
	'Samuro':{'press':['pta','press the advantage'],
		'merciless':['mcs'],
		'way of the wind':['wotw'],
		'way of illusion':['woi'],
		'way of the blade':['wotb'],
		'one with the wind':['owtw'],
		'phantom pain':['pp'],
		'burning blade':['bb'],
		'crushing blows':['cb'],
		'illusion master':['im'],
		'bladestorm':['bs'],
		'mirrored steel':['ms'],
		'shukuchi':['sh'],
		'kawarimi':['kw'],
		'harsh winds':['hw'],
		'dance of death':['dod'],
		'three blade style':['tbs','3bs'],
		'wind strider':['ws'],
		'pursuit':['bmp']},
	'Thrall':{'crash lightning':['trash lightning']},
	'Tyrael':{'sword of justice':['swordhole'],
		'judgment':['judgement']},
	'Zeratul':{'void prison':['za warudo','vp']}}
	try:
		for ability in abilityAliasDict[hero].keys():
			if name in abilityAliasDict[hero][ability]:
				return ability
	except:pass
	return name