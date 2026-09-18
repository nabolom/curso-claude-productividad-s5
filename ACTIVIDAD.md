# Actividad · Diseña tu propia colina

**Duración:** 25 minutos

**Requisito:** no necesitas programar.

El propósito es transformar una tarea generativa en un loop que pueda **probar, medir, conservar el mejor intento y detenerse**. LangGraph permite modelar este comportamiento con estado, nodos y rutas condicionales.[1]

## 1. Elige una salida pequeña

Escoge un resultado que puedas revisar en menos de dos minutos. Algunos ejemplos son un asunto de correo, un resumen ejecutivo, una descripción de producto, una respuesta de soporte o la agenda de una reunión.

Escribe tu salida:

```text
Mi salida es:
```

## 2. Define la métrica antes de generar

Crea una rúbrica de cinco criterios observables. Evita criterios vagos como “suena bien”. Define evidencia que dos personas puedan reconocer de forma parecida.

| Criterio | Evidencia observable | Puntos |
|---|---|---:|
| 1. |  | /20 |
| 2. |  | /20 |
| 3. |  | /20 |
| 4. |  | /20 |
| 5. |  | /20 |
| **Total** |  | **/100** |

> Si un criterio no puede observarse en la salida, no sirve todavía como función de evaluación.

## 3. Define el ciclo

Completa estas reglas:

```text
GENERAR: El sistema crea ________________________________________________
MEDIR: La rúbrica revisa _________________________________________________
CONSERVAR: Un intento reemplaza al mejor cuando __________________________
REPETIR: El sistema intenta otra vuelta cuando ___________________________
DETENER: El sistema termina cuando ______________________________________
```

Incluye al menos dos condiciones de paro. Una debe limitar recursos, por ejemplo un máximo de cinco iteraciones. La otra debe reflejar calidad o estancamiento.

## 4. Analiza la corrida de referencia

Abre `resultados/corrida-referencia.json` y responde:

1. ¿Qué rasgo explica el salto de 5 a 50?
2. ¿Qué mejora permitió subir de 50 a 62?
3. ¿Por qué el intento de la ronda 4 no reemplazó al de la ronda 3?
4. ¿Qué cambió para llegar a 70?
5. ¿Qué limitación tiene usar esta puntuación como si fuera una tasa real de respuesta?

## 5. Añade guard rails

Escribe al menos tres límites. Usa este formato:

```text
NUNCA enviar, publicar o modificar un sistema externo sin aprobación humana.
NUNCA usar datos confidenciales para probar el loop.
DETENER si ______________________________________________________________
ESCALAR A UNA PERSONA si ________________________________________________
```

## 6. Criterio de terminado

Tu diseño está listo cuando otra persona puede responder sin preguntarte:

- qué genera el sistema;
- qué mide;
- qué resultado conserva;
- cuándo repite;
- cuándo se detiene;
- qué acción queda reservada para una persona.

## Entregable

Entrega una sola página con tu rúbrica y las cinco reglas del ciclo. No necesitas construir el código. La meta es demostrar que puedes diseñar una función objetivo y límites antes de automatizar.

## Referencias

[1]: https://docs.langchain.com/oss/python/langgraph/quickstart "LangGraph Python quickstart"
