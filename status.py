import schedule
import time
import requests
import sys


# declare vars

modes = ["EIGHT_ONE", "EIGHT_TWO", "FOUR_THREE", "FOUR_FOUR", "FOUR_FOUR_ULTIMATE", "NaM", "LOBBY"]
modesReplace = ["solo", "doubles", "3s", "4s", "dreams", "Mode not exist", "lobby"]
games = ["BEDWARS", "SKYWARS", "DUELS", "HOUSING"]
gamesReplace = ["Bedwars", "Skywars", "Duels", "Housing"]
# aight its provided now set "name" to the arg
name = sys.argv[2]
Key = sys.argv[1]

# test if name even provided lol
try:
	sys.argv[2]
except IndexError:
	raise SystemExit(f"Correct usage: {sys.argv[0]} <API KEY> <IGN>")
# okay passed: 



playerDetails = requests.get("https://playerdb.co/api/player/minecraft/{}".format(name)).json()

if (playerDetails["success"] == False):
	print("Unable to fetch player UUID.")
	raise SystemExit(f"No UUID.")
else:
	#yay success, now query hypixel api
	UUID = playerDetails["data"]["player"]["raw_id"]
	Name = playerDetails["data"]["player"]["username"]
	HyData = requests.get("https://api.hypixel.net/status?key={}&uuid={}".format(Key, UUID)).json()
	HyStats = requests.get("https://api.hypixel.net/player?key={}&name={}".format(Key, Name)).json()
	online = HyData["session"]["online"]


def bwStats(f):
	bwLevel = HyStats['player']['achievements']['bedwars_level']
	bwWinstreak = HyStats['player']['stats']['Bedwars']['winstreak']
	bwKills = HyStats['player']['stats']['Bedwars']['kills_bedwars']
	bwFinals = HyStats['player']['stats']['Bedwars']['final_kills_bedwars']
	bwBeds = HyStats['player']['stats']['Bedwars']['beds_broken_bedwars']

	bwStatsArray = [bwLevel, bwWinstreak, bwKills, bwFinals, bwBeds]
	
	return str(bwStatsArray[f])
	
# do i need to explain from here
if (online == False):
	print("UUID: " + UUID)
	print("Name: " + sys.argv[1])
	print("Status: Offline.")

else:
	game = HyData["session"]["gameType"]
	try:
		mode = HyData["session"]["mode"]
	except:
		mode = "NaM"
	try:
		modeIndex = modes.index(mode)
		gameModeReplaced = modesReplace[modeIndex]
	except:
		gameModeReplaced = "--"
	try:
		map = HyData["session"]["map"]
	except:
		map = "--"	
	
	gameIndex = games.index(game)
	gameReplaced = gamesReplace[gameIndex]

			
	print("UUID: " + UUID)
	print("Name: " + sys.argv[1])
	print("Status: Online! \n\n     Playing: {}".format(gameReplaced + " " + gameModeReplaced + " on map: " + map))
	queryUser = input("Query API for player stats? (y/n) ")
	if (queryUser == "y" or queryUser == "Y"):
		print("\nRetrieved player stats for {}.".format(name))
		print("   Level: " + bwStats(0))
		print("   Winstreak: " + bwStats(1))
		print("   Kills: " + bwStats(2))
		print("   Finals: " + bwStats(3))
		print("   Beds: " + bwStats(4))
		
	elif (queryUser == "n" or queryUser == "N"):
		pass
	else:
		"Not an input."
		