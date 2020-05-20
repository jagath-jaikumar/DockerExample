import requests
from image_encoder.image_encoder import *
import argparse
parser = argparse.ArgumentParser(description='Test Docker Example')

type = "MLSample"


endpoint = "http://localhost:5000/"

r = requests.post(endpoint,json={"image":encode("dog.jpg")})
print(r.text)
