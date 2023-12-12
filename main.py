import csv
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_file
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, Float, or_, LargeBinary
from sqlalchemy.orm import relationship
from liq_noise import Lpe1m
from gas_noise import lpae_1m
import os

# app configuration
app = Flask(__name__)

app.config['SECRET_KEY'] = "kkkkk"

# CONNECT TO DB
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///NITTO_DB.db"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL1", "sqlite:///FCC_DB.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Creation of Database table
#
class products(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    name = Column(String(300))
    stock = Column(Integer)
    discount = Column(Float)
    # relationship as parent


with app.app_context():
    db.create_all()


# Routes

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')


@app.route('/gas-noise', methods=["GET", "POST"])
def gasNoise():
    return render_template('gas-noise.html')


@app.route('/liq-noise', methods=["GET", "POST"])
def liqNoise():
    initial_data = {'FD': None, 'FL': None, 'densityLiq': None, 'fi': None, 'iPressure': None, 'internalPipeDia': None,
                    'massFlowRate': None, 'oPressure': None, 'pipeWallThickness': None, 'reqCV': None, 'rw': None,
                    'seatDia': None, 'speedSoundLiq': None, 'vPressure': None, 'valveDia': None}
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        a = jsonify(data).json
        try:
            output_ = Lpe1m(float(a['fi'][0]), float(a['FD'][0]), float(a['reqCV'][0]), float(a['iPressure'][0]),
                            float(a['oPressure'][0]), float(a['vPressure'][0]),
                            float(a['densityLiq'][0]), float(a['speedSoundLiq'][0]), float(a['massFlowRate'][0]),
                            float(a['rw'][0]), float(a['FL'][0]),
                            float(a['seatDia'][0]), float(a['valveDia'][0]), 7800, float(a['pipeWallThickness'][0]),
                            5000,
                            1293, float(a['internalPipeDia'][0]), 343)
        except:
            output_ = "N/A"
        # print(output_)
        return render_template('liq-noise.html', data=a, value=output_)
    return render_template('liq-noise.html', data=initial_data, value=0)


# json_data = {
#     'data1': [30, 200, 100, 400, 150, 250],
#     'data2': [50, 20, 10, 40, 15, 25]
# }


# Server run
if __name__ == "__main__":
    app.run(debug=False)
