import json
import time

from pika import BlockingConnection, ConnectionParameters


BROKER_HOST = "localhost"
BROKER_POST = 5672


connection_params = ConnectionParameters(
    host=BROKER_HOST,
    port=BROKER_POST
)


def callback(channel, method, properties, body):
    # Processing a message
    print(f"Message: {json.loads(body.decode('utf-8'))}")
    time.sleep(1)
    
    channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    # Removing the message after processing
    # channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    with BlockingConnection(connection_params) as connection:
        with connection.channel() as channel:
            channel.basic_qos(prefetch_count=1)
            
            # channel.queue_declare(queue="messages", durable=True)
            
            channel.basic_consume(
                queue="messages",
                on_message_callback=callback,
                # auto_ack=True
            )
            
            channel.start_consuming()


if __name__ == '__main__':
    main()
