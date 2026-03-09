import os
import json
from dataclasses import asdict
from simlab_events.events import SimulationEvent
import pika

class Dispatch():
    
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="rabbitmq",
                credentials=pika.PlainCredentials(
                    username=os.getenv("RABBITMQ_USER"),
                    password=os.getenv("RABBITMQ_PASS")
                )
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='simlab', durable=True)
        
    
    def dispatch_event(self, params):
        event = SimulationEvent(**params)
        self.channel.basic_publish(
            exchange='',
            routing_key='simlab',
            body=json.dumps(asdict(event)),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )

    def close(self):
        self.connection.close()
