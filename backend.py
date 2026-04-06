from flask import Flask, request, jsonify, Response
import requests
import json

app = Flask(__name__)

API_URL = "http://arastir.sbs/api/adsoyad.php"

@app.route('/api/kisi', methods=['GET'])
def kisi_sorgula():
    ad = request.args.get('ad')
    soyad = request.args.get('soyad')
    
    if not ad or not soyad:
        return jsonify({
            "success": False,
            "error": "ad ve soyad parametreleri gerekli"
        }), 400
    
    response = requests.get(API_URL, params={
        'adi': ad,
        'soyadi': soyad
    })
    
    # UTF-8 decode et
    veri = response.json()
    
    # JSON'ı UTF-8 olarak dön
    return Response(
        json.dumps(veri, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8'
    )

@app.route('/api/kisi/filtreli', methods=['GET'])
def kisi_sorgula_filtreli():
    ad = request.args.get('ad')
    soyad = request.args.get('soyad')
    il = request.args.get('il')
    uyruk = request.args.get('uyruk')
    
    if not ad or not soyad:
        return jsonify({
            "success": False,
            "error": "ad ve soyad parametreleri gerekli"
        }), 400
    
    response = requests.get(API_URL, params={
        'adi': ad,
        'soyadi': soyad
    })
    
    veri = response.json()
    
    if veri.get('success') != 'true':
        return Response(
            json.dumps(veri, ensure_ascii=False, indent=2),
            mimetype='application/json; charset=utf-8'
        )
    
    sonuclar = veri['data']
    
    if il:
        sonuclar = [k for k in sonuclar if k.get('NUFUSIL') == il]
    if uyruk:
        sonuclar = [k for k in sonuclar if k.get('UYRUK') == uyruk]
    
    sonuc = {
        "success": True,
        "count": len(sonuclar),
        "data": sonuclar
    }
    
    return Response(
        json.dumps(sonuc, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
