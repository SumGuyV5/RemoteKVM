import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

from Modules.USBInput import USBInput

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

UPLOAD_FOLDER = r'C:\Users\Richard\PycharmProjects\keyboard_input/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'iso', 'img'}

usb = USBInput()


@socketio.on('my event', namespace='/')
def handle_my_custom_namespace_event(json):
    # print('received json: ' + str(json))
    if json['type'] == 'keyboard_down':
        usb.keyboard_down(json['key'])
    elif json['type'] == 'keyboard_up':
        usb.keyboard_up(json['key'])
    elif json['type'] == 'mouse':
        usb.mouse_move(int(json['posX']), int(json['posY']))
    elif json['type'] == 'mouse_button_down':
        usb.mouse_button_down(json['data'])
    elif json['type'] == 'mouse_button_up':
        usb.mouse_button_up(json['data'])
    elif json['type'] == 'mouse_enter':
        pass


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
