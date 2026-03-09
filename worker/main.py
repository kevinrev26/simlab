import os
import time
import pika
import json
from simlab_events.events import SimulationEvent


def main():
    print("### SIM EVENTS")
    print(SimulationEvent)
    credentials = pika.PlainCredentials(
        username=os.getenv("RABBITMQ_USER"),
        password=os.getenv("RABBITMQ_PASS")
    )
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    credentials=credentials
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue="simlab", durable=True)

            def callback(ch, method, properties, body):
                # handle your event here
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print(method)
                print(properties)
                event = json.loads(body)
                print(event)


            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue="simlab", on_message_callback=callback)
            print("Worker is listening...")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()