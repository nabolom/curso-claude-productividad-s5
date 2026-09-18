# Guía del facilitador · Walkthrough de Hill Climbing

**Claude para Productividad · Nivel 2 · S5**

Esta guía permite conducir una demostración de 12–15 minutos para una audiencia básica/intermedia. El objetivo no es enseñar Python; es hacer visible la diferencia entre **generar una respuesta** y **operar un ciclo que mide, decide y mejora**.

## Preparación

Antes de la sesión, confirma que el repositorio abre correctamente y deja disponibles estas tres pantallas:

1. `assets/grafo-langgraph.png`
2. `assets/traza-langsmith.png`
3. `assets/curva-hill-climbing.png`

Si mostrarás LangSmith en vivo, entra a tu cuenta, abre **Tracing** y localiza el proyecto `S5-HillClimbing-Reactivacion`. Comprueba que la corrida carga. No muestres la sección de llaves ni archivos `.env`.

## Apertura · 90 segundos

Muestra el primer borrador dentro de `resultados/corrida-referencia.json` y di:

> “Un prompt normal termina cuando Claude responde. Este sistema hace algo distinto: toma la respuesta como un intento, la mide y decide si merece conservarla. Si todavía hay oportunidad de mejorar, vuelve a redactar.”

Aclara desde el inicio:

> “La métrica de esta demo es simulada y transparente. No estamos diciendo que 70 sea una tasa real de respuesta. Estamos aislando el mecanismo para poder observarlo.”

## El grafo · 3 minutos

Muestra `assets/grafo-langgraph.png`. LangGraph representa este tipo de ejecución mediante estado, nodos, conexiones y rutas condicionales.[3] Recorre los nodos en orden:

- **Redactar:** Claude produce una versión.
- **Medir:** una función determinista revisa rasgos observables.
- **Evaluar:** compara el intento con el mejor puntaje histórico.
- **Decidir:** termina o regresa a redactar.

La frase central es:

> “La autonomía no está en que Claude escriba. Está en que el sistema puede decidir si necesita otra vuelta sin que una persona vuelva a presionar un botón.”

No digas que el agente “aprendió solo”. La formulación precisa es:

> “El agente optimizó dentro de una corrida, usando una métrica y conservando el mejor resultado. No cambió los parámetros del modelo ni adquirió memoria permanente.”

## La traza en LangSmith · 4 minutos

Muestra `assets/traza-langsmith.png` o abre la corrida real. Señala el patrón repetido a la izquierda.

> “LangSmith es la capa de observabilidad. El agente no vive aquí; aquí vemos la evidencia de lo que ejecutó el código. Cada bloque `redactar → medir → evaluar → decidir` es una vuelta del loop.”

Al abrir un nodo `redactar`, señala la entrada y la salida:

> “En la entrada viajan la cuenta, el mejor mensaje hasta ahora y el diagnóstico. En la salida aparece el nuevo intento de Claude.”

Si preguntan por `ChatOpenAI`, responde:

> “Es el nombre del adaptador compatible con el protocolo de OpenAI. En esta corrida, el modelo detrás del adaptador es Claude Haiku servido mediante OpenRouter.”

LangSmith documenta que las trazas pueden capturar la jerarquía completa de una ejecución y agruparse por proyecto.[1] [2]

## La curva · 3 minutos

Muestra `assets/curva-hill-climbing.png` y recorre los valores:

> “El primer mensaje obtuvo 5. El segundo llegó a 50. Después subió a 62. La cuarta ronda también obtuvo 62: se probó una alternativa, pero no superó el récord, así que no reemplazó al mejor mensaje. La quinta llegó a 70.”

Haz la pregunta al grupo:

> “¿La meseta de 62 a 62 es un fallo?”

La respuesta esperada es no. El guard rail funcionó: explorar no implica aceptar una versión peor o igual.

## El aprendizaje clave · 90 segundos

Cierra con esta escalera:

| Nivel | Comportamiento |
|---|---|
| Prompt | Genera una respuesta. |
| Workflow | Ejecuta pasos predefinidos. |
| Verificación | Revisa si el resultado cumple reglas. |
| Hill Climbing | Genera, mide, conserva el mejor y vuelve a intentar hasta detenerse. |

> “La calidad del loop depende de la calidad de la métrica. Si medimos mal, el sistema optimiza la cosa equivocada con mucha disciplina.”

## Preguntas difíciles

| Pregunta | Respuesta recomendada |
|---|---|
| ¿Dónde vive el agente? | En `demo_hill_climbing.py`. Claude vive en la nube y LangSmith guarda las trazas. |
| ¿Cómo genero otra iteración? | Dentro de una corrida, el grafo vuelve solo a `redactar`. Para otra corrida completa, se ejecuta de nuevo el programa. |
| ¿Esto reemplaza al humano? | No. El humano diseña la métrica, define límites y revisa el borrador final antes de cualquier acción. |
| ¿La métrica de 70 es real? | No. Es una puntuación didáctica reproducible, no una predicción de respuesta. |
| ¿Por qué no mejoró la ronda 4? | El modelo exploró una redacción distinta, pero la rúbrica no encontró una mejora. El sistema conservó el récord anterior. |
| ¿Qué pasa si la métrica está mal? | El agente optimiza el objetivo equivocado. Diseñar y validar la métrica es la responsabilidad más importante. |
| ¿Cuánto cuesta? | Depende del modelo, número de iteraciones y longitud del contexto. Revisa el consumo de tu propia traza y la tarifa vigente; no prometas una cifra fija. |

## Plan B

Si falla internet, no intentes reparar credenciales frente al grupo. Usa las tres imágenes incluidas y `resultados/corrida-referencia.json`. El relato y la evidencia son los mismos; únicamente cambia que la interfaz está congelada.

## Checklist de seguridad

- [ ] No mostrar ni proyectar llaves de API.
- [ ] No usar datos reales de clientes.
- [ ] No compartir acceso a la cuenta personal de LangSmith.
- [ ] Recordar que el resultado es un borrador y no se envía.
- [ ] Revocar cualquier llave que haya sido expuesta accidentalmente.

## Referencias

[1]: https://docs.langchain.com/langsmith/observability-quickstart "LangSmith observability quickstart"
[2]: https://docs.langchain.com/langsmith/log-traces-to-project "Log traces to a specific LangSmith project"
[3]: https://docs.langchain.com/oss/python/langgraph/quickstart "LangGraph Python quickstart"
