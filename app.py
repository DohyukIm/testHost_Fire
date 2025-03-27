from flask import Flask, render_template, jsonify, request
import requests
import os
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/forest-fires')
def forest_fires():
    try:
        print("API 호출 시도 중...")
        api_url = "https://www.bigdata-forest.kr/todayFireGet?apiKey=tby1rdt7EaL6RCyxZNmWRQ37AhaQpl6hEQVr1MaKv5ix9fWHj9aw3pq0hsbTdzN0d0LcROuF0D0mFe69Dun8SjTTNEG9XsMsNppL9rQVqP0%253D"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(api_url, headers=headers)
        
        return response.text, 200, {'Content-Type': 'application/xml', 'Access-Control-Allow-Origin': '*'}
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"API 호출 오류: {str(e)}")
        return jsonify({"error": str(e), "details": error_details}), 500

@app.route('/api/forest-fire-detail')
def forest_fire_detail():
    try:
        fire_id = request.args.get('id')
        
        if not fire_id:
            return jsonify({"error": "ID 파라미터가 필요합니다"}), 400
        
        detail_url = f"http://mepv2.safekorea.go.kr/forestFires/showForestFiresDetail.do?frfrInfoId={fire_id}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(detail_url, headers=headers)
        
        if response.status_code != 200:
            return jsonify({"error": f"상세 정보 요청 실패: {response.status_code}"}), 500
        
        return response.text, 200, {'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*'}
    
    except Exception as e:
        error_details = traceback.format_exc()
        return jsonify({"error": str(e), "details": error_details}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)