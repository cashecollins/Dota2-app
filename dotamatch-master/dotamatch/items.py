from dotamatch.api import CachedApi


class GameItems(CachedApi):
    url = "https://api.steampowered.com/IEconDOTA2_570/GetGameItems/V001/?"

    def gameItems(self):
        results = self._get()
        game_items = {}
        for result in results['result']['items']:
            game_items[result['id']] = GameItem(result['id'], result['name'])
        CachedApi.cache = {}
        return game_items


class GameItem(object):
    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name