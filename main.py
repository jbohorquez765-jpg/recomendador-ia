from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DatosUsuario(BaseModel):
    area: str
    objetivo: str
    nivel: str
    tecnologias: str
    idioma: str
    presupuesto: str
    tiempo: str
    aprendizaje: str
    proyecto: str
    meta: str

class RecomendadorCursos:

    def __init__(self):
        self.cursos_mostrados = []
        self.prompt_sistema = """
        Eres un asistente especializado en recomendar cursos personalizados.
        Devuelve TODA la respuesta ÚNICAMENTE en formato JSON válido.
        NO escribas texto fuera del JSON.
        La respuesta debe ser un array con exactamente 10 cursos.
        Cada curso debe tener EXACTAMENTE estas propiedades:
        nombre, plataforma, link, precio, nivel, descripcion, aprendizaje, motivo, thumbnail, video
        REGLAS: thumbnail URL REAL, video link REAL de YouTube. RESPONDE SOLO JSON.
        """

    def generarRecomendaciones(self, informacionUsuario):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY no está definida.")
        client = Groq(api_key=api_key)
        prompt_completo = f"""
        INFORMACIÓN DEL USUARIO:
        {informacionUsuario}
        Cursos ya recomendados anteriormente:
        {self.cursos_mostrados}
        """
        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.prompt_sistema},
                {"role": "user", "content": prompt_completo}
            ],
            temperature=0.4
        )
        texto = respuesta.choices[0].message.content
        texto = texto.strip()
        if texto.startswith("```"):
            texto = texto.split("```")[1]
            if texto.startswith("json"):
                texto = texto[4:]
        texto = texto.strip()
        self.cursos_mostrados.append(texto)
        try:
            return {"respuesta": json.loads(texto)}
        except Exception as e:
            print("ERROR JSON:", e)
            return {"respuesta": [{"nombre": "Error", "plataforma": "Sistema", "link": "#", "precio": "Gratis", "nivel": "Todos", "descripcion": texto, "aprendizaje": "Error", "motivo": "Formato inválido", "thumbnail": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3", "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}]}

recomendador = RecomendadorCursos()

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando 😎"}

@app.get("/debug-env")
def debug_env():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return {"estado": "❌ GROQ_API_KEY no encontrada"}
    return {
        "estado": "✅ GROQ_API_KEY encontrada",
        "longitud": len(key),
        "preview": f"{key[:6]}...{key[-4:]}",
        "empieza_con_gsk": key.startswith("gsk_"),
        "tiene_espacios": key != key.strip()
    }

@app.post("/recomendar")
def recomendar(datos: DatosUsuario):
    informacionUsuario = f"""
    Área de interés: {datos.area}
    Objetivo principal: {datos.objetivo}
    Nivel actual: {datos.nivel}
    Tecnologías favoritas: {datos.tecnologias}
    Idioma preferido: {datos.idioma}
    Presupuesto: {datos.presupuesto}
    Tiempo disponible: {datos.tiempo}
    Tipo de aprendizaje: {datos.aprendizaje}
    Proyecto deseado: {datos.proyecto}
    Meta final: {datos.meta}
    """
    return recomendador.generarRecomendaciones(informacionUsuario)


