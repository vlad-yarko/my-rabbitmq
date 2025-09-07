import asyncio
import json

from aio_pika import connect_robust, IncomingMessage


BROKER_URL = "amqp://guest:guest@localhost:5672/"


async def callback(message: IncomingMessage):
    try:
        print("Received:", message.body.decode())
        print("Headers:", message.headers)
        print("Routing key:", message.routing_key)
        await asyncio.sleep(2)
        await message.ack()
    except Exception as e:
        print(str(e))
        await message.nack(requeue=False)


async def main():
    connection = await connect_robust(BROKER_URL)
    async with connection:
        async with connection.channel() as channel:
            
            await channel.set_qos(prefetch_count=True)
            
            # Consuming
            args = {
                "x-dead-letter-exchange": "dlx"
            }
            
            # Messages
            messages_queue = await channel.declare_queue(name="messages", durable=True, exclusive=False, arguments=args)
            await messages_queue.consume(callback)
            await asyncio.Future()
            
            
asyncio.run(main())
