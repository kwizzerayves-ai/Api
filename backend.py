from flask import Flask, request, jsonify, Response
import requests
import json
import os

app = Flask(__name__)

API_URL = "http://arastir.sbs/api/adsoyad.php"

@app.route('/api/kisi', methods=['GET'])
def kisi_sorgula():
    ad = request.args.get('ad')
    soyad = request.args.get('soyad')
    
    if not ad or not soyad:
        return Response(
            json.dumps({"success": False, "error": "ad ve soyad parametreleri gerekli"}, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
            status=400
        )
    
    try:
        response = requests.get(API_URL, params={
            'adi': ad,
            'soyadi': soyad
        }, timeout=10)
        
        # Eğer API hata dönerse
        if response.status_code != 200:
            return Response(
                json.dumps({
                    "success": False, 
                    "error": f"API hatası: {response.status_code}"
                }, ensure_ascii=False),
                mimetype='application/json; charset=utf-8',
                status=response.status_code
            )
        
        # JSON parse et
        try:
            veri = response.json()
        except:
            return Response(
                json.dumps({
                    "success": False, 
                    "error": "API geçersiz yanıt döndü"
                }, ensure_ascii=False),
                mimetype='application/json; charset=utf-8',
                status=500
            )
        
        return Response(
            json.dumps(veri, ensure_ascii=False, indent=2),
            mimetype='application/json; charset=utf-8'
        )
        
    except requests.exceptions.RequestException as e:
        return Response(
            json.dumps({
                "success": False, 
                "error": f"Bağlantı hatası: {str(e)}"
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8',
            status=500
        )

@app.route('/health', methods=['GET'])
def health():
    # Orijinal API'yi kontrol et
    try:
        test_response = requests.get(API_URL, params={'adi': 'test', 'soyadi': 'test'}, timeout=5)
        api_status = "ok" if test_response.status_code == 200 else "error"
    except:
        api_status = "down"
    
    return jsonify({
        "status": "ok",
        "api_status": api_status,
        "message": "Service is running"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
