from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
import json

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MODELO DE DATOS
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


# CLASE PRINCIPAL
class RecomendadorCursos:

    def __init__(self):
        # ✅ FIX: el cliente se crea AQUÍ dentro, no afuera con self
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.cursos_mostrados = []

        self.prompt_sistema = """
        Eres un asistente especializado en recomendar cursos personalizados.

        IMPORTANTE:

        Devuelve TODA la respuesta ÚNICAMENTE en formato JSON válido.

        NO escribas texto fuera del JSON.

        La respuesta debe ser un array con exactamente 10 cursos.

        Cada curso debe tener EXACTAMENTE estas propiedades:

        - nombre
        - plataforma
        - link
        - precio
        - nivel
        - descripcion
        - aprendizaje
        - motivo
        - thumbnail
        - video

        REGLAS IMPORTANTES:

        - thumbnail debe ser una URL REAL de imagen.
        - video debe ser un link REAL de YouTube.
        - Usa miniaturas llamativas.
        - Prioriza cursos con videos de YouTube.
        - NO inventes links falsos.
        - TODOS los cursos deben tener thumbnail y video.

        RESPONDE SOLO JSON.
        """

    def generarRecomendaciones(self, informacionUsuario):

        # ✅ FIX: prompt_completo solo lleva la info del usuario, no el system prompt de nuevo
        prompt_completo = f"""
        INFORMACIÓN DEL USUARIO:
        {informacionUsuario}

        Cursos ya recomendados anteriormente:
        {self.cursos_mostrados}
        """

        respuesta = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": self.prompt_sistema
                },
                {
                    "role": "user",
                    "content": prompt_completo
                }
            ],
            temperature=0.4
        )

        texto = respuesta.choices[0].message.content

        self.cursos_mostrados.append(texto)

        try:
            recomendaciones_json = json.loads(texto)
            return {"respuesta": recomendaciones_json}

        except Exception as e:
            print("ERROR JSON:", e)
            print(texto)
            return {
                "respuesta": [
                    {
                        "nombre": "Error generando cursos",
                        "plataforma": "Sistema",
                        "link": "#",
                        "precio": "Gratis",
                        "nivel": "Todos",
                        "descripcion": texto,
                        "aprendizaje": "Error procesando respuesta",
                        "motivo": "La IA devolvió un formato inválido",
                        "thumbnail": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3",
                        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                    }
                ]
            }


# INSTANCIA
recomendador = RecomendadorCursos()


# RUTA PRINCIPAL
@app.get("/")
def inicio():
    return {"mensaje": "API funcionando 😎"}


# ENDPOINT PRINCIPAL
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

    recomendaciones = recomendador.generarRecomendaciones(informacionUsuario)

    return recomendaciones