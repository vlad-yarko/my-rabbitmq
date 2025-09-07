import json

from pika import BlockingConnection, ConnectionParameters, BasicProperties


BROKER_HOST = "localhost"
BROKER_POST = 5672


connection_params = ConnectionParameters(
    host=BROKER_HOST,
    port=BROKER_POST
)


def main():
    with BlockingConnection(connection_params) as connection:
        with connection.channel() as channel:
            channel.exchange_declare(exchange="dlx", exchange_type="fanout", durable=True)
            channel.queue_declare(queue="dlx", durable=True)
            channel.queue_bind(exchange="dlx", queue="dlx")
            
            args = {
                "x-dead-letter-exchange": "dlx"
            }
            
            channel.exchange_declare(exchange="messages", exchange_type="direct", durable=True)
            channel.queue_declare(queue="messages", durable=True, arguments=args)
            channel.queue_bind(
                exchange="messages",
                queue="messages",
                routing_key="messages"
            )

            
            channel.exchange_declare(exchange="logs", exchange_type="fanout", durable=False)
            channel.queue_declare(queue="logs")
            channel.queue_bind(exchange="logs", queue="logs")
            
            message_properties = BasicProperties(
                headers={
                    "my_header": "Hello"
                }
            )
            channel.basic_publish(
                exchange="messages",
                routing_key="messages",
                body=json.dumps({"message": "Hello world!"}),
                properties=message_properties
            )
            print("YEP")


if __name__ == '__main__':
    main()
