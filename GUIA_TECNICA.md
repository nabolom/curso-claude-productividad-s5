# Guía técnica · De Google Colab a una traza propia en LangSmith

**Claude para Productividad · Nivel 2 · S5**

La ruta oficial requiere una sola acción técnica: **pegar una API key personal de LangSmith en un campo oculto**. El notebook hace todo lo demás.

## 1. Qué ejecuta qué

| Pieza | Dónde vive | Qué hace |
|---|---|---|
| Notebook | Google Colab | Instala el entorno y dispara la ejecución. |
| Código | `demo_hill_climbing.py` | Define el estado, la rúbrica, los nodos y las condiciones de paro. |
| LangGraph | Dentro del proceso de Python | Ejecuta el ciclo y conserva el estado entre nodos. |
| LangSmith | En la nube | Recibe la traza y permite inspeccionarla. |
| Claude | En la nube | Generó los borradores de referencia; en el modo avanzado produce borradores nuevos. |

**LangSmith no ejecuta este repositorio por sí solo.** Su función principal en la ruta oficial es la observabilidad. LangSmith Studio puede conectarse a un agente desplegado o a un servidor local, pero exige una configuración técnica adicional.[2]

## 2. Ruta oficial para alumnos

### Paso 1 · Crear una llave personal

1. Abre [LangSmith Settings](https://smith.langchain.com/settings).
2. Entra a **API Keys**.
3. Selecciona **Create API Key** y elige una llave personal.
4. Cópiala. LangSmith solo muestra su valor una vez.[1]

### Paso 2 · Abrir el notebook

[![Abrir en Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nabolom/curso-claude-productividad-s5/blob/main/EJECUTA_S5_EN_LANGSMITH.ipynb)

### Paso 3 · Ejecutar

1. Abre **Entorno de ejecución → Ejecutar todas**.
2. Pega tu llave cuando aparezca el campo oculto.
3. Abre el enlace que aparece debajo de **TU TRAZA ESTÁ LISTA**.

El notebook crea o reutiliza el proyecto `S5-HillClimbing-Mi-Traza`. LangSmith agrupa las trazas por proyecto mediante `LANGSMITH_PROJECT`.[3] [4]

## 3. Qué sucede dentro del notebook

El flujo es automático:

1. Instala versiones compatibles de LangGraph, LangChain y LangSmith.
2. Descarga este repositorio.
3. Verifica que la llave sea aceptada por LangSmith.
4. Ejecuta el grafo con cinco borradores ficticios guardados.
5. Recalcula la rúbrica para cada borrador.
6. Envía la jerarquía de nodos a LangSmith.
7. Consulta la corrida recién creada.
8. Imprime el enlace directo a esa traza.
9. Retira la llave de la variable temporal del notebook.

La llave no se imprime ni se guarda en el archivo `.ipynb`. Aun así, debe tratarse como una contraseña.

## 4. Qué es nuevo y qué se reproduce

En la ruta oficial, **la ejecución de LangGraph y la traza de LangSmith son nuevas**. Los cinco textos provienen de una corrida previa de Claude. Esto elimina una segunda llave, evita costo de modelo y garantiza que todo el grupo vea la secuencia 5 → 50 → 62 → 62 → 70.

La palabra `replay` describe exactamente ese comportamiento: reproduce las salidas guardadas, pero vuelve a ejecutar los nodos, las decisiones y la evaluación.

## 5. Cómo leer la traza

En el enlace generado, busca la corrida `S5 Hill Climbing Reactivacion`.

1. Abre el nodo raíz y reconoce cinco bloques repetidos.
2. Abre `redactar` para ver el borrador usado en esa ronda.
3. Abre `medir` para localizar la métrica y los rasgos detectados.
4. Abre `evaluar` para comparar el intento con el mejor histórico.
5. Identifica el regreso de `ruta_decision` hacia `redactar`.

LangGraph modela esta lógica mediante estado, nodos y rutas condicionales.[5]

## 6. Si algo falla

| Síntoma | Causa probable | Solución exacta |
|---|---|---|
| `No se pudieron preparar las librerías` | Colab no pudo descargar un paquete o encontró un bloqueo temporal de red | Lee el detalle que aparece al final, comprueba internet y repite **PASO 1**. La instalación es aislada y no modifica las librerías base de Colab. |
| `No se pudo descargar el ejercicio` | Conexión temporal con GitHub | Comprueba internet y repite **PASO 1**. El mensaje ahora muestra el detalle real del error. |
| `LangSmith no aceptó la llave` | Llave incompleta, vencida o con espacios | Crea una llave personal nueva y ejecuta otra vez la celda **PASO 2**. |
| No aparece el campo para pegar | Colab no llegó a la segunda celda | Ejecuta manualmente la celda **PASO 2** con el botón triangular. |
| La corrida terminó, pero no aparece el enlace | La ingestión tardó más de 16 segundos | Espera 10 segundos y repite **PASO 2** y después **PASO 3**. |
| Colab pide permiso para ejecutar | Es la protección normal de un notebook externo | Confirma solo si la URL corresponde a este repositorio. |
| La llave pertenece a varios workspaces | LangSmith requiere identificar el workspace | Usa una llave personal de un solo workspace o configura `LANGSMITH_WORKSPACE_ID` con apoyo del facilitador.[1] |

## 7. Extensión avanzada · Generar textos nuevos con Claude

Esta ruta no es necesaria para completar la actividad. Requiere una segunda llave y produce resultados variables.

En una computadora con Python 3.11 o posterior:

```bash
git clone https://github.com/nabolom/curso-claude-productividad-s5.git
cd curso-claude-productividad-s5
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

En `.env`, agrega tu propia llave de OpenRouter y conserva las variables de LangSmith:

```dotenv
OPENROUTER_API_KEY=reemplaza_con_tu_clave
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=reemplaza_con_tu_clave
LANGSMITH_PROJECT=S5-HillClimbing-Reactivacion-Live
```

Ejecuta:

```bash
python demo_hill_climbing.py --mode live
```

OpenRouter expone un endpoint compatible con clientes OpenAI y permite seleccionar el modelo mediante su identificador.[6] Los resultados pueden variar porque Claude genera un texto nuevo en cada ronda.

## 8. Condiciones de paro

El grafo termina cuando ocurre cualquiera de estas condiciones:

- alcanza el máximo de iteraciones;
- llega a 95 puntos;
- acumula tres intentos consecutivos sin mejora.

Estos límites evitan un ciclo infinito y gasto sin control en el modo en vivo.

## Referencias

[1]: https://docs.langchain.com/langsmith/create-account-api-key "Create an account and API key · LangSmith Docs"
[2]: https://docs.langchain.com/langsmith/quick-start-studio "Get started with LangSmith Studio"
[3]: https://docs.langchain.com/langsmith/observability-quickstart "LangSmith observability quickstart"
[4]: https://docs.langchain.com/langsmith/log-traces-to-project "Log traces to a specific LangSmith project"
[5]: https://docs.langchain.com/oss/python/langgraph/quickstart "LangGraph Python quickstart"
[6]: https://openrouter.ai/docs/quickstart "OpenRouter quickstart"
