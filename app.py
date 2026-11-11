import os
import json
from flask import Flask, send_file, request, redirect, url_for, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# ==========================================
# 1. CONFIGURACIÓN DE IA Y ESCUELA
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "TU_GEMINI_API_KEY_AQUI")
genai.configure(api_key=GEMINI_API_KEY)

ESCUELA_NOMBRE = "ETP N° 394"
REPORTES_DB = []

# ==========================================
# 2. MOTOR DE ANÁLISIS CON IA
# ==========================================
def analizar_reporte_con_ia(texto_reporte, emociones_seleccionadas, frecuencia, lugar):
    prompt = f"""
    Eres el motor de IA de 'Voz Segura', para la {ESCUELA_NOMBRE}.
    Analiza el reporte confidencial enviado por un estudiante:
    - Descripción: "{texto_reporte}"
    - Emociones: {emociones_seleccionadas}
    - Frecuencia: {frecuencia}
    - Lugar: {lugar}

    Devuelve EXCLUSIVAMENTE un JSON con esta estructura exacta:
    {{
      "nivel_riesgo": "Verde" | "Amarillo" | "Rojo",
      "resumen_caso": "Resumen claro de la situación para el plantel docente.",
      "emociones_detectadas": ["Emoción"],
      "recomendacion_docente": "Protocolo de intervención institucional y una actividad pedagógica concreta para realizar en el aula orientada a la concientización y prevención.",
      "consejo_estudiante": "Mensaje de contención, empatía y consejo personalizado y seguro para el alumno según su situación individual."
    }}
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except:
        return {
            "nivel_riesgo": "Amarillo",
            "resumen_caso": texto_reporte[:120] + "...",
            "emociones_detectadas": emociones_seleccionadas,
            "recomendacion_docente": "Realizar una tutoría grupal y proponer un taller de convivencia y escucha activa en el curso.",
            "consejo_estudiante": "Gracias por expresarte. Recordá que no estás solo/a y que en la escuela hay adultos dispuestos a escucharte y ayudarte."
        }

# ==========================================
# 3. DISEÑOS HTML OPTIMIZADOS PARA MÓVIL
# ==========================================

# Página principal con QR adaptados para pantallas verticales de celulares
HTML_INDEX = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acceso - Voz Segura</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
</head>
<body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white p-6 sm:p-8 rounded-3xl shadow-xl text-center max-w-sm w-full space-y-6 border border-slate-100">
        <div class="space-y-2">
            <span class="inline-block bg-indigo-50 text-indigo-600 font-bold text-xs px-3 py-1 rounded-full uppercase tracking-wider">Plataforma Oficial</span>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900">Voz Segura IA 🛡️</h1>
            <p class="text-slate-500 font-medium text-sm">{{ escuela }}</p>
        </div>
        
        <div class="space-y-4 pt-2">
            <!-- QR Estudiantes -->
            <div class="p-4 border border-slate-100 rounded-2xl bg-indigo-50/30 shadow-sm space-y-3">
                <h3 class="font-bold text-sm text-indigo-900">Acceso Estudiantes</h3>
                <div id="qr-estudiantes" class="flex justify-center bg-white p-3 rounded-xl shadow-sm inline-block"></div>
                <div>
                    <a href="/reportar" class="inline-block w-full bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-4 rounded-xl shadow-md transition-all">Ir al formulario de reporte</a>
                </div>
            </div>
            
            <!-- QR Docentes -->
            <div class="p-4 border border-slate-100 rounded-2xl bg-slate-50 shadow-sm space-y-3">
                <h3 class="font-bold text-sm text-slate-700">Acceso Docentes</h3>
                <div id="qr-docentes" class="flex justify-center bg-white p-3 rounded-xl shadow-sm inline-block"></div>
                <div>
                    <a href="/panel/institucional" class="inline-block w-full bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold py-2.5 px-4 rounded-xl shadow-md transition-all">Ver panel institucional</a>
                </div>
            </div>
        </div>
    </div>

    <script>
        const baseUrl = "https://easily-sip-compile.ngrok-free.dev";
        
        new QRCode(document.getElementById("qr-estudiantes"), {
            text: baseUrl + "/reportar",
            width: 130,
            height: 130
        });

        new QRCode(document.getElementById("qr-docentes"), {
            text: baseUrl + "/panel/institucional",
            width: 130,
            height: 130
        });
    </script>
</body>
</html>
"""

# Formulario de estudiantes optimizado en formato vertical tipo app móvil
HTML_REPORTE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reportar - Voz Segura</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 min-h-screen py-6 px-3 sm:px-4">
<div class="max-w-md mx-auto bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
    <div class="bg-indigo-600 p-6 text-white text-center space-y-1">
        <h1 class="text-xl font-bold">Voz Segura</h1>
        <p class="text-xs text-indigo-100">{{ escuela }} - Espacio confidencial</p>
    </div>
    
    <form method="POST" class="p-5 sm:p-6 space-y-5">
        <div class="space-y-4 border-b border-slate-100 pb-5">
            <h2 class="text-xs font-bold uppercase tracking-wider text-indigo-600">1. Tus Datos</h2>
            <div>
                <label class="block font-bold text-slate-700 text-xs mb-1.5">Nombre:</label>
                <input type="text" name="nombre" required class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm outline-none focus:bg-white focus:ring-2 focus:ring-indigo-500" placeholder="Tu nombre">
            </div>
            <div>
                <label class="block font-bold text-slate-700 text-xs mb-1.5">Apellido:</label>
                <input type="text" name="apellido" required class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm outline-none focus:bg-white focus:ring-2 focus:ring-indigo-500" placeholder="Tu apellido">
            </div>
            <div>
                <label class="block font-bold text-slate-700 text-xs mb-1.5">Curso:</label>
                <input type="text" name="curso" required class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm outline-none focus:bg-white focus:ring-2 focus:ring-indigo-500" placeholder="Ej: 3ro A">
            </div>
        </div>

        <div class="space-y-4 border-b border-slate-100 pb-5">
            <h2 class="text-xs font-bold uppercase tracking-wider text-indigo-600">2. La Situación</h2>
            <div>
                <label class="block font-bold text-slate-700 text-xs mb-1.5">¿Qué sucede?:</label>
                <textarea name="texto" rows="3" required class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm outline-none focus:bg-white focus:ring-2 focus:ring-indigo-500" placeholder="Describí la situación con confianza..."></textarea>
            </div>
            <div>
                <label class="block font-bold text-slate-700 text-xs mb-2">¿Cómo te sentís?:</label>
                <div class="grid grid-cols-2 gap-2 text-xs">
                    <label class="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center cursor-pointer hover:bg-slate-100"><input type="checkbox" name="emociones" value="Miedo" class="mr-2 w-4 h-4 text-indigo-600"> 😨 Miedo</label>
                    <label class="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center cursor-pointer hover:bg-slate-100"><input type="checkbox" name="emociones" value="Tristeza" class="mr-2 w-4 h-4 text-indigo-600"> 😢 Tristeza</label>
                    <label class="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center cursor-pointer hover:bg-slate-100"><input type="checkbox" name="emociones" value="Exclusión" class="mr-2 w-4 h-4 text-indigo-600"> 🫂 Exclusión</label>
                    <label class="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center cursor-pointer hover:bg-slate-100"><input type="checkbox" name="emociones" value="Amenaza" class="mr-2 w-4 h-4 text-indigo-600"> ⚠️ Amenazas</label>
                </div>
            </div>
        </div>

        <div class="space-y-4">
            <h2 class="text-xs font-bold uppercase tracking-wider text-indigo-600">3. Contexto</h2>
            <div class="grid grid-cols-1 gap-3">
                <div>
                    <label class="block font-bold text-slate-700 text-xs mb-1.5">Frecuencia:</label>
                    <select name="frecuencia" class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm outline-none focus:bg-white focus:ring-2 focus:ring-indigo-500">
                        <option value="Ocasional">Ocasional</option>
                        <option value="Varias veces por semana">Varias veces por semana</option>
                        <option value="Todos los días">Todos los días</option>
                    </select>
                </div>
                <div>
                    <label class="block font-bold text-slate-700 text-xs mb-1.5">Lugar:</label>
                    <input type="text" name="lugar" required placeholder="Ej: Patio, Aula, Redes" class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm outline-none focus:bg-white focus:ring-2 focus:ring-indigo-500">
                </div>
            </div>
        </div>

        <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3.5 rounded-xl shadow-lg transition-all text-sm mt-2">Enviar Confidencial</button>
    </form>
</div>
</body>
</html>
"""

HTML_EXITO = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enviado</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white p-6 sm:p-8 rounded-3xl text-center shadow-xl max-w-sm w-full space-y-4 border border-slate-100">
        <div class="w-14 h-14 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto text-2xl font-bold">✓</div>
        <h2 class="text-xl font-bold text-slate-900">¡Reporte enviado!</h2>
        <p class="text-slate-500 text-xs">El equipo de orientación y conducción de la {{ escuela }} fue notificado de forma segura.</p>
        
        {% if ultimo_consejo %}
        <div class="bg-indigo-50/60 p-4 rounded-2xl text-left border border-indigo-100 mt-3 space-y-1">
            <strong class="block text-indigo-900 text-xs">💡 Consejo de la IA para vos:</strong>
            <p class="text-indigo-950 text-xs leading-relaxed">{{ ultimo_consejo }}</p>
        </div>
        {% endif %}

        <a href="/reportar" class="inline-block w-full bg-indigo-600 text-white font-bold py-3 rounded-xl text-xs shadow-md mt-4">Enviar otro reporte</a>
    </div>
</body>
</html>
"""

# Panel docente totalmente adaptado a pantallas verticales
HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel Docente</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-100 p-3 sm:p-6">
<div class="max-w-4xl mx-auto space-y-4">
    <div class="bg-white p-5 rounded-3xl shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border border-slate-100">
        <div>
            <h1 class="text-xl font-extrabold text-slate-800">Panel Institucional</h1>
            <p class="text-xs text-slate-500">{{ escuela }} - Monitoreo de convivencia</p>
        </div>
        <a href="/" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl text-xs font-bold shadow transition-all">Pantalla Principal</a>
    </div>
    
    <div class="space-y-4">
        {% for r in reportes %}
        <div class="bg-white p-5 sm:p-6 rounded-3xl shadow-sm border-l-8 border border-slate-100
            {% if r.analisis.nivel_riesgo == 'Rojo' %}border-red-500 bg-red-50/20
            {% elif r.analisis.nivel_riesgo == 'Amarillo' %}border-yellow-400 bg-yellow-50/20
            {% else %}border-emerald-500 bg-emerald-50/20{% endif %}">
            
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-2">
                <div class="flex flex-wrap items-center gap-2">
                    <span class="font-bold text-xs uppercase px-2.5 py-1 rounded-full text-white shadow-sm
                        {% if r.analisis.nivel_riesgo == 'Rojo' %}bg-red-500
                        {% elif r.analisis.nivel_riesgo == 'Amarillo' %}bg-yellow-500 text-slate-900
                        {% else %}bg-emerald-500{% endif %}">
                        Riesgo: {{ r.analisis.nivel_riesgo }}
                    </span>
                    <span class="text-xs text-slate-500">Reporte #{{ r.id }}</span>
                </div>
                
                <a href="/resolver/{{ r.id }}" onclick="return confirm('¿Confirma que el caso está resuelto y desea eliminarlo?');" class="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1.5 rounded-xl text-xs font-bold transition-all shadow flex items-center gap-1">
                    ✓ Marcar Resuelto
                </a>
            </div>

            <div class="space-y-3">
                <div class="bg-indigo-50/40 p-3 rounded-2xl border border-indigo-100/60">
                    <span class="text-xs font-bold text-indigo-900 block mb-0.5">👤 Estudiante:</span>
                    <span class="text-xs font-semibold text-slate-800">{{ r.nombre }} {{ r.apellido }} — <span class="text-indigo-600 font-bold">Curso: {{ r.curso }}</span></span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                    <div class="bg-slate-50 p-3 rounded-2xl border border-slate-100 space-y-1.5">
                        <strong class="block text-slate-700">Relato:</strong> 
                        <p class="text-slate-600 italic">"{{ r.texto_original }}"</p>
                        <p class="text-slate-400 pt-1"><strong>Lugar:</strong> {{ r.lugar }} | <strong>Frecuencia:</strong> {{ r.frecuencia }}</p>
                        <p class="text-slate-400"><strong>Emociones:</strong> {{ r.emociones | join(', ') }}</p>
                    </div>
                    
                    <div class="bg-indigo-50/60 p-3 rounded-2xl border border-indigo-100/50 space-y-2">
                        <div>
                            <strong class="block text-indigo-900 mb-0.5">Resumen IA:</strong> 
                            <p class="text-slate-700">{{ r.analisis.resumen_caso }}</p>
                        </div>
                        <div>
                            <strong class="block text-indigo-900 mb-0.5">🚨 Acciones y Concientización:</strong>
                            <p class="text-indigo-950 font-medium leading-relaxed">{{ r.analisis.recomendacion_docente }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% else %}
        <div class="bg-white p-10 text-center rounded-3xl text-slate-400 shadow-sm border border-slate-100">
            <p class="text-sm font-medium">¡Excelente! No hay reportes pendientes.</p>
        </div>
        {% endfor %}
    </div>
</div>
</body>
</html>
"""

# ==========================================
# 4. RUTAS DE NAVEGACIÓN
# ==========================================
@app.route('/')
def index():
    return render_template_string(HTML_INDEX, escuela=ESCUELA_NOMBRE)

@app.route('/reportar', methods=['GET', 'POST'])
def reportar():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        curso = request.form.get('curso', '').strip()
        
        texto = request.form.get('texto', '')
        emociones = request.form.getlist('emociones')
        frecuencia = request.form.get('frecuencia', 'Ocasional')
        lugar = request.form.get('lugar', 'No indicado')
        
        analisis = analizar_reporte_con_ia(texto, emociones, frecuencia, lugar)
        
        REPORTES_DB.insert(0, {
            "id": len(REPORTES_DB) + 1,
            "nombre": nombre,
            "apellido": apellido,
            "curso": curso,
            "texto_original": texto,
            "emociones": emociones,
            "frecuencia": frecuencia,
            "lugar": lugar,
            "analisis": analisis
        })
            
        return render_template_string(HTML_EXITO, escuela=ESCUELA_NOMBRE, ultimo_consejo=analisis.get("consejo_estudiante"))
        
    return render_template_string(HTML_REPORTE, escuela=ESCUELA_NOMBRE)

@app.route('/panel/institucional')
def dashboard():
    return render_template_string(HTML_DASHBOARD, escuela=ESCUELA_NOMBRE, reportes=REPORTES_DB)

@app.route('/resolver/<int:reporte_id>')
def resolver_reporte(reporte_id):
    global REPORTES_DB
    REPORTES_DB = [r for r in REPORTES_DB if r["id"] != reporte_id]
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    print("🚀 Servidor 'Voz Segura' iniciado correctamente.")
    app.run(debug=True, port=5000)