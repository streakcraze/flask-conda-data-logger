import base64
from io import BytesIO

from flask import Flask, render_template
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    return render_template("graph.html")


@app.route('/accelerometer')
def acc_data():
    df = pd.read_csv("./data/imu_data.csv")

    fig = Figure()
    ax = fig.subplots()

    xs = np.array(range(100))
    y1 = df["Acc_x"].to_numpy()[0:100]
    y2 = df["Acc_y"].to_numpy()[0:100]
    y3 = df["Acc_z"].to_numpy()[0:100]

    ax.set_ylim([min(min(y1), min(y2), min(y3))-2,
                max(max(y1), max(y2), max(y3))+2])
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Acceleration [m.s^2]')
    ax.set_title('3-axis accelerometer')

    ax.plot(xs, y1)
    ax.plot(xs, y2)
    ax.plot(xs, y3)
    ax.legend(['ax', 'ay', 'az'])

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'>"


@app.route('/gyroscope')
def gyro_data():
    df = pd.read_csv("./data/imu_data.csv")

    fig = Figure()
    ax = fig.subplots()

    xs = np.array(range(100))
    y1 = df["Gyro_x"].to_numpy()[0:100]
    y2 = df["Gyro_y"].to_numpy()[0:100]
    y3 = df["Gyro_z"].to_numpy()[0:100]

    ax.set_ylim([min(min(y1), min(y2), min(y3))-2,
                max(max(y1), max(y2), max(y3))+2])
    ax.set_xlabel('Time [s]')
    ax.set_ylabel(f"Degrees [{chr(176)}]")
    ax.set_title('3-axis gyroscope')

    ax.plot(xs, y1)
    ax.plot(xs, y2)
    ax.plot(xs, y3)
    ax.legend(['gx', 'gy', 'gz'])

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'>"


@app.route('/barometer')
def baro_data():
    df = pd.read_csv('./data/pressure_data.csv')

    fig = Figure()
    ax = fig.subplots()

    xs = np.array(range(18))
    y1 = df["Temperature (C)"].to_numpy()
    y2 = df["Atmospheric Pressure (mbar)"].to_numpy()

    ax.set_title('Temperature-pressure')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel(f"Temperature [{chr(176)} C]")
    ax.set_ylim(min(y1)-2, max(y1)+2)
    ax.plot(xs, y1, 'ro-')

    ax2 = ax.twinx()
    ax2.set_ylabel('Atmospheric Pressure (mbar)')
    ax2.set_ylim(min(y2)-100, max(y2)+100)

    ax2.plot(xs, y2, 'b^-')
    ax.legend(['temp'])
    ax2.legend(['pressure'])

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'>"


if __name__ == "__main__":
    app.run(debug=True)
