from dotamatch.api import Api


class LeagueListing(Api):
    url = "https://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001/"

    def leagues(self, **kwargs):
        result = self._get(**kwargs)
        for league in result['result']['leagues']:
            yield League(**league)

class LiveLeague(Api):
    url = "http://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/"

    def liveLeagues(self, **kwargs):
        result = self._get(**kwargs)
        #print(result)
        """
        #this is for testing purposes
        for i in result['result']['games']:
            print(i)
        #^^ it organized the information
        """
        for live in result['result']['games']:
            yield League(**live)

class League(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)