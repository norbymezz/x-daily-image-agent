# X Daily Image Agent

Agente local para preparar una imagen diaria candidata para publicar manualmente en X.

No publica automáticamente. El MVP genera o selecciona una imagen, valida condiciones mínimas y registra la ejecución.

## Uso

```bash
python -m venv .venv
pip install -r requirements.txt
cp config.example.json config.json
python src/run_daily.py
```

## Flujo

```text
prompt fijo + memoria -> imagen candidata -> validación -> salida revisable -> log -> learner suggestion
```
