ffmpeg_command = "C:/" #Odwłoanie do programu ffmpeg, może być inna nazwa w zależności od systemu operacyjnego
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import send_from_directory
import os
import subprocess

app = Flask(__name__)

cors = CORS()
cors.init_app(app, resources={r"/*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        
        filename = secure_filename(fname)
        counter = 1
        while os.path.exists('./uploads/' + filename):
            name, ext = os.path.splitext(filename)
            filename = f"{name}x{counter}{ext}"
            counter += 1

        f.save('./uploads/%s' % filename)

    return 'Okay!'

@app.route('/files', methods=['GET'])
def files():
    files = [f for f in os.listdir('./uploads') if f.endswith('.mp4')]
    return jsonify(files)

@app.route('/photosfiles', methods=['GET'])
def photosfiles():
    files = [f for f in os.listdir('./uploads') if f.endswith('.png')]
    return jsonify(files)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='./uploads', path=filename)

@app.route('/delete/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    os.remove('./uploads/' + filename)
    return 'File deleted'

@app.route('/watermark/<path:filename>/', methods=['GET'])
def watermark(filename):
    #opacity = request.args.get('opacity', 0.5) # Domyślna wartość przezroczystości
    
    output_filename = './uploads/watermarked_' + filename
    counter = 1

    # Sprawdzanie, czy plik już istnieje i zmiana nazwy, jeśli tak
    while os.path.exists(output_filename):
        name, ext = os.path.splitext(output_filename)
        output_filename = f"{name}x{counter}{ext}"
        counter += 1
    subprocess.call([ffmpeg_command, '-y', '-i', f'./uploads/{filename}', '-i', 'watermark.png', '-filter_complex', '[1:v]format=rgba,colorchannelmixer=aa=0.5[wm];[0:v][wm]overlay=W-w-10:H-h-10', '-c:a', 'copy', f'{output_filename}'])
    return 'Watermarked video created'
    
@app.route('/sepia/<path:filename>/', methods=['GET'])
def sepia(filename):
    print(filename)
    output_filename = './uploads/sepia_' + filename
    counter = 1

    while os.path.exists(output_filename):
        name, ext = os.path.splitext(output_filename)
        output_filename = f"{name}x{counter}{ext}"
        counter += 1

    subprocess.call([ffmpeg_command, '-y', '-i', f'./uploads/{filename}', '-vf', 'format=gray,geq=lum_expr=(128+(lum-128)*0.68)', f'{output_filename}'])
    return 'Sepia video created'

@app.route('/blackwhite/<path:filename>/', methods=['GET'])
def blackwhite(filename):
    print(filename)
    output_filename = './uploads/blackwhite_' + filename
    counter = 1

    while os.path.exists(output_filename):
        name, ext = os.path.splitext(output_filename)
        output_filename = f"{name}x{counter}{ext}"
        counter += 1

    subprocess.call([ffmpeg_command, '-y', '-i', f'./uploads/{filename}', '-vf', 'format=gray', f'{output_filename}'])
    return 'Black and white video created'


if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./uploads')
    app.run(host='0.0.0.0')
