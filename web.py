from flask import Flask, render_template, request, jsonify, send_from_directory,send_file
from werkzeug.utils import secure_filename
import os
import uuid
import threading
import time
import requests
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('MyFlaskService')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler('webservice.log', maxBytes=100000, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# 文件上传状态字典
upload_statuses = {}

# 锁定对象，用于同步上传状态
upload_lock = threading.Lock()
# 获取文件名的后缀
def get_file_extension(filename):
    return os.path.splitext(filename)[1]

@app.route('/')
def index():
    logger.info("get index")
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    files = request.files.getlist('file')
    logger.info(files)
    response_data = []
    for file in files:
        if file.filename == '':
            continue
        uuid_filename = f"{uuid.uuid4().hex}{get_file_extension(file.filename)}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid_filename)
        print(file.filename,file_path)
        try:
            file.save(file_path)
        except Exception as e:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(file_path)
        
        # 使用线程来处理文件上传，以避免阻塞主线程
        # threading.Thread(target=upload_file, args=(file_path, target_path)).start()
        
        # 将文件路径添加到上传状态字典
        with upload_lock:
            upload_statuses[file_path] = (0, os.path.getsize(file_path))
        
        # 添加到响应数据中
        response_data.append({
            'filename': file.filename,
            'uuid_filename': uuid_filename # 只保留 UUID 部分
        })

    return jsonify({'status': 'started', 'files': response_data})


@app.route('/status/<filename>')
def get_status(filename):
    with upload_lock:
        status = upload_statuses.get(filename)
    return jsonify(status)

@app.route('/download/<uuid>/<filename>')
def download(uuid, filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid)
    if not os.path.exists(file_path):
        return 'File not found', 404
    
    # 重命名文件为指定的文件名
    try:
        os.rename(file_path, os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except FileExistsError as e:
        os.replace(file_path, os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except Exception as e:
        logger.error(e)
        return 'Error occurred while renaming file', 500
    
    
    # 构造新的文件路径
    new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # 返回文件作为附件下载
    try:
        response = send_file(new_file_path, as_attachment=True)
        return response
    except Exception as e:
        logger.error(e)
        return 'Error occurred while downloading file', 500

if __name__ == '__main__':
    logger.info("start")
    app.run(debug=True, port=5984)
    logger.info("end")