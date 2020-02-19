import asyncio
import aiohttp
from aliases import *
from printFunctions import *

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def patchNotes(channel,text):
	splitText=text.split(',')
	hero=aliases(splitText.pop(0)).replace('ú','u').lower().translate({ord(i):None for i in "' _-."}).replace('thebutcher','butcher')
	if splitText:
		patchesAgo=int(splitText.pop(0))
	else:
		patchesAgo=1
	async with aiohttp.ClientSession() as session:
		page = await fetch(session, 'https://heroespatchnotes.com/hero/'+hero+'.html')
		patches=page.split('<h3>')
		patch=patches[patchesAgo]
		remove=['<small class="hidden-xs">','  ','<li>','<p>','<em>','</li>','</p>','</em>','</ul>','<blockquote>','</blockquote>']
		for i in remove:
			patch=patch.replace(i,'')
		output='**'+patch.split('<')[0]+'**\n'	#Date and version
		patch='>'.join(patch.split('<h4')[1].split('>')[1:])
		output+=patch.split('<')[0]+':'	#Type (bug fix, hero update)
		patch='>'.join(patch.split('>')[1:])
		patch=patch.split('</div>')[0]
		patch=patch.replace('\n',' ').replace('<strong>Developer Comment:</strong> ','\n***Developer Comment***: *').replace('<strong>','\n**').replace('</strong>',':** ').replace('<ul>',' ')
		output+=patch
		if 'Developer Comment' in output:
			output=output.strip()+'*'

		await printLarge(channel,output)