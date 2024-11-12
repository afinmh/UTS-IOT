from flask import Flask, jsonify, request, render_template
import datetime

app = Flask(__name__)

data = {
    "suhumax": 0,
    "suhumin": 0,
    "suhurata": 0,
    "nilai_suhu_max_humid_max": [
        {
            "idx": 101,
            "suhu": 36,
            "humid": 36,
            "kecerahan": 25,
            "timestamp": "2010-09-18 07:23:48"
        },
        {
            "idx": 226,
            "suhu": 21,
            "humid": 36,
            "kecerahan": 27,
            "timestamp": "2011-05-02 12:29:34"
        }
    ],
    "month_year_max": [
        {"month_year": ""},
        {"month_year": ""}
    ]
}


def calculate_statistics():
    suhu_max = -float('inf')  
    suhu_min = float('inf')  
    suhu_total = 0          
    count = 0               
    oldest_timestamp = None 
    latest_timestamp = None 

    for entry in data["nilai_suhu_max_humid_max"]:
        suhu = entry["suhu"]
        timestamp = entry["timestamp"]

        if suhu > suhu_max:
            suhu_max = suhu
        if suhu < suhu_min:
            suhu_min = suhu

        suhu_total += suhu
        count += 1

        timestamp_obj = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        if not oldest_timestamp or timestamp_obj < oldest_timestamp:
            oldest_timestamp = timestamp_obj
        if not latest_timestamp or timestamp_obj > latest_timestamp:
            latest_timestamp = timestamp_obj

    suhu_rata_rata = suhu_total / count if count > 0 else 0

    data["suhumax"] = suhu_max
    data["suhumin"] = suhu_min
    data["suhurata"] = suhu_rata_rata
    data["month_year_max"][0]["month_year"] = oldest_timestamp.strftime("%Y-%m")
    data["month_year_max"][1]["month_year"] = latest_timestamp.strftime("%Y-%m")

@app.route('/')
def muncul():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    calculate_statistics() 
    return jsonify(data)

@app.route('/data', methods=['POST'])
def update_data():
    new_data = request.json
    if new_data:
        data.update(new_data)
        calculate_statistics()
        return jsonify({"message": "Data berhasil diperbarui", "data": data}), 200
    else:
        return jsonify({"message": "Data yang diberikan tidak valid"}), 400

if __name__ == '__main__':
    app.run(debug=True)
