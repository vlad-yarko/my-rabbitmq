import json

from pika import BlockingConnection, ConnectionParameters


BROKER_HOST = "localhost"
BROKER_POST = 5672


connection_params = ConnectionParameters(
    host=BROKER_HOST,
    port=BROKER_POST
)


def main():
    with BlockingConnection(connection_params) as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue="messages", durable=False)
            
            channel.basic_publish(
                exchange="",
                routing_key="messages",
                body=json.dumps({"message": "Hello world!"})
            )


if __name__ == '__main__':
    main()
