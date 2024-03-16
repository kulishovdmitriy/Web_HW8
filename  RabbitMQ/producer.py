import pika
from faker import Faker
from mongoengine import connect
from models import Contact

# З'єднання з RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='contacts')

# Підключення до MongoDB
connect('contacts_database')

# Генерування та зберігання фейкових контактів
fake = Faker()
for _ in range(10):
    name = fake.name()
    email = fake.email()
    contact = Contact(name=name, email=email)
    contact.save()

    # Відправлення повідомлення з ObjectId контакту в чергу
    channel.basic_publish(exchange='', routing_key='contacts', body=str(contact.id))
    print(f" [x] Sent {contact.id}")

# Закриття з'єднання з RabbitMQ
connection.close()
