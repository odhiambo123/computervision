# computervision
detects handwritten images from a file and translates then outputs the results

Install the python decouple package to help with the .env files

`$ pip install python-decouple`

Create a .env file

on linux use:
`touch .env`

 on windows use:
`New-Item .env -type file`

[create a computer vision resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision)

after you create your resource, copy the endpoint and the subsription keys and add them to the .env file as below

COMPUTER_VISION_SUBSCRIPTION_KEY=''
COMPUTER_VISION_ENDPOINT=''

you can add a different file path to read from by replacing the url on main.py
run your code.

References:

[Azure samples](https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/REST/python-hand-text.md)

[how to set environment variables](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5)