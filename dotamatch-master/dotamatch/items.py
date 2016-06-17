from dotamatch.api import CachedApi


class Items(CachedApi):
    url = "https://api.steampowered.com/IEconDOTA2_570/GetGameItems/V001/?"

    def items(self):
        results = self._get()
        items = {}
        for result in results['result']['items']:
            items[result['id']] = Item(result['id'], result['name'])
        return items


class Item(object):
    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name