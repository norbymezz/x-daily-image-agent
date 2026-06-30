# Authentication notes

Este archivo no es documentación formal para terceros. Es una libreta técnica para recordar qué espera la API de X cuando probemos publicación real.

## Estado actual observado

Para el camino mínimo de publicación con imagen se usan dos endpoints:

```text
POST https://api.x.com/2/media/upload
POST https://api.x.com/2/tweets
```

Ambos endpoints usan header:

```text
Authorization: Bearer <token>
```

Pero el token relevante no debe entenderse como un bearer token genérico de app-only. La documentación de X indica `OAuth2UserToken`, es decir, un access token de usuario obtenido por OAuth 2.0.

## Implicación práctica

Para publicar en la cuenta del usuario, el token debe representar al usuario que publica. No alcanza con que exista una app; tiene que haber autorización de usuario con permisos de escritura.

## Variables que el proyecto espera por ahora

```text
POST_MODE=draft | live
POST_TEXT=""
X_BEARER_TOKEN=...
```

`X_BEARER_TOKEN` queda como nombre simple de variable, pero conceptualmente debería contener el access token OAuth 2.0 de usuario.

## Riesgo conocido

El archivo `src/post_to_x.py` implementa el camino simple:

```text
media/upload -> tweets
```

Si X exige refresh tokens, scopes concretos, OAuth 1.0a para cierta cuenta, o un flujo distinto por tipo de plan, no se cambia todo el agente. Se cambia solamente `src/post_to_x.py` y esta nota.

## Scopes/permisos a revisar antes de live

Pendiente de confirmación en Developer Portal:

```text
tweet.write
users.read
offline.access   # solo si usamos refresh token
media.write      # si el portal lo expone separado
```

## Regla de seguridad

Nunca subir tokens al repositorio. Usar GitHub Actions Secrets o variables locales.

## Criterio de compatibilidad mínima

Una prueba live es válida si el log guarda:

```json
{
  "publish_result": {
    "ok": true,
    "media_id": "...",
    "post_id": "...",
    "post_url": "..."
  }
}
```
