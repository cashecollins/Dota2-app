"""
This example shows how you could count up the heroes used by a player.
"""
import pprint
import time
import datetime
from dotamatch.history import MatchHistory, MatchHistoryBySequenceNum
from dotamatch.players import PlayerSummaries
from dotamatch.heroes import Heroes
from dotamatch.matches import MatchDetails, Match
from dotamatch.dotadictionary import h
from dotamatch.leagues import LeagueListing, LiveLeague
from dotamatch.teams import Teams
from dotamatch.items import GameItems

print("")
#global test values
cashe = 99244105
kyson = 103094836
ursa = 2422865073
tb = 2418453237
#cashe's special key
key = "DCC68441A828EA75DB2D320764869026"
history = MatchHistory(key)
historySequence = MatchHistoryBySequenceNum(key)
player_summaries = PlayerSummaries(key)
heroes = Heroes(key)
details = MatchDetails(key)
summary = PlayerSummaries(key)
teams = Teams(key)
game_items = GameItems(key)


# gives the hero usage for the last 100 games#
def heroUsage(steamID):
    """Gets the number of times that a user has played
    each hero in the last 100 games"""
    heroes_played = {}
    for match in history.matches(account_id=steamID):
        player = match.player(steamID)
        hero = heroes.heroes()[player['hero_id']].name
        heroes_played[hero] = heroes_played.get(hero, 0) + 1
    pprint.pprint(heroes_played)

# API Functions
def getHeroName(id):
    """returns the heroes friendly name from their id"""
    hero_name = heroes.heroes()[id]
    friendly_hero_name = str(hero_name)[14:]
    friendly_hero_name = friendly_hero_name.replace("_", " ")
    return friendly_hero_name.title()
def getPlayerName(steamID):
    """returns the players gamer name"""
    l = list(summary.players(steamID))
    if l:
        return l[0]
    else:
        return "Private Account Faggot Face"
def getItemName(id):
    """returns the items friendly name from their id"""
    item_name = game_items.gameItems()[id]
    friendly_item_name = str(item_name)[5:]
    friendly_item_name = friendly_item_name.replace("_", " ")
    return friendly_item_name.title()
def getPlayerMatches(steamID):
    """ returns a list of most recent games for player steamID, including:
    (start_time, match_id, players, dire_team_id, radiant_team_id, match_seq_num) """
    games = []
    matches = 0
    lastMatch = 0
    date = 0
    for i in range(5):
        for match in history.matches(account_id=steamID, matches_requested=500, start_at_match_id=lastMatch):
            matches += 1
            player = match.player(steamID)
            games.append(match)
            lastMatch = match.match_id
            date = match.start_time
            print(match.__dict__)
        print(matches)
    for j in range(5):
        for match2 in history.matches(account_id=steamID, matches_requested=500, start_at_match_id=lastMatch, max_date=date):
            matches += 1
            player = match2.player(steamID)
            games.append(match2)
            lastMatch = match2.match_id
            date = match2.start_time
            print(date)
            print(match2.__dict__)
        print(matches)
    print(lastMatch)
    getMatchDetails(lastMatch)
    return games
def getMatchesBySequence(steamID):
    """ returns a list of most recent games for player steamID, including:
    (start_time, match_id, players, dire_team_id, radiant_team_id, match_seq_num) """
    games = []
    matches = 0
    lastMatch = 0
    for i in range(2):
        for match in historySequence.matches(account_id=steamID, start_at_match_seq_num=lastMatch):
            matches += 1
            #player = match.player(steamID)
            games.append(match)
            lastMatch = match.match_seq_num
            print(match.__dict__)
        print(matches)
    print(lastMatch)
    getMatchDetails(lastMatch)
    return games
def getMatchDetails(match_id):
    """gets a match with who's id is match_id and right now
    prints out some cool information including: parent,
    match_id, flags, dire_score, radiant_score,
    tower_status_radiant, tower_status_dire, positive_votes,
    negative_votes, leagueid, barracks_status_radiant,
    barracks_status_dire, duration, lobby_type, human_players,
    start_time, first_blood_time, engine, players, cluster,
    game_mode"""
    game = details.match(match_id)
    print(game.__dict__.keys())
    if match_id:
        if details.match(match_id).players != []:
            if game.radiant_win:
                print("Radiant Victory!")
            else:
                print("Dire Victory!")
            print("Radiant " + str(game.radiant_score) + " - " + str(game.dire_score) + " Dire")
            print("")
            """ get player stats for match """
            for player in game.players:
                #print(player)
                invent = []
                inventory = []
                for i in range(6):
                    invent.append(int(player['item_'+str(i)]))
                for j in invent:
                    if j == 0:
                        inventory.append("too poor, no item")
                    else:
                        inventory.append(getItemName(j))
                print("Name: " + str(getPlayerName(int(player['account_id']))))
                print("Hero: " + getHeroName(player['hero_id']))
                print(inventory)
                print("Level: " + str(player['level']))
                print("K/D/A: " + str(player['kills']) + "/" + str(player['deaths']) + "/" + str(player['assists']))
                print("GPM: " + str(player['gold_per_min']))
                print("XPM: " + str(player['xp_per_min']))
                print("Last hits: " + str(player['last_hits']))
                print("Denies: " + str(player['denies']))
                print("")


# ============================================ #
# =========== Tournament Functions =========== #
# ============================================ #
pro = LeagueListing(key)
livepro = LiveLeague(key)
def getLeagueInfo(leagueName):
    """gets the information of a specific name, and creates
    the leaguelist that holds all of the leagues and their
    id numbers that are used in the getLiveLeague() function"""
    leaguelist = []
    for league in pro.leagues():
        leaguelist.append({'name':str(league.name), 'id':league.leagueid})
        if league.name[11:] == leagueName:

            print("")
            print("Description: " + str(league.description))
            print("League id: " + str(league.leagueid))
            print("Item Def: " + str(league.itemdef))
            print("Tournament URL: " + str(league.tournament_url))
            print("Tournament Name: " + str(league.name[11:]))
            print("")
            break

    getLiveLeagues(leaguelist)
def getLiveLeagues(leaguelist):
    """gets a live league that is tier 3 (a major) and prints off all of the
    information including dire and radiant team players and heroes as well as
    some of the player stats (K/D/A, gpm, xpm, net_worth, etc.) also the match
    stats, such as team_name, radiant and dire score, and the series 2/3"""
    # Getting live league infor for leagues with a league_tier of 3
    leagueInfo = []
    x = -1
    #SUPER IMPORTANT, live IS 1 MATCH FROM 1 LEAGUE AND EVERYTHING IS FROM THAT MATCH
    for live in livepro.liveLeagues():
        radiant = []
        dire = []
        #loop through all the league match players
        for i in range(len(live.players)):
            #loop through the herodictionary
            for hdict in h:
                #get the hero name from id
                if hdict['id'] == live.players[i]['hero_id']:
                    if live.players[i]['team'] == 0:
                        radiant.append({'name':live.players[i]['name'], 'hero':hdict['localized_name'], 'hero_id':hdict['id']})
                    elif live.players[i]['team'] == 1:
                        dire.append({'name':live.players[i]['name'], 'hero':hdict['localized_name'], 'hero_id':hdict['id']})
        # Get League Name
        istourny = False
        exists = False
        for i in leaguelist:
            if live.league_id == i['id'] and live.league_tier == 3:
                """
                # ============THIS IS MY CRAZY LEAGUE FILE WRITER ============== #
                f = open('leagueInfo.txt', 'r')
                leagueInfo = f.read()
                existsName = False
                existsNumber = False
                y = -1
                name = i['name'][11:]
                number = str(live.match_id)
                with open('leagueInfo.txt','r') as f:
                    for line in f:
                        for word in line.split():
                           if word == name+':':
                                existsName = True
                           elif word == number:
                                existsNumber = True
                        break
                    if not existsName and not existsNumber:
                        f = open('leagueInfo.txt', 'a')
                        f.write(name+': ')
                        f.write(number+" ")
                        f.close()
                    elif existsName and not existsNumber:
                        f = open('leagueInfo.txt','a')
                        f.write(" " + number + " ")
                        f.close()


                for j in leagueInfo:
                    if j == word+':':
                        f.close()
                        f = open('leagueInfo.txt', 'a')
                        f.write(number + ', ')
                        f.close()
                f.close()
                # ========================================================== #
                """
                # prints the league name
                print("")
                istourny = True
                if istourny:
                    print(i['name'][11:])
                    print("Game: " + ' ' + str(live.game_number) + "/" + str(live.stage_name[-1]))
                    game_time = time.strftime('%H:%M:%S', time.gmtime(live.scoreboard['duration']))
                    print(game_time)
                    print(("Radiant " + str(getScore(live, 'radiant')) + " - " + str(getScore(live, 'dire')) + " Dire"))
                    #print(live.scoreboard)
                    print("")
                else:
                    print("No tournament games are live right now!")

                break

        if istourny:
            # ========================================================================= #
            # ================== Radiant Team and Current Stats ======================= #
            # ========================================================================= #
            print("RADIANT" + " " + getTeam(live)[0])
            side = 'radiant'
            print("Radiant Bans: " + str(getBans(live, side)))
            print("Radiant Picks: " + str(getPicks(live, side)))
            print("Score: " + str(getScore(live, side)))
            print("")
            getPlayerStats(live, side, radiant) #adds all radiant players stats to the radiant[] player dictionary
            for player in radiant:
                print(player['name'] + ": " + player['hero'])
                # print("Quick Stats: " + str(player))
                print("K/D/A: " + str(player['kills']) + "/" + str(player['death']) + "/" + str(player['assists']))
                print("GPM: " + str(player['gold_per_min']))
                print("XPM: " + str(player['xp_per_min']))
                print("Last Hits: " + str(player['last_hits']))
                print("Denies: " + str(player['denies']))
                print("Net Worth: " + str(player['net_worth']))
                print("Current Gold: " + str(player['gold']))
                print("")

            # ====================================================================== #
            # ================== Dire Team and Current Stats ======================= #
            # ====================================================================== #
            print(" ")
            print("DIRE" + " " + getTeam(live)[1])
            side = 'dire'
            print("Dire Bans: " + str(getBans(live, side)))
            print("Dire Picks: " + str(getPicks(live, side)))
            print("Score: " + str(getScore(live, side)))
            getPlayerStats(live, side, dire) #adds all dire player stats to the dire[] dictionary
            for player in dire:
                print(player['name'] + ": " + player['hero'])
                print("K/D/A: " + str(player['kills']) + "/" + str(player['death']) + "/" + str(player['assists']))
                print("GPM: " + str(player['gold_per_min']))
                print("XPM: " + str(player['xp_per_min']))
                print("Last Hits: " + str(player['last_hits']))
                print("Denies: " + str(player['denies']))
                print("Net Worth: " + str(player['net_worth']))
                print("Current Gold: " + str(player['gold']))
                print("")
            print(" ")
            istourny = False
def getLeagueMatches(l_id):
    """ Gets only league matches for a sertain league_id from
    getTournamentGames() and returns the match details of all
    of the matches from that tournament """
    """
    matches = []
    with open('leagueInfo.txt', 'r') as f:
        for line in f:
            for word in line.split():
                matches.append(word)
        f.close()
        for i in range(len(matches)):
            if i != 0:
                getMatchDetails(matches[i])
    """
    for match in getTournamentGames(l_id):
        # print(match.__dict__)
        # This will get you the team_id, which is super cool
        # match.dire_team_id or match.radiant_team_id
        # This prints the names of all of the pro teams
        # print(teams.teams())
        getMatchDetails(match.match_id)
def getTournamentGames(l_id):
    """returns a list of match objects all from a specific tournament from
    its league_id as a list in list games"""
    games = []
    # gets all of the matches from a specific tournament l_id and appends them to games which is returned
    for match in history.matches(tournament_games_only=1, league_id=l_id):
        game = match
        games.append(game)
    return games
# logic, helper functions for getLiveLeagues()
def getScore(live, side):
    return live.scoreboard[side]['score']
def getTeam(live):
    return [live.radiant_team['team_name'], live.dire_team['team_name']]
def getBans(live, side):
    return bans(live.scoreboard[side])
def getPicks(live, side):
    return picks(live.scoreboard[side])
def getPlayerStats(live, side, team):
    for player in live.scoreboard[side]['players']:
        for i in team:
            if player['hero_id'] == i['hero_id']:
                i['gold_per_min'] = player['gold_per_min']
                i['net_worth'] = player['net_worth']
                i['gold'] = player['gold']
                i['last_hits'] = player['last_hits']
                i['denies'] = player['denies']
                i['kills'] = player['kills']
                i['death'] = player['death']
                i['assists'] = player['assists']
                i['xp_per_min'] = player['xp_per_min']
                i['player_slot'] = player['player_slot']
                i['position_x'] = player['position_x']
                i['position_y'] = player['position_y']
                i['ultimate_cooldown'] = player['ultimate_cooldown']
                i['account_id'] = player['account_id']
                i['hero_id'] = player['hero_id']
                i['ultimate_state'] = player['ultimate_state']


#LogicalFunctions
def bans(banlist):
    names = []
    for ban in banlist['bans']:
        names.append(getHeroName(ban['hero_id']))
    return names
def picks(picklist):
    names = []
    for pick in picklist['picks']:
        names.append(getHeroName(pick['hero_id']))
    return names

def main():
    #heroUsage(kyson)
    #getLeagueInfo("The_Manila_Major_2016")
    #getMatchDetails(tb)
    #getLeagueMatches(4479)
    #getPlayerName(cashe)
    #getPlayerMatches(kyson)
    #getMatchesBySequence(cashe)
    #print(getHeroName(45))
    #print(getItemName(71))


main()



# | steamname: CA$HE
# |  steam3ID: [U:1:99244105]
# | steamID32: STEAM_0:1:49622052
# | steamID64: http://steamcommunity.com/profiles/76561198059509833
# | customURL: http://steamcommunity.com/id/cashecollins
# |  steamrep: http://steamrep.com/profiles/76561198059509833