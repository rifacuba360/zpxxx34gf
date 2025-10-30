from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import html

# ==========================
# ⚙️ CONFIGURACIÓN
# ==========================
BOT_TOKEN = os.getenv("TU_TOKEN_AQUI") or "TU_TOKEN_AQUI"
ADMIN_ID = os.getenv("TU_ID_ADMIN") or "TU_ID_ADMIN"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

app = Flask(__name__, static_folder='.', static_url_path='')

# ==========================
# 🌐 RUTA HTML PRINCIPAL
# ==========================
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ==========================
# 📤 RUTA DE NOTIFICACIÓN
# ==========================
@app.route('/notificar', methods=['POST'])
def notificar():
    try:
        data = request.get_json()
        nombre = html.escape(data.get('nombre', ''))
        mensaje = html.escape(data.get('mensaje', ''))

        texto = (
            f"📨 <b>Nueva notificación desde formulario</b>\n\n"
            f"👤 <b>Nombre:</b> {nombre}\n"
            f"💬 <b>Mensaje:</b> {mensaje}"
        )

        # Enviar solo al administrador
        resp = requests.post(API_URL, json={
            "chat_id": ADMIN_ID,
            "text": texto,
            "parse_mode": "HTML"
        })

        if resp.status_code != 200:
            return jsonify(error="No se pudo enviar a Telegram"), 500

        return jsonify(success=True)
    except Exception as e:
        print("Error:", e)
        return jsonify(error="Error interno del servidor"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
