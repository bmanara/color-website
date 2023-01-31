from flask import Flask, render_template, url_for, redirect, request, flash
import os
from werkzeug.utils import secure_filename
from PIL import Image
from photo_processor import ColorProcessor

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = ['png', 'jpg']

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4032 * 4032
app.config['UPLOAD_EXTENSIONS'] = ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', filename=False, colors=False)


@app.route('/', methods=['POST'])
def submit():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('home'))
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for upload')
        return redirect(url_for('home'))
    filename = secure_filename(file.filename)
    filename_arr = filename.split(".")
    filename_arr[0] = 'picture'
    filename = '.'.join(filename_arr)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('index.html', filename=filename, colors=False)


@app.route('/display/<filename>')
def display(filename):
    print(filename)
    return redirect(url_for('static', filename=f'uploads/{filename}', colors=False, code=301))


@app.route('/extract/<filename>', methods=['POST'])
def extract(filename):
    img = Image.open(f'static/uploads/{filename}')
    photo = ColorProcessor(img)
    colors, color_pct = photo.color_dist()
    hex_colors = photo.hex_colors()
    brightness = photo.color_brightness()
    print(colors, color_pct)
    print(type(colors), type(color_pct))
    return render_template('index.html', filename=filename, colors=colors, color_pct=color_pct,
                           hex_colors=hex_colors, brightness=brightness)


if __name__ == '__main__':
    app.run()
