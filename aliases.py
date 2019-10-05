def aliases(hero):
	#The Wiki redirects correctly most upper/lowercase results, but not all acronyms
	if hero in ['aba']:
		hero='Abathur'
	elif hero in ['alex','alexstrazsa']:
		hero='Alexstrasza'
	elif hero in ['anub','beetle','anubarak']:
		hero="Anub'arak"
	elif hero in ['art']:
		hero='Artanis'
	elif hero in ['azmo']:
		hero='Azmodan'
	elif hero in ['bw']:
		hero='Brightwing'
	elif hero in ['cain']:
		hero='Deckard'
	elif hero in ['dva']:
		hero='D.Va'
	elif hero in ['etc']:
		hero='E.T.C.'
	elif hero in ['gaz']:
		hero='Gazlowe'
	elif hero in ['graymane','gm']:
		hero='Greymane'
	elif hero in ['best hero']:
		hero='Genji'
	elif hero in ['guldan','gd']:
		hero="Gul'dan"
	elif hero in ['bow genji']:
		hero='Hanzo'
	elif hero in ['ilidan']:
		hero='Illidan'
	elif hero in ['jo','jojo']:
		hero='Johanna'
	elif hero in ['jr','junk']:
		hero='Junkrat'
	elif hero in ['kt','kael','kaelthas']:#He came to HotS first. Use KTZ for your beloved lich.
		hero="Kael'thas"
	elif hero in ['ktz','kel','kelthuzad']:
		hero="Kel'Thuzad"
	elif hero in ['ker']:
		hero='Kerrigan'
	elif hero in ['karazhim','khara']:
		hero='Kharazim'
	elif hero in ['leo']:
		hero='Leoric'
	elif hero in ['lili','li-li']:
		hero='Li_Li'
	elif hero in ['lm','liming','li-ming','li ming','ming']:
		hero='Li-Ming'
	elif hero in ['morales','medic','lt']:
		hero='Lt._Morales'
	elif hero in ['malf']:
		hero='Malfurion'
	elif hero in ['malganis',"mal'ganis",'mg']:
		hero="Mal'Ganis"
	elif hero in ['medihv']:
		hero='Medivh'
	elif hero in ['meph']:
		hero='Mephisto'
	elif hero in ['mura']:
		hero='Muradin'
	elif hero in ['naz']:
		hero='Nazeebo'
	elif hero in ['probe']:
		hero='Probius'
	elif hero in ['rag']:
		hero='Ragnaros'
	elif hero in ['jimmy']:
		hero='Raynor'
	elif hero in ['reghar','rhegar']:
		hero='Rehgar'
	elif hero in ['misha']:
		hero='Rexxar'
	elif hero in ['sam','useless hero']:
		hero='Samuro'
	elif hero in ['hammer','sgt']:
		hero='Sgt._Hammer'
	elif hero in ['sylv','sylvannas']:
		hero='Sylvanas'
	elif hero in ['tass']:
		hero='Tassadar'
	elif hero in ['tlv','vikings','the lost vikings','lost vikings']:
		hero='The_Lost_Vikings'
	elif hero in ['val']:
		hero='Valeera'
	elif hero in ['wm']:
		hero='Whitemane'
	elif hero in ['goat','space goat']:
		hero='Yrel'
	elif hero in ['zag']:
		hero='Zagara'
	elif hero in ['zera']:
		hero='Zeratul'
	elif hero in ["zj",'zul','zuljin']:
		hero="Zul'jin"	
	else:
		hero=hero.capitalize()#Emoji pages are case sensitive
	return hero

def abilityAliases(tier):
	if tier in ['broccoli']:
		tier='vengeful'
	return tier