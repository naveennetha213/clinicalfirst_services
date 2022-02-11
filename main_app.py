import logging
import socket
from datetime import datetime, timedelta
from functools import wraps
import jwt
from faker import Faker
from flask import request, Flask, jsonify, session
from flask_mysqldb import MySQL
from marshmallow import ValidationError, Schema, fields, validate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'raghu'
app.config['MYSQL_DB'] = 'clinicalfirst_services'
app.config['SECRET_KEY'] = 'raghu'
mysql = MySQL(app)


# default root:-
# @app.route("/")
# def default():
#     return "<h1>Test Message from Empty root !!!</h1>"


# Validations:-
class User_SignUp(Schema):
    # user_signupid = fields.String(validate=validate.Regexp(r'[A-Za-z0-9]+'))
    username = fields.String(validate=validate.Regexp(r'[A-Za-z]+'))
    email = fields.Email(required=True)
    phone = fields.String(validate=validate.Regexp(r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$'),
                          required=True)
    password = fields.String(validate=validate.Regexp(r'^[A-Za-z0-9@#$%^&+=]{8,32}'))
    ip = fields.String(validate=validate.Regexp(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|'
                                                r'[01]?[0-9][0-9]?)$'))
    # date = fields.String(validate=validate.Regexp(r'^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$'))


# Signup:-
@app.route('/user/insert', methods=['POST'])
def User_signup():
    # @wraps()
    # def wrappersUserSignup(*args, **kwargs):
    if 'username' in request.json and 'password' in request.json \
            and 'email' in request.json and 'phone' in request.json:
        request_data = request.json
        # user_signupid = request_data['user_signupid']
        username = request_data['username']
        email = request_data['email']
        phone = request_data['phone']
        password = request_data['password']
        hassedpassword = generate_password_hash(password)
        # userip = request_data['ip']
        ex = Faker()
        ip = ex.ipv4()
        print(ip)
        # date = request_data['date']
        device = socket.gethostname()
        print(device)

        # UserId Pattern for Insert Operation:-
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT USER_ID FROM user_signup")
        last_user_id = cursor.rowcount
        print('----------------------------------')
        print("Last Inserted ID is: " + str(last_user_id))
        pattern = 'US000'  # pattern = ooo
        last_user_id += 1
        # add_value = 00
        # pattern += 1 # pattern incremnting always by 1:-
        user_id = pattern + str(last_user_id)  # pass 'user_id' value in place holder exactly
        # User Id pattern Code End #

        # Cursor:-
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user_signup WHERE USER_MAIL_ID = %s OR USER_PHONE_NUMBER = %s', (email, phone))
        account = cursor.fetchone()

        if account and account[2] == email:
            return 'Your Email already exist please enter new Email !', 400

        elif account and account[3] == phone:
            return "Your Phone number is duplicate please enter new number!!!", 400

        # elif account:
        #     return fun(account, args, *kwargs)

        result = User_SignUp()
        try:
            # Validate request body against schema data types
            result.load(request_data)
            cur = mysql.connection.cursor()
            cur.execute(
                "insert into user_signup(USER_ID, USER_NAME, USER_MAIL_ID, USER_PHONE_NUMBER, USER_PASSWORD,"
                "USER_IP, USER_DEVICE) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                (user_id, username, email, phone, hassedpassword, ip, device))
            mysql.connection.commit()
            logging.info("successfully registered")

            # return fun("successfully inserted", args, *kwargs), 201
            return "Succesfully Inserted", 200
        except ValidationError as e:
            # logTo_database("/user/insert", "user_signup", e, 401)
            return (e.messages), 400
    return "Invalid input", 200


# return wrappersUserSignup

# Login:-
def logined(func):
    @wraps(func)
    def Wrapperlogin(*args, **kwargs):
        if 'email' in request.json and 'password' in request.json:
            email = request.json["email"]
            # phone = request.json['phonenumber']
            pw = request.json["password"]

            logging.warning('Watch out!')

            cur = mysql.connection.cursor()
            # cur.execute("select USER_PASSWORD from user_signup where USER_MAIL_ID = %s", (email,))
            cur.execute('SELECT * FROM USER_SIGNUP WHERE USER_MAIL_ID = %s', (email,))
            details = cur.fetchone()
            # # If account exists in accounts table in out database
            # if details:
            #     # Create session data, we can access this data in other routes
            #     session['loggedin'] = True
            #     session['id'] = details['USER_ID']
            #     session['username'] = details['USER_NAME']
            #     # Redirect to home page
            # else:
            #     # Account doesnt exist or username/password incorrect
            #     return "Incorrect username/password!"
            #
            if details is None:
                return 'Email not registered', 401
            hashed_password = details[4]
            password_match = check_password_hash(hashed_password, pw)

            if password_match:
                # generate the JWT Token
                data = {
                    'user_mail': email,
                    'password': hashed_password,
                    "user_id": details[1],
                    'exp': datetime.utcnow() + timedelta(minutes=2)}
                token = jwt.encode(data, app.config['SECRET_KEY'], algorithm='HS256')
                data['token'] = token
                return func(data, *args, **kwargs)
            else:
                logging.error("Invalid credentials")
                return "invalid credentials", 401
        return "Insufficient parameters", 400

    return Wrapperlogin


@app.route('/user/login', methods=["POST"])
@logined
def login_testing(data):
    # log_data(data)
    return data['token']


def token_validate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({"message": "Token is invalid"})

        return f(data, *args, **kwargs)

    return decorated


@app.route('/user/logined', methods=['GET'])
@token_validate
def token_testing(data):
    return data


# Logout:-
@app.route('/user/logout', methods=['GET'])
def logout():
    # Remove session data, this will log the user out
    # session.pop('loggedin', None)
    # session.pop('id', None)
    # session.pop('username', None)
    # return redirect(url_for('index'))
    cur = mysql.connection.cursor()
    cur.execute('select USER_MAIL_ID from user_signup')
    Email_id = cur.fetchall()
    Login_Email_id = Email_id[-1]
    print(Login_Email_id)
    # =============================== #
    # date and time object:-
    # now = datetime.now()
    # logout_time = now.strftime('%Y-%m-%d %H:%M:%S')
    # cur = mysql.connection.cursor()
    # cur.execute('insert into logins_data(LOGIN_EMAIL_ID, LOGOUT_TIME) values(%s, %s)', (id, logout_time))
    # return "User " + Login_Email_id + "Logged Out Successfully !!!"
    return "User Loggedout Successfully !!!"


# Medical_Equipments:-
# Equipment_Category:-
@app.route('/eqp_cat/insert', methods=['POST'])
def equipment_category():
    if 'cat_id' in request.json and 'cat_name' in request.json:
        request_data = request.json
        cat_id = request_data['cat_id']
        cat_name = request_data['cat_name']

        # Cursor:-
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM equipment_category WHERE category_ID = %s OR category_name = %s',
                       (cat_id, cat_name))
        eqpuipment = cursor.fetchone()

        if eqpuipment and eqpuipment[0] == cat_id:
            return 'Category_Id already exist please enter new Cat_Id !', 400

        elif eqpuipment and eqpuipment[1] == cat_name:
            return "Category_Name already exist please enter new Cat_Name !", 400

        result = equipment_category()
        try:
            # Validate request body against schema data types
            result.load(request_data)
            cur = mysql.connection.cursor()
            cur.execute(
                "insert into equipment_category(CATEGORY_ID, CATEGORY_NAME)"
                "VALUES(%s, %s)", (cat_id, cat_name))
            mysql.connection.commit()
            logging.info("successfully registered")

            # return fun("successfully inserted", args, *kwargs), 201
            return "Succesfully Inserted", 200
        except ValidationError as e:
            # logTo_database("/user/insert", "user_signup", e, 401)
            return (e.messages), 400
    return "Invalid input", 200


# Equipment_Type:-
@app.route('/eqp_type/insert', methods=['POST'])
def equipment_type():
    if 'type_id' in request.json and 'type_name' in request.json:
        request_data = request.json
        type_id = request_data['type_id']
        type_name = request_data['type_name']

        # Cursor:-
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM equipment_type WHERE TYPE_ID = %s OR TYPE_NAME = %s',
                       (type_id, type_name))
        type = cursor.fetchone()

        if type and type[0] == type_id:
            return 'Type_Id already exist please enter new Type_Id !', 400

        elif type and type[1] == type_name:
            return "Type_Name already exist please enter new Type_Name !", 400

        result = equipment_type()
        try:
            # Validate request body against schema data types
            result.load(request_data)
            cur = mysql.connection.cursor()
            cur.execute(
                "insert into equipment_type(TYPE_ID, TYPE_NAME)"
                "VALUES(%s, %s)", (type_id, type_name))
            mysql.connection.commit()
            logging.info("successfully registered")

            # return fun("successfully inserted", args, *kwargs), 201
            return "Succesfully Inserted", 200
        except ValidationError as e:
            # logTo_database("/user/insert", "user_signup", e, 401)
            return (e.messages), 400
    return "Invalid input", 200


# Equipment_Recommendation:-
@app.route('/eqp_recommendation/insert', methods=['POST'])
def equipment_recommendation():
    if 'rec_id' in request.json and 'rec_name' in request.json:
        request_data = request.json
        rec_id = request_data['rec_id']
        rec_name = request_data['rec_name']

        # Cursor:-
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM equipment_recommendations WHERE RECOMMENDATION_ID = %s OR RECOMMENDATION_NAME = %s',
            (rec_id, rec_name))
        recommendation = cursor.fetchone()

        if recommendation and recommendation[0] == rec_id:
            return 'Recommendation_Id already exist please enter new Recommendation_Id !', 400

        elif recommendation and recommendation[1] == rec_name:
            return "Recommendation_Name already exist please enter new Recommendation_Name !", 400

        result = equipment_recommendation()
        try:
            # Validate request body against schema data types
            result.load(request_data)
            cur = mysql.connection.cursor()
            cur.execute(
                "insert into equipment_recommendations(RECOMMENDATION_ID, RECOMMENDATION_NAME)"
                "VALUES(%s, %s)", (rec_id, rec_name))
            mysql.connection.commit()
            logging.info("successfully registered")

            # return fun("successfully inserted", args, *kwargs), 201
            return "Succesfully Inserted", 200
        except ValidationError as e:
            # logTo_database("/user/insert", "user_signup", e, 401)
            return (e.messages), 400
    return "Invalid input", 200


# Doctors_Table:-
@app.route('/doctor/insert', methods=['POST'])
def doctors_list():
    if 'doc_id' in request.json and 'doc_name' in request.json:
        request_data = request.json
        doc_id = request_data['doc_id']
        doc_name = request_data['doc_name']

        # Cursor:-
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM doctors_table WHERE DOCTOR_ID = %s OR DOCTOR_NAME = %s',
            (doc_id, doc_name))
        doctors = cursor.fetchone()

        if doctors and doctors[0] == doc_id:
            return 'Doctor_Id already exist please enter new Doctor_Id !', 400

        elif doctors and doctors[1] == doc_name:
            return "Doctor_Name already exist please enter new Doctor_Name !", 400

        result = doctors_list()
        try:
            # Validate request body against schema data types
            result.load(request_data)
            cur = mysql.connection.cursor()
            cur.execute(
                "insert into doctors_table(DOCTOR_ID, DOCTOR_NAME)"
                "VALUES(%s, %s)", (doc_id, doc_name))
            mysql.connection.commit()
            logging.info("successfully registered")

            # return fun("successfully inserted", args, *kwargs), 201
            return "Succesfully Inserted", 200
        except ValidationError as e:
            # logTo_database("/user/insert", "user_signup", e, 401)
            return (e.messages), 400
    return "Invalid input", 200


# Hospitals_Table:-
@app.route('/hospital/insert', methods=['POST'])
def hospitals_list():
    if 'hosp_id' in request.json and 'hosp_name' in request.json:
        request_data = request.json
        hosp_id = request_data['hosp_id']
        hosp_name = request_data['hosp_name']

        # Cursor:-
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM hospitals_table WHERE HOSPITAL_ID = %s OR HOSPITAL_NAME = %s',
            (hosp_id, hosp_name))
        hospitals = cursor.fetchone()

        if hospitals and hospitals[0] == hosp_id:
            return 'Doctor_Id already exist please enter new Doctor_Id !', 400

        elif hospitals and hospitals[1] == hosp_name:
            return "Doctor_Name already exist please enter new Doctor_Name !", 400

        result = hospitals_list()
        try:
            # Validate request body against schema data types
            result.load(request_data)
            cur = mysql.connection.cursor()
            cur.execute(
                "insert into hospitals_table(HOSPITAL_ID, HOSPITAL_NAME)"
                "VALUES(%s, %s)", (hosp_id, hosp_name))
            mysql.connection.commit()
            logging.info("successfully registered")

            # return fun("successfully inserted", args, *kwargs), 201
            return "Succesfully Inserted", 200
        except ValidationError as e:
            # logTo_database("/user/insert", "user_signup", e, 401)
            return (e.messages), 400
    return "Invalid input", 200


# MAIN app To Run the Flask Script:-
if __name__ == "__main__":
    app.run(debug=True)
