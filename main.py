from datetime import datetime, timedelta
import re
from marshmallow import ValidationError

import MySQLdb
from flask import Flask, request, jsonify, json, session
import logging
import socket
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from faker import Faker

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'raghu'
app.config['MYSQL_DB'] = 'clinicalfirst_services'
app.config['SECRET_KEY'] = 'secret_key'

mysql = MySQL(app)


#
#
@app.route('/patient_signup', methods=['POST'])
def register():
    if 'patient_name' in request.json and 'password' in request.json \
            and 'email' in request.json and 'phone' in request.json:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        PATIENT_ID = max_id_value(cursor)
        patient_name = request.json['patient_name']
        email = request.json['email']
        phone = request.json['phone']
        password = request.json['password']
        hashed_password = generate_password_hash(password)
        ex = Faker()
        ip = ex.ipv4()
        print(ip)

        date = datetime.today()
        device = socket.gethostname()
        print(device)

        # Cursor:-

        cursor.execute('SELECT * FROM PATIENT_SIGNUP WHERE PATIENT_MAIL_ID = %s OR PATIENT_PHONE_NUMBER = %s',
                       (email, phone))
        account = cursor.fetchone()

        if account and account['PATIENT_MAIL_ID'] == email:
            msg = 'Your mail_id already exist please enter new mail_id  !!!!'

        elif account and account["PATIENT_PHONE_NUMBER"] == phone:
            msg = "Your phone number is duplicate please enter new number!!!"

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = ' mail id must contain @ domain name !'

        elif not re.match(r'[A-Za-z]+', patient_name):
            msg = 'Username must contain only characters !'

        elif not re.match(r'^[A-Za-z0-9@#$%^&+=]{8,32}', password):
            msg = 'Password must contain alpha_number with special_characters !'

        elif not re.match(r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$', phone):
            msg = ' phone number must contain ten digits, must starts with 9 or 8 or 7 and starts with +91 !'

        elif not re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                          ip):
            msg = 'Invalid ip address format !'

        # elif not re.match(r'^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$', date):
        #     msg = ' date format start with year, month and date !'

        elif not patient_name or not password or not email or not phone or not ip or not date:
            msg = 'Please fill out the form !'

        else:
            cur = mysql.connection.cursor()
            cur.execute(
                "insert into PATIENT_SIGNUP (PATIENT_ID, PATIENT_NAME, PATIENT_MAIL_ID, PATIENT_PHONE_NUMBER, PATIENT_PASSWORD, PATIENT_IP,"
                "PATIENT_DATE_CREATED, PATIENT_DEVICE) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                (PATIENT_ID, patient_name, email, phone, hashed_password, ip, date, device))
            mysql.connection.commit()
            # details = cur.fetchall()
            logging.info("successfully registered")
            return "successfully inserted", 200
        return msg
    return "invalid parameters"


@app.route('/patient_login', methods=["POST"])
def login():
    if 'email' in request.json and 'password' in request.json:
        email = request.json["email"]
        logging.info('Admin logged in')
        pw = request.json["password"]
        logging.warning('Watch out!')
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select * from patient_signup WHERE (PATIENT_MAIL_ID = %s )", (email,))
        details = cur.fetchone()
        if details is None:
            return ({"message": "No details"}), 401
        hashed_password = details["patient_password"]
        password_match = check_password_hash(hashed_password, pw)
        if password_match:
            session['PATIENT_ID'] = details['PATIENT_ID']
            return "successfully login"
        else:
            logging.error("Invalid credentials")

        return ({"Error": "invalid credentials"}), 401

    return "Insufficient parameters", 400


def max_id_value(c):
    max_value_query = "SELECT substring(patient_id,6) as id FROM PATIENT_SIGNUP WHERE substring(patient_id," \
                      "6)=(SELECT MAX(CAST(SUBSTRING(patient_id,6) AS SIGNED)) FROM PATIENT_SIGNUP) "
    c.execute(max_value_query)
    result_value = c.fetchone()
    if result_value == 0 or result_value == 'None' or result_value == '' or result_value is None:
        result_value = 1;
        patient_id = 'PA000' + str(result_value)
        return patient_id
    else:
        result_value = int(result_value[0]) + 1
        patient_id = 'PA000' + str(result_value)
        return patient_id
    #
    # 'patient_id' in request.json and
    # and 'patient_approved' in request.json


@app.route('/patient_registration', methods=['POST'])
def patient_registration():
    if 'patient_age' in request.json and 'patient_exp' in request.json \
            and 'patient_gender' in request.json and 'patient_licnce_num' in request.json and 'patient_flat_num' in request.json \
            and 'patient_street_name' in request.json and 'patient_city_name' in request.json and 'patient_state_name' in request.json \
            and 'patient_country_name' in request.json and 'zipcode' in request.json:
        request_data = request.json

        cursor = mysql.connection.cursor()
        patient_Id = max_id_value(cursor)
        age = request_data['patient_age']
        patient_experience = request_data['patient_exp']
        gender = request_data['patient_gender']
        liciencenum = request_data['patient_licnce_num']
        flatnum = request_data['patient_flat_num']
        street = request_data['patient_street_name']
        city = request_data['patient_city_name']
        state = request_data['patient_state_name']
        country = request_data['patient_country_name']
        zipcode = request_data['zipcode']
        approved = datetime.today()
        ex = Faker()
        ip = ex.ipv4()
        print(ip)

        date = datetime.today()
        device = socket.gethostname()
        print(device)

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM patient_registration WHERE PATIENT_ID = %s', (patient_Id,))
        account = cur.fetchone()
        if account and account["PATIENT_ID"] == patient_Id:
            return 'Your user id duplicate please enter new value!', 400
        patient_data = patient_sub_registration(MySQLdb.cursors.DictCursor)
        try:
            patient_data.load(request_data)
            cur = mysql.connection.cursor()
            cur.execute(
                "insert into patient_registration(PATIENT_ID, PATIENT_AGE,PATIENT_EXPERIANCE, PATIENT_GENDER,"
                "PATIENT_LICENSE_NUMBER,FLAT_NO,STREET_NAME,CITY_NAME,STATE_NAME,COUNTRY_NAME,ZIP_CODE,"
                "PATIENT_APPROVED,PATIENT_IP,PATIENT_DATE_REGISTERED,PATIENT_DEVICE) values(%s,%s,%s,%s,%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,%s,%s)",
                (patient_Id, age, patient_experience, gender, liciencenum, flatnum, street,
                 city, state, country, zipcode, approved, ip, date, device))
            mysql.connection.commit()
            return "successfully inserted", 200
        except ValidationError as e:
            print(e)
        return jsonify(e.messages)

    return "invalid parameters"


def max_id_value(c):
    max_value_query = "SELECT substring(patient_id,6) as id FROM PATIENT_REGISTRATION WHERE substring(patient_id," \
                      "6)=(SELECT MAX(CAST(SUBSTRING(patient_id,6) AS SIGNED)) FROM PATIENT_REGISTRATION) "
    c.execute(max_value_query)
    result_value = c.fetchone()
    if result_value == 0 or result_value == 'None' or result_value == '' or result_value is None:
        result_value = 1;
        patient_id = 'PA000' + str(result_value)
        return patient_id
    else:
        result_value = int(result_value[0]) + 1
        patient_id = 'PA000' + str(result_value)
        return patient_id


@app.route('/patient_sub_registration', methods=['POST'])
def patient_sub_registration():
    if 'patient_age' in request.json and 'patient_exp' in request.json \
            and 'patient_gender' in request.json and 'patient_licnce_num' in request.json and 'patient_flat_num' in request.json \
            and 'patient_street_name' in request.json and 'patient_city_name' in request.json and 'patient_state_name' in request.json \
            and 'patient_country_name' in request.json and 'zipcode' in request.json:
        request_data = request.json

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        patient_id = session['PATIENT_ID']
        patient_sub_Id = max_id_value(cursor)
        age = request_data['patient_age']
        patient_experience = request_data['patient_exp']
        gender = request_data['patient_gender']
        liciencenum = request_data['patient_licnce_num']
        flatnum = request_data['patient_flat_num']
        street = request_data['patient_street_name']
        city = request_data['patient_city_name']
        state = request_data['patient_state_name']
        country = request_data['patient_country_name']
        zipcode = request_data['zipcode']
        approved = datetime.today()
        ex = Faker()
        ip = ex.ipv4()
        print(ip)

        date = datetime.today()
        device = socket.gethostname()
        print(device)

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM patient_sub_registration WHERE PATIENT_SUB_ID = %s', (patient_sub_Id,))
        account = cur.fetchone()
        if account and account["PATIENT_ID"] == patient_sub_Id:
            return 'Your user id duplicate please enter new value!', 400
        patient_data = patient_registration()
        try:
            patient_data.load(request_data)
            cur = mysql.connection.cursor()

            cur.execute(
                "insert into patient_sub_registration(PATIENT_ID,PATIENT_SUB_ID, PATIENT_AGE,PATIENT_EXPERIANCE, PATIENT_GENDER,"
                "PATIENT_LICENSE_NUMBER,FLAT_NO,STREET_NAME,CITY_NAME,STATE_NAME,COUNTRY_NAME,ZIP_CODE,"
                "PATIENT_APPROVED,PATIENT_IP,PATIENT_DATE_REGISTERED,PATIENT_DEVICE) values(%s,%s,%s,%s,%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,%s,%s,%s)",
                (patient_id, patient_sub_Id, age, patient_experience, gender, liciencenum, flatnum, street,
                 city, state, country, zipcode, approved, ip, date, device))
            mysql.connection.commit()
            return "successfully inserted", 200
        except ValidationError as e:
            print(e)
        return jsonify(e.messages)

    return "invalid parameters"


def max_id_value(c):
    max_value_query = "SELECT substring(patient_sub_id,6) as id FROM PATIENT_SUB_REGISTRATION WHERE substring(patient_sub_id," \
                      "6)=(SELECT MAX(CAST(SUBSTRING(patient_sub_id,6) AS SIGNED)) FROM PATIENT_SUB_REGISTRATION) "
    c.execute(max_value_query)
    result_value = c.fetchone()
    if result_value == 0 or result_value == 'None' or result_value == '' or result_value is None:
        result_value = 1;
        patient_sub_id = 'PAS000' + str(result_value)
        return patient_sub_id
    else:
        result_value = int(result_value[0]) + 1
        patient_sub_id = 'PAS000' + str(result_value)
        return patient_sub_id


if __name__ == '__main__':
    app.run()
