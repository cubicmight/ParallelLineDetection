import json
import os.path
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
import cvzone
from flask import render_template, flash, redirect, url_for, Response, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, UserLogData
from image_processing import image_processing

current_direction_image = None
camera = None

with app.app_context():
    UserLogData.query.delete()
    db.session.commit()
    basedir = os.path.abspath(os.path.dirname(__file__))

    image_file_name = "direction_arrow.png"
    full_image_path = os.path.join(basedir, 'static', image_file_name)
    if os.path.exists(full_image_path):
        # validate the image
        current_direction_image = cv2.imread(full_image_path, cv2.IMREAD_UNCHANGED)
    else:
        print("cannot find image")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/logs')
def logs():
    data = db.session.query(UserLogData.data).all()
    row = []
    for d in data:
        row.append(d[0])
    return row


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)





# Image processing
def format_video(cap):
    global output, gray
    output = cap.copy()
    gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0);
    gray = cv2.medianBlur(gray, 5)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 3.5)
    kernel = np.ones((3, 3), np.uint8)
    gray = cv2.erode(gray, kernel, iterations=1)
    gray = cv2.dilate(gray, kernel, iterations=1)
    # find the contours from the thresholded image
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    output = cv2.drawContours(output, contours, -1, (0, 255, 0), 2)

    a1 = contours[0][:, 0]
    a2 = contours[1][:, 0]
    # interpolate(a1, a2)
    return output

def gen_frame():
    """Video streaming generator function."""
    global camera
    if not camera:
        basedir = os.path.abspath(os.path.dirname(__file__))

        image_file_name = "../videos/lane detection.mp4"
        full_image_path = os.path.join(basedir, image_file_name)
        if not os.path.exists(full_image_path):
            print("cannot find image")
            exit(-1)

        cap = cv2.VideoCapture(full_image_path)
        # fixed_cap = format_video(cap)

    else:
        cap = camera
    while cap:
        (grabbed, frame) = cap.read()
        if grabbed:
            global current_direction_image
            imgResult = format_video(frame)  # 750, 400 , current_direction_image, [930, 500])
            ret, buffer = cv2.imencode('.jpg', imgResult)

            if ret:
                convert = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')
                # concatenate frame one by one and show result
    cap.release()


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
