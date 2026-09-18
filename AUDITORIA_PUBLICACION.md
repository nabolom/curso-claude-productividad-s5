# Auditoría de publicación · S5 Hill Climbing

**Fecha:** 17 de septiembre de 2026

**Resultado local:** **17 de 17 controles principales aprobados**

## Cambio evaluado

La ruta oficial para alumnos ya no requiere terminal, instalación local ni una llave de OpenRouter. El repositorio incorpora `EJECUTA_S5_EN_LANGSMITH.ipynb`, un notebook para Google Colab con tres acciones visibles: preparar el ejercicio, introducir una llave personal de LangSmith en un campo oculto y ejecutar el loop.

## Resultado de controles

| Área | Resultado | Evidencia |
|---|---|---|
| Estructura | Aprobado | Están presentes portada, notebook, actividad, guías, código, pruebas, imágenes y corrida de referencia. |
| Enlaces internos | Aprobado | No hay rutas locales rotas en los archivos Markdown. |
| Secretos | Aprobado | No se detectaron llaves de GitHub, LangSmith, OpenAI u OpenRouter con formato real. No existe `.env`. |
| Portabilidad | Aprobado | No hay rutas absolutas del entorno de construcción. |
| Corrida de referencia | Aprobado | Los puntajes se recalculan como 5, 50, 62, 62 y 70. |
| Selección del mejor | Aprobado | La cuarta ronda se descarta y la quinta conserva 70 como mejor puntaje. |
| Transparencia | Aprobado | La portada separa ejecución nueva, borradores reproducidos y métrica simulada. |
| Acción externa | Aprobado | La actividad no envía correos ni modifica sistemas externos. |
| Entrada principal | Aprobado | El README enlaza directamente al notebook en Google Colab. |
| Simplicidad | Aprobado | El notebook contiene siete celdas, de las cuales solo tres son ejecutables. |
| Credenciales | Aprobado | La llave entra por `getpass`, no se imprime, no se hardcodea y se retira de la variable temporal. |
| Traza | Aprobado | El notebook activa tracing, consulta la corrida recién creada y solicita su URL directa. |
| Código | Aprobado | El script principal y las celdas del notebook compilan. |
| Estilo | Aprobado | El código pasa Ruff y conserva formato estable. |
| Dependencias | Aprobado | Las versiones están fijadas y el entorno no reporta dependencias rotas. |
| Pruebas | Aprobado | Las ocho pruebas automatizadas pasan. |
| Modo avanzado | Aprobado | Una corrida de una iteración recibió respuesta real de Claude mediante OpenRouter. |

## Qué puede afirmarse

La corrida de referencia del repositorio ya produjo una traza real en LangSmith, visible en las capturas. La nueva ruta ejecuta LangGraph nuevamente y está instrumentada para crear una traza en la cuenta del alumno. Las firmas de `list_projects`, `runs.query` y `runs.get_url` fueron verificadas contra `langsmith==0.12.6`, y la documentación oficial confirma el uso de API keys, proyectos y trazas.[1] [2] [3]

## Límite de la validación

La prueba automática no introduce una credencial personal nueva de LangSmith, porque una API key no debe almacenarse en el repositorio ni en la suite de pruebas. Por ello, antes de impartir la clase el facilitador debe realizar una corrida de humo en Colab con una llave temporal propia y revocarla al terminar. Si una organización bloquea la creación de llaves, la guía incluye un Plan B con capturas y trabajo en parejas.

## Decisiones de seguridad

Cada participante usa su propia llave. El notebook no solicita la llave de OpenRouter en la ruta oficial. Los borradores son ficticios y están guardados de antemano. El sistema nunca envía el correo generado. La captura de LangSmith es evidencia estática y no comparte acceso a la cuenta del facilitador.

## Referencias

[1]: https://docs.langchain.com/langsmith/create-account-api-key "Create an account and API key · LangSmith Docs"
[2]: https://docs.langchain.com/langsmith/observability-quickstart "LangSmith observability quickstart"
[3]: https://docs.langchain.com/langsmith/log-traces-to-project "Log traces to a specific LangSmith project"
