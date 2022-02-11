import os
from datetime import datetime
from urllib import request

from flask import Flask, request
import json
from flask_mysqldb import MySQL

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'naveen/images' # 'media/images'
ALLOWED_EXTENSIONS = (['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'raghu'
app.config['MYSQL_DB'] = 'clinicalfirst_services'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mysql = MySQL(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/image', methods=['POST'])
def index():
    now = datetime.now()
    if request.method == 'POST':
        userDetails = None
        path = request.form['user_folder_path + filename']
        mail_id = request.form['mail_id']
        if request.files['image']:
            userDetails = request.files['image']
        # else:
        #     userDetails = users(request.form)
        if userDetails and allowed_file(userDetails.filename):
            filename = secure_filename(userDetails.filename)
            user_folder_path = app.config['UPLOAD_FOLDER'] + '/pics/'
            if not os.path.exists(user_folder_path):
                os.makedirs(user_folder_path)
            userDetails.save(os.path.join(user_folder_path, filename))
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO Images(file_name,mail_id,uploaded_on) VALUES(%s,%s,%s)',
                               (user_folder_path + filename, mail_id, now))
                mysql.connection.commit()
                cursor.close()
            except Exception as e:
                print(e)
                return "Unable to insert image metadata to db"
            return "Image uploaded successfully."

if __name__ == "__main__":
    app.run(debug=True)
