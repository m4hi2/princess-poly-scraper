import os
import pickle
from typing import ByteString, Callable
import time

import pika
from dotenv import load_dotenv
from pika import channel

load_dotenv()


def declare(queues: list):
    """Declared queues in rabbitMQ

    Args:
        queues (list): List of queues to declare
    """
    for queue in queues:
        channel.queue_declare(queue=queue)


def publish(queue: str, body: dict, pickleit=True):
    """Publishes a message to the specified queue.

    Args:
        queue (str): Publish Queue
        body (dict): Message in python dictionary form
        pickeit (bool, optional): Whether to use python pickle binary in transport
        or send in plain JSON or other format. If set to false, the code has to 
        account for serialization. Defaults to True.
    """
    if pickleit:
        message = pickle.dumps(body)
    else:
        message = body
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2
                          ))


def consume(queue: str, callback: Callable[[str, str, str, ByteString], None], pickled=True):
    """Consumes messages from a queue and performs the action in the callback function

    Args:
        queue (str): Queue to consume
        callback (Callable[[str, str, str, ByteString], None]): Callback function  that performs
        the action/processing based on the consumed message from the queue.
        pickled (bool, optional): Describes whether the incoming message is serialized with
        python pickle or not. If set to false, the code has to handle serialization. Defaults to True.
    """
    def _consume(ch, method, properties, message):
        if pickled:
            body = pickle.loads(message)
        else:
            body = message
        callback(ch, method, properties, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue=queue, on_message_callback=_consume)


def loop():
    channel.start_consuming()

def connect(host):
    try:
        print("Waiting for rabbitmq")
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
    except:
        time.sleep(5)

if __name__ != "__main__":
    host = os.getenv("RABBITHOST", "localhost")
    connection = connect(host)
    while not connection:
        connection = connect(host)

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)