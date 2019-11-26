from miscFunctions import getHeroes

def aliases(hero):
	#The Wiki redirects correctly most upper/lowercase results, but not all acronyms
	hero=hero.lower().replace('_','').replace('.','').replace(' ','').replace("'","").replace('-','').replace('[','')#Trying to make this function idempotent
	if hero in ['slug','snail']:
		return 'Abathur'
	elif hero in ['alexstrazsa']:
		return 'Alexstrasza'
	elif hero in ['beetle','anubarak','bug']:
		return "Anub'arak"
	elif hero in ['zealot']:
		return 'Artanis'
	elif hero in ['lichking','lk']:
		return 'Arthas'
	elif hero in ['dunklord']:
		return 'Azmodan'
	elif hero in ['bw']:
		return 'Brightwing'
	elif hero in ['cain']:
		return 'Deckard'
	elif hero in ['amazon']:
		return 'Cassia'
	elif hero in ['dibbles']:
		return 'Diablo'
	elif hero in ['dw','destroyer','neltharion']:
		return 'Deathwing'
	elif hero in ['dva','gremlin']:#Showdown at Hanamura cinematic, never forget
		return 'D.Va'
	elif hero in ['etc']:
		return 'E.T.C.'
	elif hero in ['bird']:
		return 'Falstad'
	elif hero in ['garry','hellscream']:
		return 'Garrosh'
	elif hero in ['gazlord']:
		return 'Gazlowe'
	elif hero in ['graymane','gm']:
		return 'Greymane'
	elif hero in ['besthero','madamada','weaboo','ineedhealing','weeb']:
		return 'Genji'
	elif hero in ['guldan','gd']:
		return "Gul'dan"
	elif hero in ['bowgenji']:
		return 'Hanzo'
	elif hero in ['ilidan']:
		return 'Illidan'
	elif hero in ['dreadlord']:
		return "Jaina"
	elif hero in ['jojo','johnna','johannajoestar','crusader']:
		return 'Johanna'
	elif hero in ['jr']:
		return 'Junkrat'
	elif hero in ['kt','kaelthas']:#He came to HotS first. Use KTZ for your beloved lich.
		return "Kael'thas"
	elif hero in ['ktz','kelthuzad']:
		return "Kel'Thuzad"
	elif hero in ['karazhim']:
		return 'Kharazim'
	elif hero in ['janitor']:
		return 'Leoric'
	elif hero in ['lili','li-li']:
		return 'Li_Li'
	elif hero in ['lm','liming']:
		return 'Li-Ming'
	elif hero in ['medic','ltmorales']:
		return 'Lt._Morales'
	elif hero in ['deer','bambi','33elk']:
		return 'Lunara'
	elif hero in ['malganis','mg']:
		return "Mal'Ganis"
	elif hero in ['medihv','raven']:
		return 'Medivh'
	elif hero in ['fish']:
		return 'Murky'
	elif hero in ['witchdoctor']:
		return 'Nazeebo'
	elif hero in ['voreloli']:
		return 'Orphea'
	elif hero in ['probe']:
		return 'Probius'
	elif hero in ['jimmy']:
		return 'Raynor'
	elif hero in ['reghar','rhegar']:
		return 'Rehgar'
	elif hero in ['misha']:
		return 'Rexxar'
	elif hero in ['worsthero','uselesshero','grandpa']:
		return 'Samuro'
	elif hero in ['sgthammer']:
		return 'Sgt._Hammer'
	elif hero in ['barbarian']:
		return 'Sonya'
	elif hero in ['stiches']:
		return 'Stitches'
	elif hero in ['sylvannas']:
		return 'Sylvanas'
	elif hero in ['thebutcher']:
		return 'The_Butcher'
	elif hero in ['tlv','thelostvikings','lostvikings']:
		return 'The_Lost_Vikings'
	elif hero in ['wm']:
		return 'Whitemane'
	elif hero in ['goat','spacegoat']:
		return 'Yrel'
	elif hero in ['zerathul']:
		return 'Zeratul'
	elif hero in ["zj",'zuljin']:
		return "Zul'jin"

	for i in getHeroes():#Substring
		if hero in i.lower():
			return i
	return hero.capitalize().replace(' ','_')#Emoji pages are case sensitive

def abilityAliases(hero,name):#Spell hero with correct capitalization, then rest lowercase
	if hero=='Cassia':
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
	elif hero=='Lt._Morales':
		if name=='stimdrone':
			return 'stim drone'
	elif hero=='Malfurion':
		if name in ['broccoli']:
			return 'vengeful'
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
			return 'blademasters pursuit'
	elif hero=='Zeratul':
		if name in ['za warudo','vp']:
			return 'void prison'
	return name