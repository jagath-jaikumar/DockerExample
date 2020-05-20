from flask import Flask, request
import mysql.connector
import uuid
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='imageq')

app = Flask(__name__)

@app.route("/", methods = ["POST"])
def save_dispatch():
    packet = request.get_json()
    for k,v in packet.items():
        if k == "image":
            save_post_image(packet)

    return ""

def save_post_image(packet):
    img_id = save_image(packet)
    channel.basic_publish(exchange='', routing_key='imageq', body=img_id)
    print(img_id)
    print("sent img_id")


def save_image(packet):
    config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'content'
        }
    connection_images = mysql.connector.connect(**config)
    cursor = connection_images.cursor()

    img_id = uuid.uuid4().urn[9:]

    img_data = (img_id,packet["image"])
    add_image = ("INSERT IGNORE INTO images "
               "(uuid, image) "
               "VALUES (%s, %s)")

    cursor.execute(add_image, img_data)

    connection_images.commit()
    cursor.close()
    connection_images.close()

    return img_id





if __name__=="__main__":
    app.run(host='0.0.0.0')
