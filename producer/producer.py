import json
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

async def send_product(product):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        await producer.send_and_wait("productos", product)
        await send_email(product['correo'], "Producto Registrado", f"Su producto {product['product']} ha sido registrado con éxito.")
    finally:
        await producer.stop()

async def main():
    while True:
        try:
            product = input("Ingrese los detalles del producto (product, category, price, correo): ")
            product_data = json.loads("{" + product + "}")
            await send_product(product_data)
        except Exception as e:
            if str(e) == "EOF when reading a line":
                continue
            else:
                print(f"Error: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())