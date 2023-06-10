from flask import Flask, request, send_file, render_template
from flask_start import flask_start
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('mainPage.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    # 동영상 파일을 메모리에 저장

    file.save("./VideoFile/video.mp4")
    flask_start("./VideoFile/video.mp4")
    zip_path = './outputVideo/HighlightVideo.zip'
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write('./outputVideo/highlight_time.txt')
        zip_file.write('./outputVideo/output.mp4')

    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

