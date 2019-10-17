from urllib.request import urlopen

def rotation():
	page=[i.strip().decode('utf-8') for i in urlopen('https://nexuscompendium.com/currently.php')]
	rotationHeroes=[]
	for line in page:
		if 'Week of ' in line:
			lineIndex=line.index('Week of ')
			output='**Free rotation w'+line[lineIndex+1:lineIndex+18]+':**\n'
		if '<td valign' in line:
			rotationHeroes.append(line[line.index('title="')+7:line.index('" alt')])
			if len(rotationHeroes)==14:
				break
	output+=', '.join(rotationHeroes[:7])+'\n'
	output+=', '.join(rotationHeroes[8:])
	return output