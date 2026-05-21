"use client"

import { useState } from "react"

export default function Home() {

  const [form, setForm] = useState({
    area: "",
    objetivo: "",
    nivel: "",
    tecnologias: "",
    idioma: "",
    presupuesto: "",
    tiempo: "",
    aprendizaje: "",
    proyecto: "",
    meta: "",
  })

  const [respuesta, setRespuesta] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  async function enviar() {

    setLoading(true)

    const res = await fetch(
      "http://127.0.0.1:8000/recomendar",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
      }
    )

    const data = await res.json()

    setRespuesta(data.respuesta)

    setLoading(false)
  }

  return (
    <main className="min-h-screen bg-black text-white">

      <div className="max-w-7xl mx-auto p-10">

        <div className="mb-14">

          <h1 className="text-7xl font-black mb-4 bg-gradient-to-r from-white to-zinc-500 bg-clip-text text-transparent">
            Recomendador IA
          </h1>

          <p className="text-zinc-400 text-xl">
            Cursos personalizados con inteligencia artificial
          </p>

        </div>

        <div className="grid md:grid-cols-2 gap-4 mb-10">

          <input
            placeholder="Área"
            className="bg-zinc-900 p-4 rounded-2xl"
            onChange={(e) =>
              setForm({
                ...form,
                area: e.target.value
              })
            }
          />

          <input
            placeholder="Objetivo"
            className="bg-zinc-900 p-4 rounded-2xl"
            onChange={(e) =>
              setForm({
                ...form,
                objetivo: e.target.value
              })
            }
          />

          <input
            placeholder="Nivel"
            className="bg-zinc-900 p-4 rounded-2xl"
            onChange={(e) =>
              setForm({
                ...form,
                nivel: e.target.value
              })
            }
          />

          <input
            placeholder="Tecnologías"
            className="bg-zinc-900 p-4 rounded-2xl"
            onChange={(e) =>
              setForm({
                ...form,
                tecnologias: e.target.value
              })
            }
          />

          <input
            placeholder="Idioma"
            className="bg-zinc-900 p-4 rounded-2xl"
            onChange={(e) =>
              setForm({
                ...form,
                idioma: e.target.value
              })
            }
          />

          <input
            placeholder="Presupuesto"
            className="bg-zinc-900 p-4 rounded-2xl"
            onChange={(e) =>
              setForm({
                ...form,
                presupuesto: e.target.value
              })
            }
          />

        </div>

        <button
          onClick={enviar}
          className="bg-white text-black px-10 py-5 rounded-2xl font-bold text-xl hover:scale-105 transition-all"
        >
          {
            loading
            ? "Generando..."
            : "Generar recomendaciones"
          }
        </button>

        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-8 mt-16">

          {
            respuesta.map((curso, index) => (

              <div
                key={index}
                className="bg-zinc-900 rounded-3xl overflow-hidden border border-zinc-800 hover:border-zinc-600 transition-all hover:scale-[1.02]"
              >

                <img
                  src={curso.thumbnail}
                  className="w-full h-52 object-cover"
                />

                <div className="p-6">

                  <h2 className="text-2xl font-bold mb-2">
                    {curso.nombre}
                  </h2>

                  <p className="text-zinc-400 mb-4">
                    {curso.descripcion}
                  </p>

                  <div className="flex gap-2 mb-4 flex-wrap">

                    <span className="bg-zinc-800 px-3 py-1 rounded-full text-sm">
                      {curso.nivel}
                    </span>

                    <span className="bg-zinc-800 px-3 py-1 rounded-full text-sm">
                      {curso.plataforma}
                    </span>

                    <span className="bg-zinc-800 px-3 py-1 rounded-full text-sm">
                      {curso.precio}
                    </span>

                  </div>

                  <p className="text-sm text-zinc-500 mb-6">
                    {curso.motivo}
                  </p>

                  <a
                    href={curso.link}
                    target="_blank"
                    className="block bg-white text-black text-center py-3 rounded-2xl font-bold"
                  >
                    Ver curso
                  </a>

                </div>

              </div>

            ))
          }

        </div>

      </div>

    </main>
  )
}