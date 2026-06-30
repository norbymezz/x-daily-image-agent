# Prompt fijo

Objetivo fijo: producir exactamente una imagen candidata por día para publicación manual en X.

## Reglas invariantes

1. No inferir objetivos nuevos.
2. No publicar automáticamente.
3. Evitar repetición de imágenes.
4. Validar formato, resolución y peso.
5. Registrar cada ejecución.
6. Proponer aprendizaje separado de la ejecución.
7. La memoria puede orientar selección y descarte, pero no puede cambiar el objetivo.
8. Si no hay imagen de entrada, generar una imagen placeholder local para mantener el ciclo operativo.

## Salida esperada

- imagen final en `assets/published/`;
- log de ejecución en `logs/run_log.json`;
- sugerencia del learner en `logs/learner_suggestions.json`.
