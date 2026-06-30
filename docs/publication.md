# Publicación automática en X

Objetivo: cerrar el camino mínimo funcional.

```text
imagen validada
  -> upload media
  -> create post
  -> guardar respuesta
  -> registrar log
```

## Modo de ejecución

Por defecto el sistema corre en modo seguro:

```text
POST_MODE=draft
```

En ese modo no publica. Solo valida la imagen y registra qué habría hecho.

Para publicar realmente:

```text
POST_MODE=live
X_BEARER_TOKEN=...
```

## Endpoints usados

El publicador está encapsulado en `src/post_to_x.py`.

Usa dos pasos:

1. `POST https://api.x.com/2/media/upload`
2. `POST https://api.x.com/2/tweets`

## Contrato interno

El resto del agente no conoce detalles de X.

Solo llama:

```python
publish_to_x(image_path, config)
```

El resultado queda en `publish_result` dentro de `logs/run_log.json`.

## Variables

```text
POST_MODE=draft | live
POST_TEXT=""
X_BEARER_TOKEN=...
```

## Criterio de éxito del Hello World

Una ejecución live es compatible si:

1. la imagen pasa validación;
2. X devuelve `media_id`;
3. X devuelve `post_id`;
4. el log guarda `post_url`.

## Nota

Este primer publicador usa el camino simple para imagen. Si X exige otro flujo para el tipo de cuenta, tamaño de archivo o autorización, se reemplaza solo `src/post_to_x.py`. El resto del agente queda igual.
