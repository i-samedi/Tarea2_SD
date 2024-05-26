from aiokafka import AIOKafkaConsumer
import asyncio
import json
from db import get_connection
import smtplib
from email.message import EmailMessage

# Configuración SMTP
email_sender = "leaguel255@gmail.com"
email_password = "91213399.."

# Configuración Kafka
bootstrap_servers = 'kafka:9092'
topic = 'pedidos'
group_id = "pedidos-group"

# Crear consumidor Kafka
consumer = AIOKafkaConsumer(
    topic,
    bootstrap_servers=[bootstrap_servers],
    group_id=group_id
)

# Enviar correo electrónico
def send_mail(email_receiver, subject, body):
    mail = EmailMessage()
    mail['From'] = email_sender
    mail['To'] = email_receiver
    mail['Subject'] = subject
    mail.set_content(body)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(email_sender, email_password)
        smtp.send_message(mail)
        print("Email enviado con éxito")

async def obtener_estado():
    id_pedido = input("Ingrese el ID del pedido: ")
    await consumer.start()
    try:
        async for msg in consumer:
            datos = json.loads(msg.value)
            if datos['id'] == id_pedido:
                estado = datos['estado']
                subject = f"Estado del pedido {id_pedido}"
                body = f"El estado del pedido {id_pedido} es: {estado}"
                correo = datos['correo']
                send_mail(correo, subject, body)
                print(f"Estado del pedido {id_pedido}: {estado}")
                return
    finally:
        await consumer.stop()

    print("Pedido no encontrado")

async def main():
    while True:
        opcion = input("Ingrese 1 para obtener el estado de un pedido: ")
        if opcion == '1':
            await obtener_estado()
        else:
            print("Opción inválida")

if __name__ == '__main__':
    asyncio.run(main())