import asyncio
import json

from aio_pika import connect_robust, ExchangeType, Message


BROKER_URL = "amqp://guest:guest@localhost:5672/"


async def main():
    connection = await connect_robust(BROKER_URL)
    async with connection:
        async with connection.channel() as channel:
            
            # DLX
            dlx_exchange = await channel.declare_exchange(name="dlx", type=ExchangeType.FANOUT, durable=True)
            dlx_queue = await channel.declare_queue(name="dlx", durable=True, exclusive=False)
            await dlx_queue.bind(dlx_exchange)
            args = {
                "x-dead-letter-exchange": "dlx"
            }
            
            # Messages
            messages_exchange = await channel.declare_exchange(name="messages", type=ExchangeType.DIRECT, durable=True)
            messages_queue = await channel.declare_queue(name="messages", durable=True, exclusive=False, arguments=args)
            await messages_queue.bind(messages_exchange, routing_key="messages")
            
            # Messages publishing
            message = Message(
                body=json.dumps({"messages": "messages"}).encode(),
                headers={
                    "my_header": "my_header"
                }
            )
            await messages_exchange.publish(
                message,
                routing_key="messages"
            )
            
            
asyncio.run(main())
