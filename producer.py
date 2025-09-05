from pika import ConnectionParameters


BROKER_HOST = "localhost"
BROKER_POST = 5672


connection_params = ConnectionParameters(
    host=BROKER_HOST,
    port=BROKER_POST
)


def main():
    pass


if __name__ == '__main__':
    main()
