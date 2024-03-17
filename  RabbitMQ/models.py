from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    fullname = StringField(required=True, max_length=100)
    email = StringField(max_length=100)
    email_sent = BooleanField(default=False)

    def __str__(self):
        return f"Contact: {self.fullname}, Email: {self.email}, Email Sent: {self.email_sent}"
