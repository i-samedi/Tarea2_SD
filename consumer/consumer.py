from aiokafka import AIOKafkaConsumer
import asyncio
import json
from db import insert_data  # Importar la función insert_data desde db.py

async def consume():
    consumer = AIOKafkaConsumer(
        'my_topic', 'my_other_topic',
        bootstrap_servers='kafka:9092',
        group_id="my-group")
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            print("Datos recibidos:", data)
            insert_data(data)  # Llamar a la función insert_data desde db.py
    finally:
        await consumer.stop()

asyncio.run(consume())