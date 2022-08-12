import json
import os
import sys
import requests
import time
# If you are using a Jupyter Notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO
from decouple import config


if __name__ == '__main__':

    endpoint = config('COMPUTER_VISION_ENDPOINT')
    subscription_key = config('COMPUTER_VISION_SUBSCRIPTION_KEY')

    text_recognition_url = endpoint + "/vision/v3.1/read/analyze"

    # Set image_url to the URL of an image that you want to recognize.
    image_url ="https://scontent-lax3-2.xx.fbcdn.net/v/t39.30808-6/298376906_170810028778744_8361858824450820915_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=730e14&_nc_ohc=_PWSf8_66VcAX-JK2-7&tn=f2alIv-9aEpcUhCO&_nc_ht=scontent-lax3-2.xx&oh=00_AT8hstAPQB3bLX76Gc-ibA-iHxOpZoskOz4EbW2eObl3qA&oe=62FAF139"
    #image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    data = {'url': image_url}
    response = requests.post(
        text_recognition_url, headers=headers, json=data)
    response.raise_for_status()

    # Extracting text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.

    # Holds the URI used to retrieve the recognized text.
    operation_url = response.headers["Operation-Location"]

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()

        print(json.dumps(analysis, indent=4))

        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False

    polygons = []
    if ("analyzeResult" in analysis):
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"])
                    for line in analysis["analyzeResult"]["readResults"][0]["lines"]]

    # Display the image and overlay it with the extracted text.
    image = Image.open(BytesIO(requests.get(image_url).content))
    ax = plt.imshow(image)
    for polygon in polygons:
        vertices = [(polygon[0][i], polygon[0][i + 1])
                    for i in range(0, len(polygon[0]), 2)]
        text = polygon[1]
        patch = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
        ax.axes.add_patch(patch)
        plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")
    plt.show()
