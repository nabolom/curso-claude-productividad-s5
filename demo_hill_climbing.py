#!/usr/bin/env python3
"""Demo didáctica de Hill Climbing con LangGraph.

El modo predeterminado, ``replay``, recorre con LangGraph los cinco borradores de
una corrida real ya registrada. No necesita credenciales y siempre produce la
curva 5 -> 50 -> 62 -> 62 -> 70.

El modo ``live`` usa Claude mediante OpenRouter. Si las variables de LangSmith
están configuradas, LangChain y LangGraph envían automáticamente las trazas a
la cuenta y proyecto indicados por el usuario.

La métrica es simulada y determinista. No representa una tasa real de respuesta
ni envía mensajes a clientes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Callable, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

ROOT = Path(__file__).resolve().parent
REFERENCE_RUN = ROOT / "resultados" / "corrida-referencia.json"
DEFAULT_OUTPUT = ROOT / "resultados" / "ultima-corrida.json"
DEFAULT_MODEL = "anthropic/claude-haiku-4.5"

ACCOUNT = {
    "empresa": "Grupo Meridian",
    "contacto": "Daniela",
    "dias_sin_contacto": 47,
    "contexto": "cliente ficticio de consultoría que dejó de responder hace mes y medio",
}

CLICHES = [
    "estimado cliente",
    "lamentamos profundamente",
    "esperamos que se encuentre bien",
    "no dude en contactarnos",
    "quedamos a sus órdenes",
    "reciba un cordial saludo",
]


class HillState(TypedDict):
    cuenta: dict
    iteracion: int
    max_iteraciones: int
    mensaje_actual: str
    metrica_actual: float
    mejor_mensaje: str
    mejor_metrica: float
    feedback_entorno: str
    historial: list[dict]
    sin_mejora_seguidas: int


DraftProvider = Callable[[HillState, int], str]


def evaluar_mensaje(mensaje: str, cuenta: dict) -> dict:
    """Calcula una métrica didáctica, determinista y transparente (0-100)."""
    texto = mensaje.lower()
    palabras = len(re.findall(r"\w+", mensaje))
    rasgos: dict[str, object] = {}
    score = 18.0

    usa_nombre = cuenta["contacto"].lower() in texto
    rasgos["usa_nombre_contacto"] = usa_nombre
    score += 12 if usa_nombre else 0

    if palabras <= 55:
        rasgos["brevedad"] = "excelente (<=55)"
        score += 16
    elif palabras <= 75:
        rasgos["brevedad"] = "buena (56-75)"
        score += 10
    elif palabras <= 95:
        rasgos["brevedad"] = "aceptable (76-95)"
        score += 4
    else:
        rasgos["brevedad"] = f"larga ({palabras} palabras)"
        score -= 4

    tiene_pregunta = "?" in mensaje
    rasgos["pregunta_directa"] = tiene_pregunta
    score += 9 if tiene_pregunta else 0

    palabras_valor = [
        "minuto",
        "café",
        "llamada",
        "propuesta",
        "idea",
        "caso",
        "resultado",
        "ayudar",
        "ahorrar",
        "reducir",
    ]
    tiene_valor = any(palabra in texto for palabra in palabras_valor)
    rasgos["propuesta_valor"] = tiene_valor
    score += 9 if tiene_valor else 0

    tiene_cifra = bool(
        re.search(r"\d+\s?%|\b\d+\s?(min|minutos|días|semanas|clientes)\b", texto)
    )
    rasgos["dato_concreto"] = tiene_cifra
    score += 10 if tiene_cifra else 0

    cta_suave = bool(re.search(r"(10|15|20)\s?min", texto)) or "un café" in texto
    rasgos["cta_baja_friccion"] = cta_suave
    score += 8 if cta_suave else 0

    numero_cliches = sum(1 for cliche in CLICHES if cliche in texto)
    rasgos["cliches_detectados"] = numero_cliches
    score -= 9 * numero_cliches

    return {
        "tasa_respuesta": round(max(0.0, min(100.0, score)), 1),
        "rasgos": rasgos,
        "palabras": palabras,
    }


def construir_feedback(resultado: dict) -> str:
    """Convierte el resultado del evaluador en instrucciones legibles."""
    rasgos = resultado["rasgos"]
    return "\n".join(
        [
            f"- Palabras: {resultado['palabras']} ({rasgos['brevedad']})",
            "- Usa el nombre del contacto: "
            + ("sí" if rasgos["usa_nombre_contacto"] else "NO (penaliza)"),
            "- Incluye una pregunta directa: "
            + ("sí" if rasgos["pregunta_directa"] else "NO (penaliza)"),
            "- Propuesta de valor concreta: "
            + ("sí" if rasgos["propuesta_valor"] else "NO (penaliza)"),
            "- Incluye un dato o cifra concreta: "
            + ("sí" if rasgos["dato_concreto"] else "NO (penaliza)"),
            "- CTA de baja fricción: "
            + ("sí" if rasgos["cta_baja_friccion"] else "NO (penaliza)"),
            f"- Clichés robóticos detectados: {rasgos['cliches_detectados']}",
        ]
    )


def proveedor_replay(path: Path = REFERENCE_RUN) -> DraftProvider:
    """Devuelve, en orden, los borradores guardados de la corrida de referencia."""
    with path.open(encoding="utf-8") as archivo:
        historial = json.load(archivo)["historial"]
    borradores = [registro["mensaje"] for registro in historial]

    def obtener_borrador(_: HillState, iteracion: int) -> str:
        try:
            return borradores[iteracion - 1]
        except IndexError as error:
            raise ValueError(
                f"La corrida de referencia solo contiene {len(borradores)} iteraciones."
            ) from error

    return obtener_borrador


def extraer_texto_respuesta(contenido: object) -> str:
    """Normaliza la respuesta de ChatOpenAI a texto simple."""
    if isinstance(contenido, str):
        return contenido.strip()
    if isinstance(contenido, list):
        partes = []
        for bloque in contenido:
            if isinstance(bloque, dict) and isinstance(bloque.get("text"), str):
                partes.append(bloque["text"])
        if partes:
            return "\n".join(partes).strip()
    raise RuntimeError("El modelo devolvió un formato de contenido no reconocido.")


def proveedor_live(modelo: str) -> DraftProvider:
    """Crea el proveedor de borradores que llama a Claude mediante OpenRouter."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key.startswith("reemplaza_"):
        raise RuntimeError(
            "Falta OPENROUTER_API_KEY. Copia .env.example a .env y agrega tu propia clave."
        )

    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model=modelo,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        timeout=60,
        max_retries=2,
    )

    def obtener_borrador(state: HillState, iteracion: int) -> str:
        cuenta = state["cuenta"]
        if iteracion == 1:
            sistema = "Redactas un primer borrador apresurado y genérico, sin pulir."
            prompt = (
                f"Escribe un primer borrador rápido de un correo de reactivación para "
                f"{cuenta['empresa']}. Escríbelo como alguien con prisa: formal, genérico, "
                "sin personalizar demasiado y puede ser largo. No lo optimices. "
                "Devuelve solo el texto del mensaje."
            )
        else:
            sistema = (
                "Optimizas copy de forma iterativa contra una métrica. Conserva lo que "
                "funciona y cambia un punto débil importante por ronda."
            )
            prompt = (
                f"Tu mejor mensaje para {cuenta['contacto']} de {cuenta['empresa']} obtuvo "
                f"{state['mejor_metrica']}/100.\n\n"
                f"MEJOR MENSAJE HASTA AHORA:\n{state['mejor_mensaje']}\n\n"
                f"DIAGNÓSTICO:\n{state['feedback_entorno']}\n\n"
                "Mejora ese mensaje para subir la métrica. Arregla un punto débil importante "
                "sin empeorar lo que ya funciona. Devuelve solo el texto del mensaje."
            )

        respuesta = llm.invoke(
            [SystemMessage(content=sistema), HumanMessage(content=prompt)]
        )
        return extraer_texto_respuesta(respuesta.content)

    return obtener_borrador


def construir_grafo(proveedor: DraftProvider):
    """Construye el ciclo redactar -> medir -> evaluar -> decidir."""

    def nodo_redactar(state: HillState) -> dict:
        iteracion = state["iteracion"] + 1
        return {
            "iteracion": iteracion,
            "mensaje_actual": proveedor(state, iteracion),
        }

    def nodo_medir(state: HillState) -> dict:
        resultado = evaluar_mensaje(state["mensaje_actual"], state["cuenta"])
        registro = {
            "iteracion": state["iteracion"],
            "metrica": resultado["tasa_respuesta"],
            "palabras": resultado["palabras"],
            "rasgos": resultado["rasgos"],
            "mensaje": state["mensaje_actual"],
        }
        return {
            "metrica_actual": resultado["tasa_respuesta"],
            "historial": [*state["historial"], registro],
        }

    def nodo_evaluar(state: HillState) -> dict:
        mejoro = state["metrica_actual"] > state["mejor_metrica"]
        mejor_mensaje = state["mensaje_actual"] if mejoro else state["mejor_mensaje"]
        mejor_metrica = state["metrica_actual"] if mejoro else state["mejor_metrica"]
        resultado_mejor = evaluar_mensaje(mejor_mensaje, state["cuenta"])
        return {
            "mejor_mensaje": mejor_mensaje,
            "mejor_metrica": mejor_metrica,
            "feedback_entorno": construir_feedback(resultado_mejor),
            "sin_mejora_seguidas": 0 if mejoro else state["sin_mejora_seguidas"] + 1,
        }

    def ruta_decision(state: HillState) -> Literal["seguir", "fin"]:
        if state["iteracion"] >= state["max_iteraciones"]:
            return "fin"
        if state["mejor_metrica"] >= 95:
            return "fin"
        if state["sin_mejora_seguidas"] >= 3:
            return "fin"
        return "seguir"

    grafo = StateGraph(HillState)
    grafo.add_node("redactar", nodo_redactar)
    grafo.add_node("medir", nodo_medir)
    grafo.add_node("evaluar", nodo_evaluar)
    grafo.set_entry_point("redactar")
    grafo.add_edge("redactar", "medir")
    grafo.add_edge("medir", "evaluar")
    grafo.add_conditional_edges(
        "evaluar", ruta_decision, {"seguir": "redactar", "fin": END}
    )
    return grafo.compile()


def ejecutar_demo(
    modo: Literal["replay", "live"] = "replay",
    max_iteraciones: int = 5,
    modelo: str = DEFAULT_MODEL,
) -> dict:
    """Ejecuta el grafo y devuelve un resultado serializable."""
    if not 1 <= max_iteraciones <= 20:
        raise ValueError("max_iteraciones debe estar entre 1 y 20.")
    if modo == "replay" and max_iteraciones > 5:
        raise ValueError("El modo replay contiene exactamente cinco borradores.")

    proveedor = proveedor_replay() if modo == "replay" else proveedor_live(modelo)
    app = construir_grafo(proveedor)
    estado_inicial: HillState = {
        "cuenta": ACCOUNT,
        "iteracion": 0,
        "max_iteraciones": max_iteraciones,
        "mensaje_actual": "",
        "metrica_actual": 0.0,
        "mejor_mensaje": "",
        "mejor_metrica": 0.0,
        "feedback_entorno": "",
        "historial": [],
        "sin_mejora_seguidas": 0,
    }
    final = app.invoke(
        estado_inicial,
        config={
            "recursion_limit": max_iteraciones * 4 + 5,
            "run_name": "S5 Hill Climbing Reactivacion",
        },
    )

    mejor_acumulado = 0.0
    curva = []
    for registro in final["historial"]:
        mejor_acumulado = max(mejor_acumulado, registro["metrica"])
        curva.append(
            {
                "iteracion": registro["iteracion"],
                "intento": registro["metrica"],
                "mejor_acumulado": mejor_acumulado,
            }
        )

    return {
        **final,
        "modo": modo,
        "modelo": modelo if modo == "live" else "corrida de referencia",
        "curva_mejor_acumulado": curva,
        "nota_metrica": "Métrica didáctica simulada; no es una tasa real de respuesta.",
    }


def imprimir_resumen(resultado: dict) -> None:
    print("=" * 72)
    print("HILL CLIMBING EN LANGGRAPH · DEMO DIDÁCTICA")
    print(f"Modo: {resultado['modo']}")
    print("La métrica es simulada y no se envía ningún mensaje real.")
    print("=" * 72)

    mejor_previo = 0.0
    for registro in resultado["historial"]:
        aceptado = registro["metrica"] > mejor_previo
        mejor_previo = max(mejor_previo, registro["metrica"])
        estado = "ACEPTADO" if aceptado else "DESCARTADO"
        print(
            f"Iteración {registro['iteracion']}: intento={registro['metrica']}/100 · "
            f"mejor={mejor_previo}/100 · {estado}"
        )

    print(f"\nMejor métrica: {resultado['mejor_metrica']}/100")
    print("\nMENSAJE GANADOR\n")
    print(resultado["mejor_mensaje"])


def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ejecuta la demo S5 de Hill Climbing en modo replay o live."
    )
    parser.add_argument(
        "--mode",
        choices=["replay", "live"],
        default="replay",
        help="replay no usa credenciales; live llama a Claude mediante OpenRouter.",
    )
    parser.add_argument("--max-iterations", type=int, default=5)
    parser.add_argument(
        "--model",
        default=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
        help="Modelo de OpenRouter usado solo en modo live.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Archivo JSON donde se guarda la corrida.",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Muestra el resultado sin escribir un archivo JSON.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parsear_argumentos()
    resultado = ejecutar_demo(args.mode, args.max_iterations, args.model)
    imprimir_resumen(resultado)

    if not args.no_save:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as archivo:
            json.dump(resultado, archivo, ensure_ascii=False, indent=2)
        print(f"\nResultado guardado en: {args.output}")


if __name__ == "__main__":
    main()
