import pika
from mongoengine import connect
from models import Contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='contacts')

    connect(
        db="my-mongoDB",
        host="mongodb+srv://<user>:<password>@my-mongodb.qlte4g6.mongodb.net/?"
             "retryWrites=true&w=majority&appName=my-mongoDB"
    )

    def callback(ch, method, properties, body):
        contact_id = body.decode()
        contact = Contact.objects.get(id=contact_id)
        print(f" [x] Received message for contact: {contact_id}")
        contact.email_sent = True
        contact.save()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='contacts', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
