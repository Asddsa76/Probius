def aliases(hero):
	#The Wiki redirects correctly most upper/lowercase results, but not all acronyms
	if hero in ['aba']:
		return 'Abathur'
	elif hero in ['alex','alexstrazsa']:
		return 'Alexstrasza'
	elif hero in ['anub','beetle','anubarak']:
		return "Anub'arak"
	elif hero in ['art']:
		return 'Artanis'
	elif hero in ['lichking','lk']:
		return 'Arthas'
	elif hero in ['azmo']:
		return 'Azmodan'
	elif hero in ['bw']:
		return 'Brightwing'
	elif hero in ['cain']:
		return 'Deckard'
	elif hero in ['dva']:
		return 'D.Va'
	elif hero in ['etc']:
		return 'E.T.C.'
	elif hero in ['gaz']:
		return 'Gazlowe'
	elif hero in ['graymane','gm','grey']:
		return 'Greymane'
	elif hero in ['genji','best hero','mada mada','weaboo','i need healing','weeb']:
		return 'Genji'
	elif hero in ['guldan','gd']:
		return "Gul'dan"
	elif hero in ['bow genji']:
		return 'Hanzo'
	elif hero in ['ilidan']:
		return 'Illidan'
	elif hero in ['jo','jojo','joh']:
		return 'Johanna'
	elif hero in ['jr','junk']:
		return 'Junkrat'
	elif hero in ['kt','kael','kaelthas']:#He came to HotS first. Use KTZ for your beloved lich.
		return "Kael'thas"
	elif hero in ['ktz','kel','kelthuzad']:
		return "Kel'Thuzad"
	elif hero in ['ker','kerri']:
		return 'Kerrigan'
	elif hero in ['karazhim','khara']:
		return 'Kharazim'
	elif hero in ['leo']:
		return 'Leoric'
	elif hero in ['lili','li-li']:
		return 'Li_Li'
	elif hero in ['lm','liming','li-ming','li ming','ming']:
		return 'Li-Ming'
	elif hero in ['morales','medic','lt']:
		return 'Lt._Morales'
	elif hero in ['malf']:
		return 'Malfurion'
	elif hero in ['malganis',"mal'ganis",'mg']:
		return "Mal'Ganis"
	elif hero in ['medihv']:
		return 'Medivh'
	elif hero in ['meph']:
		return 'Mephisto'
	elif hero in ['mura']:
		return 'Muradin'
	elif hero in ['naz']:
		return 'Nazeebo'
	elif hero in ['probe']:
		return 'Probius'
	elif hero in ['rag']:
		return 'Ragnaros'
	elif hero in ['jimmy']:
		return 'Raynor'
	elif hero in ['reghar','rhegar']:
		return 'Rehgar'
	elif hero in ['misha']:
		return 'Rexxar'
	elif hero in ['sam','useless hero','overpowered piece of shit','grandpa','virgin']:
		return 'Samuro'
	elif hero in ['hammer','sgt']:
		return 'Sgt._Hammer'
	elif hero in ['sylv','sylvannas']:
		return 'Sylvanas'
	elif hero in ['tass']:
		return 'Tassadar'
	elif hero in ['tlv','vikings','the lost vikings','lost vikings']:
		return 'The_Lost_Vikings'
	elif hero in ['val']:
		return 'Valeera'
	elif hero in ['wm']:
		return 'Whitemane'
	elif hero in ['goat','space goat']:
		return 'Yrel'
	elif hero in ['zag']:
		return 'Zagara'
	elif hero in ['zera']:
		return 'Zeratul'
	elif hero in ["zj",'zul','zuljin']:
		return "Zul'jin"	
	return hero.capitalize()#Emoji pages are case sensitive

def abilityAliases(hero,name):#Spell hero with correct capitalization, then rest lowercase
	if hero=='Malfurion':
		if name in ['broccoli']:
			return 'vengeful'
	elif hero=='Genji':
		if name in ['dblade']:
			return 'dragonblade'
	elif hero=='Fenix':
		if name in ['aiur noon']:
			return 'salvo'
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
		elif name in ['tbs']:
			return 'three blade style'
		elif name in ['ws']:
			return 'wind strider'
		elif name in ['bmp']:
			return 'blademasters pursuit'
	return name
