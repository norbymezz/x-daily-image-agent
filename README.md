# x-daily-image-agent

Caso práctico inicial: agente que produce una imagen candidata por día para X.

Este repositorio no intenta resolver todavía el framework general del `silent-learner-core`. Es una implementación concreta para probar el ciclo mínimo:

```text
objetivo fijo
+ memoria validada
+ selección de imagen
+ validación
+ publicación opcional
+ registro
+ learner interno mínimo
```

## Idea central

El agente no inventa objetivos nuevos. Ejecuta siempre el objetivo de `prompt_fixed.md`.

La memoria no reemplaza al objetivo. Solo guarda experiencia validada o pendiente de revisión.

## Modo actual

Por defecto corre en modo borrador:

```text
POST_MODE=draft
```

Para prueba local real:

```bash
python -m venv .venv
pip install -r requirements.txt
cp config.example.json config.json
```

Crear un archivo `.env` local, no versionado:

```bash
POST_MODE=live
POST_TEXT=
X_API_KEY=...
X_API_SECRET=...
X_ACCESS_TOKEN=...
X_ACCESS_TOKEN_SECRET=...
```

Luego ejecutar:

```bash
python src/run_daily.py
```

## Flujo del MVP

1. busca una imagen en `src/assets/input/`;
2. si no encuentra, genera un placeholder local;
3. valida formato, tamaño, dimensiones y duplicado básico;
4. si `POST_MODE=draft`, registra simulación;
5. si `POST_MODE=live`, publica usando OAuth 1.0a;
6. registra la ejecución en `logs/run_log.json`;
7. genera una observación del learner en `logs/learner_suggestions.json`.

## Criterio de éxito del Hello World

El log debe contener:

```json
{
  "publish_result": {
    "ok": true,
    "post_id": "...",
    "post_url": "..."
  }
}
```

## Seguridad

No subir `.env`, `config.json`, tokens ni secrets. El repositorio ignora esos archivos.
