# x-daily-image-agent

Caso práctico inicial: agente que produce una imagen candidata por día para X.

Este repositorio no intenta resolver todavía el framework general del `silent-learner-core`. Es una implementación concreta para probar el ciclo mínimo:

```text
objetivo fijo
+ memoria validada
+ generación/selección de imagen
+ validación
+ registro
+ learner interno mínimo
```

## Idea central

El agente no inventa objetivos nuevos. Ejecuta siempre el objetivo de `prompt_fixed.md`.

La memoria no reemplaza al objetivo. Solo guarda experiencia validada o pendiente de revisión.

## Estado del MVP

Modo borrador:

1. busca una imagen en `assets/input/`;
2. si no encuentra, genera un placeholder local;
3. valida formato, tamaño, dimensiones y duplicado básico;
4. copia la imagen final a `assets/published/`;
5. registra la ejecución en `logs/run_log.json`;
6. genera una observación del learner en `logs/learner_suggestions.json`.

No publica automáticamente.

## Estructura

```text
x-daily-image-agent/
├── README.md
├── prompt_fixed.md
├── memory.json
├── config.example.json
├── requirements.txt
├── .gitignore
├── src/
│   ├── generate_image.py
│   ├── validate_image.py
│   ├── learner.py
│   └── run_daily.py
├── assets/
│   ├── input/.gitkeep
│   └── published/.gitkeep
├── logs/.gitkeep
└── .github/workflows/daily-draft.yml
```

## Uso local

```bash
python -m venv .venv
pip install -r requirements.txt
cp config.example.json config.json
python src/run_daily.py
```

## Primer criterio de éxito

Que el sistema pueda ejecutarse todos los días y dejar un resultado revisable sin intervención manual en cada paso.
