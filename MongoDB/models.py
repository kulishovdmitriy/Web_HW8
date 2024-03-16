from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

connect(
    db="my-mongoDB",
    host="mongodb+srv://djo-developer:52628271@my-mongodb.qlte4g6.mongodb.net/?"
         "retryWrites=true&w=majority&appName=my-mongoDB"
    )


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=70)
    born_location = StringField(max_length=100)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, required=CASCADE)
    tags = ListField(StringField(max_length=40))
    quote = StringField()
    meta = {"collection": "quotes"}
