import asyncio
from aiokafka import AIOKafkaProducer
import aiosmtplib
from email.message import EmailMessage

SMTP_SERVER = 'smtp.google.com'
SMTP_PORT = 587
SMTP_USERNAME = 'leaguel255@gmail.com'
SMTP_PASSWORD = '91213399..'

async def send_email(to_email, subject, content):
    message = EmailMessage()
    message["From"] = SMTP_USERNAME
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    await aiosmtplib.send(message, hostname=SMTP_SERVER, port=SMTP_PORT, username=SMTP_USERNAME, password=SMTP_PASSWORD, use_tls=False)

async def send_product(product_data):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: v.encode('utf-8')
    )
    await producer.start()
    try:
        await producer.send_and_wait("productos", product_data.encode('utf-8'))
        await send_email(product_data.split(',')[3], "Producto Registrado", f"Su producto {product_data.split(',')[0]} ha sido registrado con éxito.")
    finally:
        await producer.stop()

async def main_loop():
    while True:
        try:
            product = input("Ingrese el nombre del producto: ")
            category = input("Ingrese la categoría del producto: ")
            price = input("Ingrese el precio del producto: ")
            correo = input("Ingrese el correo electrónico: ")
            product_data = f"{product},{category},{price},{correo}"
            await send_product(product_data)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_loop())
    loop.close()