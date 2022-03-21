import base64
from io import BytesIO

from livereload import Server
from flask import Flask, render_template
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def figure():
    # Generate the figure "without using pyplot"
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'>"


@app.route('/accelerometer')
def acc_data():
    df = pd.read_csv("./data/imu_data.csv")

    fig = Figure()
    ax = fig.subplots()

    xs = np.array(range(20))
    y1 = df["Acc_x"].to_numpy()[0:20]
    y2 = df["Acc_y"].to_numpy()[0:20]
    y3 = df["Acc_z"].to_numpy()[0:20]

    ax.set_ylim([min(min(y1), min(y2), min(y3))-2,
                max(max(y1), max(y2), max(y3))+2])
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Acceleration [m.s^2]')

    ax.plot(xs, y1)
    ax.plot(xs, y2)
    ax.plot(xs, y3)
    ax.legend(['ax', 'ay', 'az'])

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("graph.html", data=data, title="3-axis Accelerometer")


@app.route('/gyroscope')
def gyro_data():
    df = pd.read_csv("./data/imu_data.csv")

    fig = Figure()
    ax = fig.subplots()

    xs = np.array(range(20))
    y1 = df["Gyro_x"].to_numpy()[0:20]
    y2 = df["Gyro_y"].to_numpy()[0:20]
    y3 = df["Gyro_z"].to_numpy()[0:20]

    ax.set_ylim([min(min(y1), min(y2), min(y3))-2,
                max(max(y1), max(y2), max(y3))+2])
    ax.set_xlabel('Time [s]')
    ax.set_ylabel(f"Degrees [{chr(176)}]")

    ax.plot(xs, y1)
    ax.plot(xs, y2)
    ax.plot(xs, y3)
    ax.legend(['gx', 'gy', 'gz'])

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("graph.html", data=data, title="3-axis Gyroscope")


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.serve()
