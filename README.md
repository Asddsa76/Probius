# Probius

A HotS Discord bot. Call in Discord with [hero/modifier], where modifier is hotkey or talent tier. Data is pulled from HotS wiki. 

Written in Python 3.5.3 and running on a Raspberry Pi 3 B+

Project started on 14/9-2019

# File description

probius: The main file that calls all the other files

aliases: Spellcheck and alternate names for heroes

trimBrackets: Trims < from text

printFunctions: The functions that output the things to print

heroPage: The function that imports the hero pages

emojis: Emojis

miscFunctions: Edge cases and help message

getDiscordToken: The token is in an untracked file because this is a public Github repo

elitesparkleGuide: Hero guides

downloadHero: Downloads a hero page. Not called by main loop, must be run after each patch.

Example usage:
![bilde](https://user-images.githubusercontent.com/49531523/109698466-b7da2a00-7b8f-11eb-8b5a-d20a3daf22a3.png)
