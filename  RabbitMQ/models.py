from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    full_name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=100)
    email_sent = BooleanField(default=False)

    def __str__(self):
        return f"Contact: {self.full_name}, Email: {self.email}, Email Sent: {self.email_sent}"
