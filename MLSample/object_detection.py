from flask import Flask, request, jsonify
from torchvision import models, transforms
import torch
from image_encoder.image_encoder import decode
import pika
import mysql.connector


def get_image(uuid):
    config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'content'
        }
    connection_images = mysql.connector.connect(**config)
    cursor = connection_images.cursor()

    query = ("SELECT TRIM(image) FROM images WHERE uuid = '{}'").format(uuid)


    print(uuid)
    cursor.execute(query)
    print(cursor)
    for image in cursor:
        print(image[0])
        return decode(image[0])


# app = Flask(__name__)

alexnet = models.alexnet(pretrained=True)
alexnet.eval()

classes = []
with open('imagenet_classes.txt') as f:
    classes = [line.strip() for line in f.readlines()]


transform = transforms.Compose([
 transforms.Resize(256),
 transforms.CenterCrop(224),
 transforms.ToTensor(),
 transforms.Normalize(
 mean=[0.485, 0.456, 0.406],
 std=[0.229, 0.224, 0.225]
 )])


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='imageq')

def callback(ch, method, properties, body):
    img_id = str(body)[2:-1]
    image = get_image(img_id)
    print(image.size)


channel.basic_consume(queue='imageq',
                      auto_ack=True,
                      on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# @app.route("/predict", methods = ["POST"])
# def predict():
#     data = request.get_json()
#     img = decode(data["image"])
#     img_t = transform(img)
#     batch_t = torch.unsqueeze(img_t, 0)
#     out = alexnet(batch_t)
#     _, indices = torch.sort(out, descending=True)
#     percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
#
#     output = {}
#     for idx in indices[0][:5]:
#         output[classes[idx]] = percentage[idx].item()
#
#     return jsonify({"result":output})


#if __name__=="__main__":
    # app.run(host='0.0.0.0')
