import base64

# Function to encode the image
def encode_image(image_path):
    return base64.b64encode(image_path.read()).decode('utf-8')