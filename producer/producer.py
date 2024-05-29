from flask import Flask, jsonify, request
from aiokafka import AIOKafkaProducer
import asyncio

import json
import asyncpg
import aiosmtplib 
from email.message import EmailMessage


app = Flask(__name__)


DATABASE_URL = "postgresql://user:password@postgres/ikea"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "leaguel255@gmail.com"
SMTP_PASSWORD = "91213399.."



async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)



async def send_one():
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    await producer.start()
    return producer
    """ try:
        await producer.send_and_wait("my_topic", b"Super message")
    finally:
        await producer.stop() """

asyncio.run(send_one())

async def send_email(to_email, subject, content):
    message = EmailMessage()
    message["From"] = SMTP_USERNAME
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)
    
    await aiosmtplib.send(message, hostname=SMTP_SERVER, port=SMTP_PORT, 
                          username=SMTP_USERNAME, 
                          password=SMTP_PASSWORD, use_tls=False)



@app.before_first_request
def startup_event():
    loop = asyncio.get_event_loop()
    app.config['db'] = loop.run_until_complete(get_db_connection())
    app.config['producer'] = loop.run_until_complete(send_one())

@app.route("/producto", methods=["POST"])
def create_producto():
    data = request.json
    product = data.get('product')
    category = data.get('category')
    price = data.get('price')
    correo = data.get('correo')

    if not all([product, category, price, correo]):
        return jsonify({"error": "Missing data"}), 400

    query = "INSERT INTO Product (product, category, price, correo) VALUES ($1, $2, $3, $4) RETURNING id"
    loop = asyncio.get_event_loop()
    product_id = loop.run_until_complete(app.config['db'].fetchval(query, product, category, price, correo))
    producto = {
        "id": product_id,
        "product": product,
        "category": category,
        "price": price,
        "correo": correo
    }
    loop.run_until_complete(app.config['producer'].send_and_wait("productos", producto))
    loop.run_until_complete(send_email(correo, "Producto Registrado", f"Su producto {product} ha sido registrado con éxito."))
    return jsonify(producto), 201

@app.teardown_appcontext
def shutdown_event(exception=None):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.config['db'].close())
    loop.run_until_complete(app.config['producer'].stop())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)