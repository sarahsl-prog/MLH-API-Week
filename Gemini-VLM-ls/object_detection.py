import os
from google import genai
from google.genai import types

# Step 1: Fetch our Gemini API key and init our client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Step 2: Loading our image to prompt
image_path = "image.jpeg"
my_image = client.files.upload(file=image_path)

# Step 3: Add a prompt
prompt = """
Locate the Lego from the image and give me the bounding box coordinates in JSON format labels should be
bounding_box: in the format [ymin, xmin, ymax, xmax] and label: with the object name
Do not use any markdown, just the raw JSON

"""

# Step 4: Call the gemini robotics model
image_response = client.models.generate_content(
    model="gemini-robotics-er-1.5-preview",
    contents=[
        my_image,
        prompt
    ],
    config = types.GenerateContentConfig(
        temperature=0.5,
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
)

print(image_response.text)
data_json = image_response.text

# Step 5: Parse the json response
import json
from PIL import Image, ImageDraw

data = json.loads(data_json)
box = data[0]['bounding_box']

print(box)

# Step 6: Draw our bounding box
img = Image.open(image_path)
w, h = img.size

draw = ImageDraw.Draw(img)
# [206, 588, 786, 960]
ymin, xmin, ymax, xmax = box
draw.rectangle(
    [xmin / 1000 * w, ymin / 1000 * h, xmax / 1000 * w, ymax / 1000 * h], 
    outline="red",
    width=3
)

# Step 7: Show the image with bounding box
img.save("output_image.jpeg")
img.show()




