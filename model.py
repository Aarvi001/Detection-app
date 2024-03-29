from flask import Flask, render_template, request, session
import os
from werkzeug.utils import secure_filename
from ultralytics import yolo
#*** Backend operation
 
# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'
 
 
@app.route('/')
def index():
    return render_template('test.html')
 
@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = "input.jpg"
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        return render_template('page2.html')
 
@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)    
    os.system('cmd /c "yolo task=detect mode=predict model=best.pt source=staticFiles/uploads/input.jpg imgsz=640 name=yolov8_infer hide_labels=True save=True"')
    # Display image in Flask application web page
    os.system('cmd /c "copy runs\\detect\\yolov8_infer\\input.jpg staticFiles\\uploads\\"')
    os.system('cmd /c "rmdir /s /q runs"')
    return render_template('show_image.html', user_image=img_file_path)
 
if __name__=='__main__':
    app.run(debug = True)