# from aiokafka import AIOKafkaConsumer
# import asyncio
# import json
# import requests
# import smtplib
# from email.message import EmailMessage

# # Configuración SMTP
# email_sender = "leaguel255@gmail.com"
# email_password = "91213399.."

# # Configuración Apache Kafka
# bootstrap_servers = 'kafka:9092'
# topic = 'pedidos'
# group_id = "pedidos-group"

# # Enviar correo electrónico
# def send_mail(email_receiver, subject, body):
#     mail = EmailMessage()
#     mail['From'] = email_sender
#     mail['To'] = email_receiver
#     mail['Subject'] = subject
#     mail.set_content(body)

#     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#         smtp.starttls()
#         smtp.login(email_sender, email_password)
#         smtp.send_message(mail)
#         print("Email enviado con éxito")

# async def enviar_pedido():
#     producto = input("Ingrese el producto: ")
#     categoria = input("Ingrese la categoría: ")
#     precio = float(input("Ingrese el precio: "))
#     correo = input("Ingrese el correo electrónico: ")

#     data = {
#         'producto': producto,
#         'categoria': categoria,
#         'precio': precio,
#         'correo': correo
#     }

#     # Enviar solicitud HTTP POST a Apache Kafka (simular productor)
#     response = requests.post('http://kafka:9092/enviar_pedido', json=data)
#     print(response.text)

# async def obtener_estado():
#     id_pedido = input("Ingrese el ID del pedido: ")

#     # Enviar solicitud HTTP GET a Apache Kafka
#     response = requests.get(f'http://kafka:9092/estado/{id_pedido}')
#     datos = response.json()

#     if 'estado' in datos:
#         estado = datos['estado']
#         subject = f"Estado del pedido {id_pedido}"
#         body = f"El estado del pedido {id_pedido} es: {estado}"
#         correo = datos['correo']
#         send_mail(correo, subject, body)
#         print(f"Estado del pedido {id_pedido}: {estado}")
#     else:
#         print("Pedido no encontrado")

# async def main():
#     while True:
#         opcion = input("Ingrese 1 para enviar un pedido o 2 para obtener el estado de un pedido: ")
#         if opcion == '1':
#             await enviar_pedido()
#         elif opcion == '2':
#             await obtener_estado()
#         else:
#             print("Opción inválida")

# if __name__ == '__main__':
#     asyncio.run(main())

from aiokafka import KafkaConsumer
import json
from db import get_db_connection

# Configuración del Kafka Consumer
consumer = KafkaConsumer(
    'pedidos',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='procesamiento_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Conexión a la base de datos PostgreSQL
conn = get_db_connection()
cursor = conn.cursor()

# Función para procesar pedido
def process_order(order):
    cursor.execute(
        """
        INSERT INTO PEDIDOS (CLIENTEID, PRODUCTO, CATEGORIA, PRECIO, ESTADO)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (order['clienteid'], order['producto'], order['categoria'], order['precio'], 'recibido')
    )
    conn.commit()
    print(f"Pedido procesado y almacenado: {order}")

# Consumiendo mensajes de Kafka y procesándolos
for message in consumer:
    order = message.value
    process_order(order)

# Cerrar conexión
cursor.close()
conn.close()
