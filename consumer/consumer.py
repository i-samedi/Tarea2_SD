from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json
from db import insert_data
from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Configuración SMTP
email_sender = "tu_correo@example.com"
email_password = "tu_contraseña"

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

# Crear productor Kafka
producer = AIOKafkaProducer(bootstrap_servers=[bootstrap_servers])

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

# Endpoint para recibir pedido (HTTP POST)
@app.route('/solicitud', methods=['POST'])
async def solicitar_pedido():
    data = await request.get_json()
    await producer.start()
    try:
        await producer.send_and_wait(topic, json.dumps(data).encode('utf-8'))
    finally:
        await producer.stop()
    return jsonify({'mensaje': 'Pedido enviado correctamente'}), 200

# Endpoint para obtener estado del pedido (HTTP GET)
@app.route('/estado/<id_pedido>', methods=['GET'])
async def obtener_estado(id_pedido):
    await consumer.start()
    try:
        async for msg in consumer:
            datos = json.loads(msg.value)
            if datos['id'] == id_pedido:
                subject = f"Estado del pedido {id_pedido}"
                body = f"El estado del pedido {id_pedido} es: {datos['estado']}"
                correo = datos['correo']
                send_mail(correo, subject, body)
                return jsonify(datos), 200
    finally:
        await consumer.stop()

    return jsonify({'mensaje': 'Pedido no encontrado'}), 404

if __name__ == '__main__':
    asyncio.run(consumer.start())
    app.run(host='0.0.0.0', port=5000)