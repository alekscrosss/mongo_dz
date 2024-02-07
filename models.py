from mongoengine import Document, StringField, ListField, ReferenceField, connect, BooleanField


connect(db="mbd",
        host="mongodb+srv://alex19951107:qmmThh9ChCKzpXMs@cluster0.spnqudz.mongodb.net/mbd?retryWrites=true&w=majority")


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField()
    message_sent = BooleanField(default=False)
    preferred_contact_method = StringField(choices=['email', 'sms'])
