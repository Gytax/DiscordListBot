class DiscordList:
    def __init__(self, name, channel_id):
        self.channel_id = channel_id
        self.name = name
        self.items = []

    def add_item(self, item: str):
        self.items.append(item)

    def remove_item(self, item: str):
        if item in self.items:
            self.items.remove(item)

    def format(self) -> dict:
        return {
            'channel_id': self.channel_id,
            'name':       self.name,
            'items':      self.items
        }
