from flask import Flask, jsonify, request
from aiokafka import AIOKafkaProducer
import asyncio
import requests
import json
import asyncpg


#app = Flask(__name__)

async def send_one():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("my_topic", b"Super message")
    finally:
        await producer.stop()

asyncio.run(send_one())

