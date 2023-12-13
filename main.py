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


# with app.app_context():
#     db.create_all()


# Routes

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')


@app.route('/gas-noise', methods=["GET", "POST"])
def gasNoise():
    initial_data = {'valveSize': None, 'valveOutletDiameter': None, 'ratedCV': None, 'reqCV': None, 'No': None,
                    'FLP': None,
                    'Iw': None, 'valveSizeUnit': 'm', 'IwUnit': 'm', 'A': None, 'xT': None, 'iPipeSize': None,
                    'oPipeSize': None,
                    'tS': None, 'Di': None, 'SpeedOfSoundinPipe_Cs': None, 'DensityPipe_Ps': None,
                    'densityUnit': 'kg/m3',
                    'SpeedOfSoundInAir_Co': None, 'densityAir_Po': None, 'atmPressure_pa': None,
                    'atmPres': 'pa',
                    'stdAtmPres_ps': None, 'stdAtmPres': 'pa', 'sigmaEta': None, 'etaI': None, 'Fp': None,
                    'massFlowrate': None, 'massFlowrateUnit': 'kg/s', 'iPres': None, 'iPresUnit': 'pa',
                    'oPres': None, 'oPresUnit': 'pa', 'inletDensity': None, 'iAbsTemp': None, 'iAbsTempUnit': 'K',
                    'specificHeatRatio_gamma': None, 'molecularMass': None, 'mMassUnit': 'kg/kmol',
                    'internalPipeDia': None,
                    'aEta': None, 'stp': None, 'R': None, 'RUnit': "J/kmol x K", 'fs': None}
    if request.method == "POST":
        data = request.form.to_dict(flat=False)
        a = jsonify(data).json
        try:
            output_ = lpae_1m(float(a['specificHeatRatio_gamma'][0]), float(a['iPres'][0]), float(a['oPres'][0]), float(a['FLP'][0]), float(a['Fp'][0]),
                              float(a['inletDensity'][0]), float(a['massFlowrate'][0]), float(a['aEta'][0]), float(8314), float(a['iAbsTemp'][0]),
                              float(a['molecularMass'][0]), float(a['oPipeSize'][0]), float(a['internalPipeDia'][0]), float(a['stp'][0]), float(a['No'][0]),
                              float(a['A'][0]), float(a['Iw'][0]), float(a['reqCV'][0]), float(5000),
                              float(343), float(a['valveSize'][0]), float(a['tS'][0]), float(1), float(a['atmPressure_pa'][0]),
                              float(101325), float(8000), -3.002)
        except KeyError:
            output_ = "N/A"
        return render_template('liq-gas.html', value=round(output_, 2), data=a)
    return render_template('liq-gas.html', data=initial_data, value=0)


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
        return render_template('liq-noise.html', data=a, value=output_)
    return render_template('liq-noise.html', data=initial_data, value=0)


# json_data = {
#     'data1': [30, 200, 100, 400, 150, 250],
#     'data2': [50, 20, 10, 40, 15, 25]
# }


# Server run
if __name__ == "__main__":
    app.run(debug=False)
