import pika
import json
from models import Contact
from faker import Faker

fake = Faker()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')


def create_fake_contact():
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        preferred_contact_method='email' if fake.boolean() else 'sms'
    )
    contact.save()
    return contact

for _ in range(10):
    contact = create_fake_contact()
    queue_name = 'email_queue' if contact.preferred_contact_method == 'email' else 'sms_queue'
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(str(contact.id))
    )

connection.close()
