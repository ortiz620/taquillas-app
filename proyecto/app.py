import os
import json
import gspread
from flask import Flask, request, render_template
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Ruta del archivo secreto en Render
CREDENTIALS_PATH = "/etc/secrets/credentials.json"

# ID de la hoja de cálculo desde env variable
SPREADSHEET_ID = os.environ.get("GOOGLE_SPREADSHEET_ID")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/guardar_google_sheets", methods=["GET", "POST"])
def guardar_google_sheets():
    if request.method == "POST":
        try:
            # Leer los datos del formulario
            campo1 = request.form.get("campo1", "")
            campo2 = request.form.get("campo2", "")

            # Autenticación con Google Sheets
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
            client = gspread.authorize(creds)

            # Acceder a la hoja y agregar una fila
            sheet = client.open_by_key(SPREADSHEET_ID).sheet1
            sheet.append_row([campo1, campo2])

            return "✅ Datos guardados exitosamente en Google Sheets"
        except Exception as e:
            return f"❌ Error al guardar en Google Sheets: {str(e)}", 500

    return "Método no permitido", 405

if __name__ == "__main__":
    app.run(debug=True)

