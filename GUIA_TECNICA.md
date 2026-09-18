# Guía técnica · Ejecutar y observar el ejercicio

**Claude para Productividad · Nivel 2 · S5**

Esta guía responde cuatro preguntas: **dónde vive el agente, cómo se ejecuta, cómo produce otra iteración y dónde se observa**.

## 1. La big picture

El sistema vive en tres lugares distintos.

| Pieza | Dónde vive | Qué hace |
|---|---|---|
| Código | `demo_hill_climbing.py`, en tu computadora | Define el estado, los nodos, la rúbrica y las condiciones de paro. |
| Claude | En la nube, accesible mediante OpenRouter | Redacta una nueva versión en el modo en vivo. |
| Trazas | En tu cuenta de LangSmith | Conserva la secuencia de pasos, entradas, salidas y tiempos. |

**LangChain** se materializa en `ChatOpenAI(...)` y en `llm.invoke(...)`. **LangGraph** se materializa en `construir_grafo()`, donde se agregan los nodos, las conexiones y la ruta condicional. LangGraph documenta este patrón como un grafo con estado, nodos y rutas condicionales.[1]

## 2. Dos formas de ejecutar

| Modo | Qué produce | Credenciales | Uso recomendado |
|---|---|---|---|
| `replay` | Recorre con LangGraph los cinco borradores guardados y recalcula la métrica. | Ninguna | Clase, práctica y validación estable. |
| `live` | Pide a Claude un borrador nuevo en cada ronda. | OpenRouter; LangSmith es opcional | Walkthrough técnico y experimentación. |

El modo `replay` no finge una llamada nueva a Claude. Reproduce con transparencia una corrida pasada para que el grafo y la rúbrica puedan estudiarse sin costo ni riesgo de red.

## 3. Preparar el entorno

Necesitas **Python 3.11 o posterior**. Descarga o clona el repositorio y abre una terminal dentro de su carpeta.

### macOS o Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 4. Reproducir la corrida sin claves

Ejecuta:

```bash
python demo_hill_climbing.py
```

Debes obtener cinco rondas con esta progresión:

```text
5.0 → 50.0 → 62.0 → 62.0 → 70.0
```

La salida se guarda en `resultados/ultima-corrida.json`. Ese archivo está ignorado por Git para evitar subir experimentos locales por accidente.

Para comprobar automáticamente la rúbrica y el ciclo:

```bash
python -m unittest discover -s tests -v
```

## 5. Ejecutar una corrida nueva con Claude

OpenRouter ofrece un endpoint compatible con clientes OpenAI y permite seleccionar el modelo mediante su identificador.[4] La demo usa `anthropic/claude-haiku-4.5` por defecto.

Copia la plantilla:

```bash
cp .env.example .env
```

En Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Abre `.env` y reemplaza únicamente:

```dotenv
OPENROUTER_API_KEY=reemplaza_con_tu_clave
```

Después ejecuta:

```bash
python demo_hill_climbing.py --mode live
```

Los resultados variarán porque Claude genera texto nuevo. La rúbrica seguirá siendo determinista: un mismo mensaje siempre recibe el mismo puntaje.

## 6. Activar las trazas en tu propia cuenta de LangSmith

Crea una llave en LangSmith y completa estas variables en `.env`:

```dotenv
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=reemplaza_con_tu_clave
LANGSMITH_PROJECT=S5-HillClimbing-Reactivacion
```

LangSmith usa `LANGSMITH_PROJECT` para agrupar las trazas. Si el proyecto no existe, se crea cuando ingresa la primera traza.[2] [3]

Vuelve a ejecutar:

```bash
python demo_hill_climbing.py --mode live
```

Luego abre [LangSmith](https://smith.langchain.com), entra a **Tracing** y selecciona `S5-HillClimbing-Reactivacion`. Verás una corrida principal con nodos anidados. Abre `redactar` para inspeccionar el prompt y la respuesta. Abre `medir` y el output final para revisar el historial de puntajes.

> Nunca uses las llaves del facilitador. Cada persona debe trabajar con sus propias credenciales y conservar `.env` fuera de Git.

## 7. Cómo ocurre “otra iteración”

Hay dos conceptos diferentes:

**Otra iteración dentro de la misma corrida.** Después de `evaluar`, `ruta_decision` devuelve `seguir`. LangGraph regresa automáticamente al nodo `redactar`. El máximo predeterminado es cinco.

**Otra corrida completa.** Vuelve a ejecutar el comando. Esa ejecución comienza con estado vacío y, si el tracing está activo, crea una nueva traza en LangSmith.

Puedes cambiar el límite del modo en vivo:

```bash
python demo_hill_climbing.py --mode live --max-iterations 8
```

El sistema también se detiene si llega a 95 puntos o acumula tres intentos consecutivos sin mejora. Estos límites evitan ciclos infinitos y gasto sin control.

## 8. Cómo leer el código sin perderte

Sigue este orden dentro de `demo_hill_climbing.py`:

1. `HillState` define la memoria de trabajo que viaja entre nodos.
2. `evaluar_mensaje()` convierte un borrador en rasgos observables y un puntaje.
3. `proveedor_replay()` y `proveedor_live()` determinan de dónde sale cada nuevo borrador.
4. `construir_grafo()` conecta `redactar`, `medir` y `evaluar`.
5. `ruta_decision()` decide continuar o terminar.
6. `ejecutar_demo()` inicia el estado e invoca el grafo.

## 9. Límites del ejercicio

La métrica es una rúbrica didáctica, no una predicción estadística. El sistema no conoce aperturas, respuestas ni conversiones reales. Una aplicación productiva necesitaría datos válidos, control de sesgos, pruebas A/B, privacidad, aprobación humana y una función objetivo ligada al resultado de negocio.

## Referencias

[1]: https://docs.langchain.com/oss/python/langgraph/quickstart "LangGraph Python quickstart"
[2]: https://docs.langchain.com/langsmith/observability-quickstart "LangSmith observability quickstart"
[3]: https://docs.langchain.com/langsmith/log-traces-to-project "Log traces to a specific LangSmith project"
[4]: https://openrouter.ai/docs/quickstart "OpenRouter quickstart"
