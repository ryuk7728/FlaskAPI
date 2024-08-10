from flask import Flask, jsonify, request
import numpy as np
import random
from tensorflow.keras.models import load_model
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_parameters():
    k = 3
    api_input = request.args.get('type')
    
    model = load_model('trained_model.keras')
    scaling_factors = np.array([65, 1800, 105, 10, 450, 4.7, 1800, 17, 65, 400, 15, 365, 125, 40])
    scaling_factors = scaling_factors+50


    parameter_names = [
    "Engine Oil Pressure",
    "Engine Speed",
    "Engine Temperature",
    "Brake Control",
    "Transmission Pressure",
    "Pedal Sensor",
    "Water Fuel",
    "Fuel Level",
    "Fuel Pressure",
    "Fuel Temperature",
    "System Voltage",
    "Exhaust Gas Temperature",
    "Hydraulic Pump Rate",
    "Air Filter Pressure Drop"
    ]

    parameters = [
    {"name": "Engine Oil Pressure", "low": 25, "high": 65, "prob_failure": 1.0},
    {"name": "Engine Speed", "low": 0, "high": 1800, "prob_failure": 0.5},
    {"name": "Engine Temperature", "low": 0, "high": 105, "prob_failure": 1.0},
    {"name": "Brake Control", "low": 1, "high": 10, "prob_failure": 0.5},
    {"name": "Transmission Pressure", "low": 200, "high": 450, "prob_failure": 0.5},
    {"name": "Pedal Sensor", "low": 0, "high": 4.7, "prob_failure": 0.2},
    {"name": "Water Fuel", "low": 0, "high": 1800, "prob_failure": 1.0},
    {"name": "Fuel Level", "low": 1, "high": 17, "prob_failure": 0.2},
    {"name": "Fuel Pressure", "low": 35, "high": 65, "prob_failure": 0.2},
    {"name": "Fuel Temperature", "low": 0, "high": 400, "prob_failure": 1.0},
    {"name": "System Voltage", "low": 12.0, "high": 15.0, "prob_failure": 1.0},
    {"name": "Exhaust Gas Temperature", "low": 0, "high": 365, "prob_failure": 1.0},
    {"name": "Hydraulic Pump Rate", "low": 0, "high": 125, "prob_failure": 0.5},
    {"name": "Air Filter Pressure Drop", "low": 20, "high": 40, "prob_failure": 0.5},
    ]



    # Engine Parameters
    mu_oilpressure = 45
    sigma_oilpressure = 20
    eng_oilpressure = np.random.normal(mu_oilpressure, sigma_oilpressure)
    if eng_oilpressure < 0:
        eng_oilpressure = 10 + random.uniform(0, 5)
    if random.randint(1, k) == 1:
        eng_oilpressure = 65 + random.uniform(0, 5)

    mu_enginespeed = 900
    sigma_enginespeed = 450
    eng_speed = np.random.normal(mu_enginespeed, sigma_enginespeed)
    if eng_speed < 0:
        eng_speed = 600 + random.uniform(0, 5)
    if random.randint(1, k) == 1:
        eng_speed = 1800 + random.uniform(10, 100)

    mu_enginetemp = 52
    sigma_enginetemp = 26
    eng_temp = np.random.normal(mu_enginetemp, sigma_enginetemp)
    if eng_temp < 0:
        eng_temp = 30 + random.uniform(0, 5)
    if random.randint(1, k) == 1:
        eng_temp = 105 + random.uniform(1, 10)

    # Drive Parameters
    mu_brakecontrol = 5
    sigma_brakecontrol = 2.5
    brake_control = np.random.normal(mu_brakecontrol, sigma_brakecontrol)
    if brake_control < 0:
        brake_control = 2 + random.uniform(0, 1)
    if random.randint(1, k) == 1:
        brake_control = 1 - random.uniform(0, 1)

    mu_transpressure = 325
    sigma_transpressure = 62
    trans_pressure = np.random.normal(mu_transpressure, sigma_transpressure)
    if trans_pressure < 0:
        trans_pressure = 200 + random.uniform(0, 10)
    if random.randint(1, k) == 1:
        trans_pressure = 200 + random.uniform(10, 30)

    mu_pedalsens = 2.5
    sigma_pedalsens = 1.25
    pedal_sens = np.random.normal(mu_pedalsens, sigma_pedalsens)
    if pedal_sens < 0:
        pedal_sens = 1 + random.uniform(0, 0.5)
    if random.randint(1, k) == 1:
        pedal_sens = 4.7 + random.uniform(0.1, 3)

    # Fuel Parameters
    mu_waterfuel = 900
    sigma_waterfuel = 450
    water_fuel = np.random.normal(mu_waterfuel, sigma_waterfuel)
    if water_fuel < 0:
        water_fuel = 500 + random.uniform(0, 20)
    if random.randint(1, k) == 1:
        water_fuel = 1800 + random.uniform(10, 100)

    mu_fuellevel = 7.5
    sigma_fuellevel = 4
    fuel_level = np.random.normal(mu_fuellevel, sigma_fuellevel)
    if fuel_level < 0:
        fuel_level = 3 + random.uniform(0, 1)
    if random.randint(1, k) == 1:
        fuel_level = 1 - random.uniform(0.2, 1)

    mu_fuelpressure = 50
    sigma_fuelpressure = 7.5
    fuel_pressure = np.random.normal(mu_fuelpressure, sigma_fuelpressure)
    if fuel_pressure < 0:
        fuel_pressure = 40 + random.uniform(0, 2)
    if random.randint(1, k) == 1:
        fuel_pressure = 65 + random.uniform(0, 10)

    mu_fueltemp = 200
    sigma_fueltemp = 100
    fuel_temp = np.random.normal(mu_fueltemp, sigma_fueltemp)
    if fuel_temp < 0:
        fuel_temp = 120 + random.uniform(0, 10)
    if random.randint(1, k) == 1:
        fuel_temp = 400 + random.uniform(1, 30)

    # Miscellaneous Parameters
    mu_sysvolt = 13.5
    sigma_sysvolt = 0.75
    sys_volt = np.random.normal(mu_sysvolt, sigma_sysvolt)
    if sys_volt < 0:
        sys_volt = 10 + random.uniform(0, 1)
    if random.randint(1, k) == 1:
        sys_volt = 12 - random.uniform(0.1, 5)

    mu_exhausttemp = 182
    sigma_exhausttemp = 90
    exhaust_temp = np.random.normal(mu_exhausttemp, sigma_exhausttemp)
    if exhaust_temp < 0:
        exhaust_temp = 100 + random.uniform(0, 10)
    if random.randint(1, k) == 1:
        exhaust_temp = 365 + random.uniform(1, 30)

    mu_hydpump = 62
    sigma_hydpump = 31
    hyd_pump = np.random.normal(mu_hydpump, sigma_hydpump)
    if hyd_pump < 0:
        hyd_pump = 30 + random.uniform(0, 10)
    if random.randint(1, k) == 1:
        hyd_pump = 125 + random.uniform(1, 20)

    mu_airpressure = 30
    sigma_airpressure = 5
    air_pressure = np.random.normal(mu_airpressure, sigma_airpressure)
    if air_pressure < 0:
        air_pressure = 5 + random.uniform(0, 2)
    if random.randint(1, k) == 1:
        air_pressure = 20 - random.uniform(1, 5)

    
    x_test = np.loadtxt('x_test.txt')

    random_number = random.randint(1, 1000)

    x_testeg = x_test[random_number].reshape(1,14)
    print(np.round(x_testeg,2))
    x_testegscaled = x_testeg/scaling_factors

    
  

    y_pred = np.round(model.predict(x_testegscaled),2)
    xlist = x_testeg.tolist()[0]
    ylist = y_pred.tolist()[0]

    xlist = [round(val, 2) for val in xlist]


    for i in range(len(ylist)):
            if(ylist[i]>0.7):
                machineName = "machineName"
                machineID = "machineID"

                # Email credentials
                sender_email = "ryuk7728@gmail.com"
                receiver_email = "haeker969@gmail.com"
                password = "venk wgxx fkmy uwje"

                # Create the email
                subject = "Machine Failure"
                body =  machineName + " with ID " + machineID + " is malfunctioning with high probability of failure. The " + parameter_names[i] + " value is " + str(xlist[i]) + " which is beyond the ideal range from " +  str(parameters[i]["low"]) + " to " + str(parameters[i]["high"]) +". Please take immediate action."

                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject

                msg.attach(MIMEText(body, 'plain'))

                # Send the email
                try:
                    # Create a secure connection with the Gmail server
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
                    server.login(sender_email, password)
                    
                    text = msg.as_string()
                    server.sendmail(sender_email, receiver_email, text)
                    print("Email sent successfully!")
                except Exception as e:
                    print(f"Failed to send email: {e}")
                finally:
                    server.quit()  # Close the connection to the SMTP server
            if(ylist[i]>0.4 and ylist[i]<0.7):
                machineName = "machineName"
                machineID = "machineID"

                # Email credentials
                sender_email = "ryuk7728@gmail.com"
                receiver_email = "haeker969@gmail.com"
                password = "venk wgxx fkmy uwje"

                # Create the email
                subject = "Machine Failure"
                body =  machineName + " with ID " + machineID + " is malfunctioning with moderate probability of failure. The " + parameter_names[i] + " value is " + str(xlist[i]) + " which is not in the ideal range from " +  str(parameters[i]["low"]) + " to " + str(parameters[i]["high"]) +". Please take immediate action."

                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject

                msg.attach(MIMEText(body, 'plain'))

                # Send the email
                try:
                    # Create a secure connection with the Gmail server
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
                    server.login(sender_email, password)
                    
                    text = msg.as_string()
                    server.sendmail(sender_email, receiver_email, text)
                    print("Email sent successfully!")
                except Exception as e:
                    print(f"Failed to send email: {e}")
                finally:
                    server.quit()  # Close the connection to the SMTP server
            if(ylist[i]>0.1 and ylist[i]<0.3):
                machineName = "machineName"
                machineID = "machineID"

                # Email credentials
                sender_email = "ryuk7728@gmail.com"
                receiver_email = "haeker969@gmail.com"
                password = "venk wgxx fkmy uwje"

                # Create the email
                subject = "Machine Failure"
                body =  machineName + " with ID " + machineID + " is malfunctioning with low probability of failure. The " + parameter_names[i] + " value is " + str(xlist[i]) + " which is not in the ideal range from " +  str(parameters[i]["low"]) + " to " + str(parameters[i]["high"]) +". Please take immediate action."

                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject

                msg.attach(MIMEText(body, 'plain'))

                # Send the email
                try:
                    # Create a secure connection with the Gmail server
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
                    server.login(sender_email, password)
                    
                    text = msg.as_string()
                    server.sendmail(sender_email, receiver_email, text)
                    print("Email sent successfully!")
                except Exception as e:
                    print(f"Failed to send email: {e}")
                finally:
                    server.quit()  # Close the connection to the SMTP server

    

    if api_input == "data":
        return jsonify({
            "failure values": ylist,
            "parameter values": xlist
            
        })

    

    return jsonify({"error": "Invalid input"}), 400


if __name__ == '__main__':
    app.run(host = "0.0.0.0",port=5000,debug=True)
