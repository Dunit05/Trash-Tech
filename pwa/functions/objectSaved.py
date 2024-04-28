# objectSaved.py

import json
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import base64
import os


def detectObject(image_data):
    # Get API_KEY and ENDPOINT from environment variables
    API_KEY = os.environ.get("API_KEY", "5e2987af82024d27be1139c7bb51d0ec")
    ENDPOINT = os.environ.get(
        "SECRET_KEY", "https://waste-it.cognitiveservices.azure.com/"
    )

    # Create a ComputerVisionClient
    cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

    # Decode base64-encoded image data
    image_data_decoded = base64.b64decode(image_data.split(",")[1])
    image_stream = BytesIO(image_data_decoded)

    # Perform object detection
    response_objects = cv_client.detect_objects_in_stream(image_stream)
    detected_objects = response_objects.objects

    # Perform image description
    image_stream.seek(0)  # Reset stream position
    response_description = cv_client.describe_image_in_stream(image_stream)
    image_description = response_description.captions[0].text

    # Perform TagImage operation
    image_stream.seek(0)  # Reset stream position
    tags_result = cv_client.tag_image_in_stream(image_stream)
    tags = [tag.name for tag in tags_result.tags]

    # Print image description and tags
    print("Image Description:", image_description)

    image_description_tags = image_description.split(" ")
    image_description_tags.extend(tags)

    print("Image Description Tags:", set(image_description_tags))
    return image_description_tags
