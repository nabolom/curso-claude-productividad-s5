# Guía del facilitador · Ejercicio 100% guiado en LangSmith

**Claude para Productividad · Nivel 2 · S5**

Esta guía conduce una actividad de **12 minutos**. El alumno no elige archivos, comandos, modelos ni parámetros. Crea una llave personal, abre Colab, ejecuta todo y entra a su propia traza.

## Resultado de aprendizaje

Al terminar, cada participante debe poder señalar en LangSmith:

1. dónde comienza una corrida;
2. qué nodos se repiten;
3. dónde se conserva el mejor resultado;
4. por qué la ronda 4 se descarta;
5. por qué una mala métrica haría que el sistema optimizara algo incorrecto.

## Preparación del facilitador

Antes de la clase:

- abre el [repositorio](https://github.com/nabolom/curso-claude-productividad-s5);
- prueba el botón **Abrir en Google Colab**;
- deja abiertas las imágenes `assets/traza-langsmith.png` y `assets/curva-hill-climbing.png` como Plan B;
- pide a cada alumno iniciar sesión en [LangSmith](https://smith.langchain.com) antes del bloque;
- no compartas tu llave ni pidas que los alumnos peguen la suya en el chat.

## Minuto 0–2 · Enmarcar

Di exactamente:

> “No van a programar. Van a ejecutar un agente y luego van a entrar a su caja negra. Google Colab corre el sistema; LangSmith nos deja observar lo que hizo.”

Después:

> “Los textos ya están preparados para que todos obtengamos la misma evidencia. Lo que se ejecuta de nuevo es el grafo: cada nodo, cada medición, cada decisión y la traza que aparecerá en su cuenta.”

## Minuto 2–4 · Crear la llave

Proyecta estas instrucciones:

1. Abre `https://smith.langchain.com/settings`.
2. Entra a **API Keys**.
3. Selecciona **Create API Key**.
4. Elige una llave personal.
5. Copia la llave y no cierres todavía LangSmith.

Di:

> “La llave funciona como contraseña. No la pongan en Zoom, Slack o el chat. El notebook abre un campo oculto y la retira de memoria al terminar.”

LangSmith recomienda una Personal Access Token para scripts personales y solo muestra el valor una vez.[1]

## Minuto 4–7 · Ejecutar

Pide que vuelvan al README del repositorio y hagan clic en **Abrir en Google Colab**.

Di exactamente:

> “Arriba, abran `Entorno de ejecución` y elijan `Ejecutar todas`. No cambien ninguna celda.”

Cuando aparezca el campo:

> “Peguen su llave en `Pega tu API key de LangSmith` y presionen Enter. Aunque parezca vacío, sí se está capturando: el texto está oculto.”

Pide que levanten la mano cuando vean:

```text
✅ TU TRAZA ESTÁ LISTA
```

## Minuto 7–10 · Encontrar evidencia

Pide que abran el enlace generado. Dales esta misión:

> “Encuentren el patrón `redactar → medir → evaluar → decidir`. Cuenten cuántas veces aparece y localicen la secuencia 5, 50, 62, 62, 70.”

Haz estas preguntas en orden:

1. “¿Qué nodo produce o recupera un intento?”
2. “¿Qué nodo convierte el intento en un puntaje?”
3. “¿Qué ocurrió en la ronda 4?”
4. “¿Por qué el sistema conservó 62 en vez de reemplazarlo?”

La respuesta clave es:

> “Explorar no obliga a aceptar. La ronda 4 fue información útil porque confirmó que esa alternativa no superaba el mejor resultado.”

## Minuto 10–12 · Debrief

Muestra `assets/curva-hill-climbing.png` y cierra con:

> “Un prompt entrega una respuesta. Este loop mantiene estado, compara intentos y decide si vale la pena otra vuelta. La autonomía no está en escribir; está en decidir qué hacer después de escribir.”

Luego pregunta:

> “Si la métrica estuviera mal diseñada, ¿qué haría el agente?”

Respuesta esperada:

> “Optimizaría con mucha disciplina la cosa equivocada.”

## Lo que verán y lo que no verán

| Elemento | Estado |
|---|---|
| Grafo y nodos | Se ejecutan nuevamente en Colab. |
| Traza | Se crea en la cuenta de cada alumno. |
| Puntajes | Se recalculan en cada ejecución. |
| Borradores | Se reproducen desde una corrida previa de Claude. |
| Llamada nueva a Claude | No ocurre en la ruta oficial. |
| Envío de correo | Nunca ocurre. |

Esta elección evita pedir una llave de OpenRouter y elimina variabilidad durante la clase. La extensión avanzada conserva el modo `live` para quien quiera generar versiones nuevas después.

## Preguntas difíciles

| Pregunta | Respuesta recomendada |
|---|---|
| ¿Se ejecuta dentro de LangSmith? | No. Colab ejecuta LangGraph; LangSmith recibe y visualiza la traza. Studio puede conectarse a una app desplegada o local, pero requiere más configuración.[2] |
| ¿Entonces dónde vive el agente? | En `demo_hill_climbing.py`, ejecutándose temporalmente en Google Colab. |
| ¿Claude está respondiendo ahora? | No en la ruta oficial. Reproducimos cinco borradores reales ya guardados para que todos vean la misma curva. |
| ¿La traza sí es mía y nueva? | Sí. El grafo vuelve a correr y LangSmith registra esa ejecución en la cuenta del alumno. |
| ¿La métrica de 70 es real? | No. Es una rúbrica didáctica reproducible, no una predicción comercial. |
| ¿Cómo genero texto nuevo? | Con la extensión avanzada y una llave propia de OpenRouter. No es necesaria en clase. |
| ¿Por qué no usar LangSmith Studio? | Studio necesita una aplicación desplegada o un servidor local. Colab reduce pasos y cumple el objetivo de observar una traza propia.[2] |

## Troubleshooting en vivo

| Síntoma | Qué dices | Qué haces |
|---|---|---|
| La llave falla | “Crea una llave nueva y pégala sin espacios.” | Repite solo la celda **PASO 2**. |
| No sale el campo oculto | “La segunda celda todavía no corrió.” | Pulsa el triángulo de **PASO 2**. |
| No aparece el enlace | “La traza tarda unos segundos en indexarse.” | Espera 10 segundos y repite **PASO 2** y después **PASO 3**. |
| Alguien no puede crear cuenta | “Usa el recorrido visual; no te quedas fuera del aprendizaje.” | Muestra la captura y forma una pareja con alguien que sí tenga traza. |
| Falla Colab para todo el grupo | “La evidencia ya está capturada.” | Usa las tres imágenes del repositorio y conduce el mismo debrief. |

## Guard rails

- Nunca proyectes o pegues una API key.
- Nunca uses datos reales de clientes.
- Nunca pidas que una persona comparta acceso a su cuenta.
- Nunca presentes el puntaje simulado como una métrica observada.
- Nunca envíes el mensaje ganador; es un borrador didáctico.

## Referencias

[1]: https://docs.langchain.com/langsmith/create-account-api-key "Create an account and API key · LangSmith Docs"
[2]: https://docs.langchain.com/langsmith/quick-start-studio "Get started with LangSmith Studio"
