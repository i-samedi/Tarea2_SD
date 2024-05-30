import json
import asyncio
from aiokafka import AIOKafkaConsumer
import aiosmtplib
from email.message import EmailMessage

SMTP_SERVER = 'smtp.google.com'
SMTP_PORT = 587
SMTP_USERNAME = 'leaguel255@gmail.com'
SMTP_PASSWORD = '91213399..'

ESTADOS = ["recibido", "preparando", "entregando", "finalizado"]
TIEMPO_DE_ESPERA = 5

async def send_email(to_email, subject, content):
    message = EmailMessage()
    message["From"] = SMTP_USERNAME
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    await aiosmtplib.send(message, hostname=SMTP_SERVER, port=SMTP_PORT, username=SMTP_USERNAME, password=SMTP_PASSWORD, use_tls=False)

async def main():
    while True:
        try:
            consumer = AIOKafkaConsumer(
                'productos',
                bootstrap_servers='kafka:9092',
                group_id="procesamiento-group",
                value_deserializer=lambda v: json.loads(v.decode('utf-8'))
            )
            await consumer.start()
            break
        except Exception as e:
            print(f"Error al conectar con Kafka: {e}. Reintentando en 5 segundos...")
            await asyncio.sleep(5)

    try:
        async for msg in consumer:
            producto = msg.value
            for estado in ESTADOS:
                producto['estado'] = estado
                await send_email(producto['correo'], f"Actualización de Producto (ID: {producto['id']})", f"Su producto ahora está en estado: {estado}")
                await asyncio.sleep(TIEMPO_DE_ESPERA)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())