import pika
from faker import Faker
from mongoengine import connect
from models import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='contacts')

connect(
    db="my-mongoDB",
    host="mongodb+srv://<user>:<password>@my-mongodb.qlte4g6.mongodb.net/?"
         "retryWrites=true&w=majority&appName=my-mongoDB"
    )

fake = Faker()


def create_contact(num):
    for _ in range(num):
        name = fake.name()
        email = fake.email()
        contact = Contact(fullname=name, email=email)
        contact.save()

        channel.basic_publish(exchange='', routing_key='contacts', body=str(contact.id))
        print(f" [x] Sent {contact.id}")

    connection.close()


if __name__ == '__main__':
    create_contact(50)
