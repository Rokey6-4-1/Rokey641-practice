
from flask import Flask, jsonify ,  render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)



def data_current():
    with open('pd_li.json', 'r') as f:
    
        data_list = json.load(f)
    return data_list

def data_forecast():
    with open('df_summary.json', 'r') as f:
    
        data_list = json.load(f)
    return data_list






@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')



@app.route('/api/current', methods=['GET'])
def get_current():
    
    try:
        current= data_current()
        return jsonify(current)
    
    except Exception as e:
        print(f"❌ 에러: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    
    try:
        forecast = data_forecast()
        return jsonify(forecast)
    
    except Exception as e:
        print(f"❌ 에러: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """API 상태 확인"""
    return jsonify({
        "status": "ok",
        "message": "Weather API is running"
    })


@app.errorhandler(404)
def not_found(error):
    """404 에러 핸들러"""
    return jsonify({
        "error": "Not Found",
        "message": "파일을 찾을 수 없습니다"
    }), 404


if __name__ == '__main__':
    
    
    app.run(debug=True,host='0.0.0.0',port=5000)
