
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, send_file, request
from flask_cors import CORS
import base64
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Extract base64 encoded string from the request
    data = request.json.get('image_base64')
    if not data:
        return "No image data provided", 400    
    try:
        # Decode the base64 string
        image_data = base64.b64decode(data) 
        # Convert binary data to image
        image = Image.open(BytesIO(image_data)) 
        # Save the image to a temporary file
        temp_file = "temp_image.png"
        image.save(temp_file)   
        # Send the file as response
        return send_file(temp_file, mimetype='image/png', as_attachment=True)
    except Exception as e:
        return str(e), 500
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)