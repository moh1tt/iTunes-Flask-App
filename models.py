class iTunes:
    def __init__(self, id, artist, title, price, album):
        self.id = id
        self.artist = artist
        self.title = title
        self.price = price
        self.album = album

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'artist': self.artist,
            'title': self.title,
            'price': self.price,
            'album': self.album

        }
