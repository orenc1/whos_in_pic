class Person:
    def __init__(self, pid, name, url, category):
        self.id = pid
        self.name = name
        self.url = url
        self.category = category
        self.image_url = None
        self.options = None

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'category': self.category,
            'image_url': self.image_url,
            'options': self.options,
        }