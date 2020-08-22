from miscFunctions import getHeroes

def aliasTrim(hero):
	return hero.lower().replace('_','').replace('.','').replace(' ','').replace("'","").replace('-','').replace('[','').replace('\n','')

def aliases(hero):
	#The Wiki redirects correctly most upper/lowercase results, but not all acronyms
	hero=aliasTrim(hero)
	if hero in ['slug','snail','malarialarva']:
		return 'Abathur'
	elif hero in ['highlord','sith','sithlord','edgelord']:
		return 'Alarak'
	elif hero in ['alexstrazsa','dragonmom']:
		return 'Alexstrasza'
	elif hero in ['beetle','anubarak','bug']:
		return "Anub'arak"
	elif hero in ['zealot']:
		return 'Artanis'
	elif hero in ['lichking','lk']:
		return 'Arthas'
	elif hero in ['dunklord','azmodunk']:
		return 'Azmodan'
	elif hero in ['firebat']:
		return 'Blaze'
	elif hero in ['bw','faeriedragon']:
		return 'Brightwing'
	elif hero in ['cain']:
		return 'Deckard'
	elif hero in ['amazon']:
		return 'Cassia'
	elif hero in ['sandgnome','sandhitler']:
		return 'Chromie'
	elif hero in ['yoshi']:
		return 'Dehaka'
	elif hero in ['dibbles']:
		return 'Diablo'
	elif hero in ['dw','destroyer','neltharion']:
		return 'Deathwing'
	elif hero in ['dva','gremlin']:
		return 'D.Va'
	elif hero in ['etc','cow']:
		return 'E.T.C.'
	elif hero in ['bird']:
		return 'Falstad'
	elif hero in ['garry','hellscream']:
		return 'Garrosh'
	elif hero in ['gazlord']:
		return 'Gazlowe'
	elif hero in ['graymane','gm']:
		return 'Greymane'
	elif hero in ['besthero','lowestwinrate','madamada','weaboo','ineedhealing','weeb']:
		return 'Genji'
	elif hero in ['cg','chogall']:
		return 'Cho'
	elif hero in ['guldan','gd','ghouldan','daniel','warlock','guldangerous']:
		return "Gul'dan"
	elif hero in ['bowgenji']:
		return 'Hanzo'
	elif hero in ['ilidan','illidumb']:
		return 'Illidan'
	elif hero in ['dreadlord']:
		return "Jaina"
	elif hero in ['jojo','johnna','johannajoestar','crusader']:
		return 'Johanna'
	elif hero in ['jr']:
		return 'Junkrat'
	elif hero in ['kt','kaelthas']:#He came to HotS first. Use KTZ for your beloved lich. 
	# no u, fake kt
		return "Kael'thas"
	elif hero in ['ktz','kelthuzad','lich']:
		return "Kel'Thuzad"
	elif hero in ['sarah']:
		return 'Kerrigan'
	elif hero in ['karazhim','monk']:
		return 'Kharazim'
	elif hero in ['janitor']:
		return 'Leoric'
	elif hero in ['lili','li-li']:
		return 'Li_Li'
	elif hero in ['lm','liming','wizard']:
		return 'Li-Ming'
	elif hero in ['medic','ltmorales']:
		return 'Lt._Morales'
	elif hero in ['dj','lucio']:
		return 'Lúcio'
	elif hero in ['deer','bambi','33elk']:
		return 'Lunara'
	elif hero in ['malganis','mg','turtle']:
		return "Mal'Ganis"
	elif hero in ['medihv','raven']:
		return 'Medivh'
	elif hero in ['mai','may','mey']:
		return 'Mei'
	elif hero in ['fish','murloc']:
		return 'Murky'
	elif hero in ['witchdoctor','brap','aieee']:
		return 'Nazeebo'
	elif hero in ['voreloli','nexusoc']:
		return 'Orphea'
	elif hero in ['probe']:
		return 'Probius'
	elif hero in ['jimmy']:
		return 'Raynor'
	elif hero in ['firelord']:
		return 'Ragnaros'
	elif hero in ['reghar','rhegar']:
		return 'Rehgar'
	elif hero in ['misha']:
		return 'Rexxar'
	elif hero in ['worsthero','uselesshero','grandpa','blademaster']:
		return 'Samuro'
	elif hero in ['sgthammer']:
		return 'Sgt._Hammer'
	elif hero in ['barbarian']:
		return 'Sonya'
	elif hero in ['stiches','stitces']:
		return 'Stitches'
	elif hero in ['sylvannas']:
		return 'Sylvanas'
	elif hero in ['executor','templar']:
		return 'Tassadar'
	elif hero in ['thebutcher']:
		return 'The_Butcher'
	elif hero in ['tlv','thelostvikings','lostvikings']:
		return 'The_Lost_Vikings'
	elif hero in ['lena','oxton','lenaoxton','mosquito']:
		return 'Tracer'
	elif hero in ['tyrone','tyreal']:
		return 'Tyrael'
	elif hero in ['demonhunter','vala']:
		return 'Valla'
	elif hero in ['wm']:
		return 'Whitemane'
	elif hero in ['necromancer']:
		return 'Xul'
	elif hero in ['goat','spacegoat']:
		return 'Yrel'
	elif hero in ['zerathul']:
		return 'Zeratul'
	elif hero in ["zj",'zuljin','troll']:
		return "Zul'jin"

	for i in getHeroes():#Substring
		if hero in aliasTrim(i):
			return i
	return hero.capitalize().replace(' ','_')#Emoji pages are case sensitive

def abilityAliases(hero,name):#Spell hero with correct capitalization, then rest lowercase
	if hero=='Azmodan':
		if name in ['sieging wrath']:
			return 'demonic invasion'
	elif hero=='Cassia':
		if name in ['volleyball','tetherball']:
			return 'ball lightning'
	elif hero=='Fenix':
		if name in ['aiur noon']:
			return 'salvo'
	elif hero=='Genji':
		if name in ['dblade']:
			return 'dragonblade'
		elif name in ['dc','claw']:
			return 'dragon claw'
	elif hero=='Leoric':
		if name=='spooky hand':
			return 'Drain Hope'
	elif hero=='Lúcio':
		if name=='boop':
			return 'soundwave'
	elif hero=='Lt._Morales':
		if name=='stimdrone':
			return 'stim drone'
	elif hero=='Malfurion':
		if name in ['broccoli']:
			return 'vengeful roots'
	elif hero=='Samuro':
		if name in ['pta','press the advantage']:
			return 'press'
		elif name in ['mcs']:
			return 'merciless'
		elif name in ['wotw']:
			return 'way of the wind'
		elif name in ['woi']:
			return 'way of illusion'
		elif name in ['wotb']:
			return 'way of the blade'
		elif name in ['owtw']:
			return 'one with the wind'
		elif name in ['pp']:
			return 'phantom pain'
		elif name in ['bb']:
			return 'burning blade'
		elif name in ['cb']:
			return 'crushing blows'
		elif name in ['im']:
			return 'illusion master'
		elif name in ['bs']:
			return 'bladestorm'
		elif name in ['ms']:
			return 'mirrored steel'
		elif name in ['sh']:
			return 'shukuchi'
		elif name in ['kw']:
			return 'kawarimi'
		elif name in ['hw']:
			return 'harsh winds'
		elif name in ['dod']:
			return 'dance of death'
		elif name in ['tbs','3bs']:
			return 'three blade style'
		elif name in ['ws']:
			return 'wind strider'
		elif name in ['bmp']:
			return 'pursuit'
	elif hero=='Tyrael':
		if name in ['swordhole']:
			return 'sword of justice'
		if name in ['judgement']:
			return 'judgment'
	elif hero=='Zeratul':
		if name in ['za warudo','vp']:
			return 'void prison'
	return name