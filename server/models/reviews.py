import mongoengine


class Review(mongoengine.EmbeddedDocument):
    rating = mongoengine.FloatField(default = 0)
    comment_text = mongoengine.StringField()
    images = mongoengine.ListField(mongoengine.StringField())
    videos = mongoengine.ListField(mongoengine.StringField())
