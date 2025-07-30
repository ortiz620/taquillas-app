import os
import gspread
from flask import Flask, request, render_template
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Ruta del archivo credentials.json almacenado como Secret File en Render
CREDENTIALS_PATH = "/etc/secrets/credentials.json"

# ID del Google Sheet desde Environment Variable
SPREADSHEET_ID = os.environ.get("GOOGLE_SPREADSHEET_ID")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/guardar_google_sheets", methods=["POST"])
def guardar_google_sheets():
    try:
        # Recoger datos del formulario
        campo1 = request.form.get("campo1", "")
        campo2 = request.form.get("campo2", "")

        # Definir el alcance y cargar credenciales
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
        client = gspread.authorize(creds)

        # Abrir el Google Sheet y agregar una fila
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        sheet.append_row([campo1, campo2])

        return "✅ Datos guardados exitosamente en Google Sheets"
    except Exception as e:
        return f"❌ Error al guardar en Google Sheets: {str(e)}", 500

# Configuración para que Render exponga el puerto correcto
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
