import pika
import json
from models import Contact


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='sms_queue')


def send_sms(contact):
    print(f"Sending SMS to {contact.phone_number}: 'Your message content here'")


def on_message(ch, method, properties, body):
    contact_id = json.loads(body)
    contact = Contact.objects(id=contact_id).first()
    if contact:
        send_sms(contact)
        contact.message_sent = True
        contact.save()
        print(f"Message sent to {contact.fullname}")
    else:
        print(f"Contact with id {contact_id} not found.")


channel.basic_consume(queue='sms_queue', on_message_callback=on_message, auto_ack=True)

print(' [*] Waiting for SMS messages. To exit press CTRL+C')
channel.start_consuming()
