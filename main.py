import os
from groq import Groq

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import json


app = FastAPI()


# CORS PARA FRONTEND
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

        self.client = Groq(
            api_key="TU_API_KEY_AQUI"
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

        EJEMPLO EXACTO:

        [
          {
            "nombre": "Python para Principiantes",
            "plataforma": "YouTube",
            "link": "https://www.youtube.com/watch?v=rfscVS0vtbw",
            "precio": "Gratis",
            "nivel": "Principiante",
            "descripcion": "Curso completo de Python desde cero.",
            "aprendizaje": "Variables, funciones y proyectos.",
            "motivo": "Perfecto para comenzar programación.",
            "thumbnail": "https://img.youtube.com/vi/rfscVS0vtbw/maxresdefault.jpg",
            "video": "https://www.youtube.com/watch?v=rfscVS0vtbw"
          }
        ]

        RESPONDE SOLO JSON.
        """

    def generarRecomendaciones(
        self,
        informacionUsuario
    ):

        prompt_completo = f"""
        {self.prompt_sistema}

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

            temperature=0.7
        )

        texto = (
            respuesta.choices[0]
            .message.content
        )

        self.cursos_mostrados.append(texto)

        return texto


# INSTANCIA
recomendador = RecomendadorCursos()


# RUTA PRINCIPAL
@app.get("/")
def inicio():

    return {
        "mensaje": "API funcionando 😎"
    }


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

    recomendaciones = (
        recomendador.generarRecomendaciones(
            informacionUsuario
        )
    )

    try:

        recomendaciones_json = json.loads(
            recomendaciones
        )

        return {
            "respuesta": recomendaciones_json
        }

    except Exception as e:

        print(e)

        return {
            "respuesta": []
        }