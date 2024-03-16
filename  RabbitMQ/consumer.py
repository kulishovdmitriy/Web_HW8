import pika
from time import sleep
from mongoengine import connect
from models import Contact

# Функція для імітації відправлення email
def send_email(contact_id):
    # Зчитуємо контакт з MongoDB за його ObjectId
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending email to {contact.email}...")

    # Імітація надсилання email

    # Позначаємо контакт як відправлений
    contact.email_sent = True
    contact.save()
    print("Email sent successfully!")

# З'єднання з RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='contacts')

# Підключення до MongoDB
connect('contacts_database')

# Функція обробки повідомлення з черги
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    send_email(body.decode())

# Встановлюємо callback-функцію для обробки повідомлень
channel.basic_consume(queue='contacts', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
