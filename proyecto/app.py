from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

taquillas = []
cortes = {}
gastos = {}

# ✅ Conexión segura con Google Sheets
def connect_to_sheets():
    try:
        secret_path = "/etc/secrets/credentials.json"
        sheet_id = os.environ.get("GOOGLE_SPREADSHEET_ID")

        if not os.path.exists(secret_path) or not sheet_id:
            print("❌ Archivo JSON o SPREADSHEET_ID no encontrados")
            return None

        with open(secret_path, "r") as f:
            credentials_dict = json.load(f)

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        client = gspread.authorize(creds)
        return client.open_by_key(sheet_id)

    except Exception as e:
        print("❌ Error conectando con Google Sheets:", e)
        return None

@app.route('/')
def index():
    ingreso_total = sum(t['total'] for t in taquillas)
    gasto_total = sum(sum(g['monto'] for g in lista) for lista in gastos.values())
    neto_total = ingreso_total - gasto_total

    return render_template('index.html',
                           taquillas=taquillas,
                           cortes=cortes,
                           gastos=gastos,
                           ingreso_total=ingreso_total,
                           gasto_total=gasto_total,
                           neto_total=neto_total)

@app.route('/agregar_taquilla', methods=['POST'])
def agregar_taquilla():
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    taquillas.append({'nombre': nombre, 'precio': precio, 'inicial': 0, 'final': 0, 'total': 0})
    return redirect(url_for('index'))

@app.route('/actualizar_boletos', methods=['POST'])
def actualizar_boletos():
    for i, t in enumerate(taquillas):
        inicial = int(request.form.get(f'inicial_{i}', 0))
        final = int(request.form.get(f'final_{i}', 0))
        vendidos = max(0, final - inicial - 2)
        total = vendidos * t['precio']
        taquillas[i]['inicial'] = inicial
        taquillas[i]['final'] = final
        taquillas[i]['total'] = total
    return redirect(url_for('index'))

@app.route('/agregar_gasto', methods=['POST'])
def agregar_gasto():
    descripcion = request.form['descripcion']
    monto = float(request.form['monto'])
    hoy = datetime.now().strftime('%Y-%m-%d')
    if hoy not in gastos:
        gastos[hoy] = []
    gastos[hoy].append({'descripcion': descripcion, 'monto': monto})
    return redirect(url_for('index'))

@app.route('/guardar_google_sheets')
def guardar_google_sheets():
    try:
        sheet = connect_to_sheets()
        if not sheet:
            return "Google Sheets no configurado"

        hoy = datetime.now().strftime('%Y-%m-%d')
        try:
            worksheet = sheet.worksheet(hoy)
        except Exception as e:
            print(f"No existe hoja {hoy}, creando nueva... {e}")
            worksheet = sheet.add_worksheet(title=hoy, rows="100", cols="10")

        worksheet.clear()

        # Sección: Taquillas
        worksheet.append_row(["--------------------------------------"])
        worksheet.append_row(["TAQUILLAS DEL DÍA"])
        worksheet.append_row(["--------------------------------------"])
        worksheet.append_row(["Taquilla", "Inicial", "Final", "Precio", "Total"])
        for t in taquillas:
            worksheet.append_row([t['nombre'], t['inicial'], t['final'], t['precio'], t['total']])

        worksheet.append_row([""])  # Espacio vacío

        # Sección: Gastos
        worksheet.append_row(["--------------------------------------"])
        worksheet.append_row(["GASTOS DEL DÍA"])
        worksheet.append_row(["--------------------------------------"])
        worksheet.append_row(["Descripción", "Monto"])
        for g in gastos.get(hoy, []):
            worksheet.append_row([g['descripcion'], g['monto']])

        worksheet.append_row([""])  # Espacio vacío

        # Sección: Resumen
        ingreso_total = sum(t['total'] for t in taquillas)
        gasto_total = sum(g['monto'] for g in gastos.get(hoy, []))
        neto = ingreso_total - gasto_total

        worksheet.append_row(["--------------------------------------"])
        worksheet.append_row(["RESUMEN DEL DÍA"])
        worksheet.append_row(["--------------------------------------"])
        worksheet.append_row(["Ingreso Bruto", ingreso_total])
        worksheet.append_row(["Gasto Bruto", gasto_total])
        worksheet.append_row(["Ingreso Neto", neto])

        return redirect(url_for('index'))

    except Exception as e:
        print("🔥 ERROR GUARDANDO EN SHEETS:", e)
        return f"Error interno del servidor: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
