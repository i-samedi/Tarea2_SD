import json
import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncpg
import aiosmtplib
from email.message import EmailMessage

DATABASE_URL = "postgresql://user:password@postgres/ikea"
SMTP_SERVER = 'smtp.example.com'  # Reemplaza con tu servidor SMTP
SMTP_PORT = 587
SMTP_USERNAME = 'tu_usuario@example.com'  # Reemplaza con tu nombre de usuario SMTP
SMTP_PASSWORD = 'tu_contraseña'  # Reemplaza con tu contraseña SMTP

ESTADOS = ["registrado", "procesando", "finalizado"]
TIEMPO_DE_ESPERA = 5  # Tiempo en segundos

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

async def send_email(to_email, subject, content):
    message = EmailMessage()
    message["From"] = SMTP_USERNAME
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)
    
    await aiosmtplib.send(message, hostname=SMTP_SERVER, port=SMTP_PORT, username=SMTP_USERNAME, password=SMTP_PASSWORD, use_tls=False)

async def main():
    consumer = AIOKafkaConsumer(
        'productos',
        bootstrap_servers='kafka:9092',
        group_id="procesamiento-group",
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    await consumer.start()
    await producer.start()
    db = await get_db_connection()

    try:
        async for msg in consumer:
            producto = msg.value
            for estado in ESTADOS:
                producto['estado'] = estado
                query = "UPDATE Product SET estado = $1 WHERE id = $2"
                await db.execute(query, estado, producto['id'])
                await producer.send_and_wait("productos_procesados", producto)
                await send_email(producto['correo'], f"Actualización de Producto (ID: {producto['id']})", f"Su producto ahora está en estado: {estado}")
                await asyncio.sleep(TIEMPO_DE_ESPERA)
    finally:
        await consumer.stop()
        await producer.stop()
        await db.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
