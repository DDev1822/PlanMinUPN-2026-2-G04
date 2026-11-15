# PlanMinUPN 2026-2 · G04 Cerro Rojo

Distribución académica privada de DD, release **DS04/EXP03** con datos sintéticos del grupo. Este repositorio conserva su commit inicial limpio y desarrolla IMP-008 sobre su propia malla y observaciones.

## Inicio

1. Clona el repositorio y abre su raíz en PyCharm con Python 3.12.
2. Instala `py -3 -m pip install -r requirements.txt` en un entorno virtual.
3. Ejecuta `py -3 -m pytest -q`.
4. Abre `index.html` para explorar E1, M01B, S11 y S12.
5. Selecciona **Kai Planeamiento** desde `.github/agents/kai-planeamiento.agent.md` en Copilot. El tutor usa el controlador `kai/recorrido_g04.py` y consulta primero su estado.

## Modelos y productos

- `data/raw/`: release original, inmutable. `data/processed/`: derivados M01/M01B propios.
- `py -3 -m src.missions.g04 verificar`: verifica SHA de fuentes, salidas y validaciones de las generaciones vigentes.
- `py -3 -m src.missions.g04 todo`: reproduce S11 y después S12 sin usar resultados de otro grupo.
- `outputs/g04_products.json`: puntero a las generaciones verificadas. Cada carpeta S11/S12 contiene CSV integral, visor 3D, reporte, resumen, validación y manifiesto.
- `docs/learning/GUIA_KAI_COMPARTIDA.md`: 30 actividades E1/S11/S12 y límites académicos. La ficha E1 recoge 21 observaciones, la aplicación S11/S12 otras 26.

Los visores usan datos locales; abre la carpeta completa para conservar sus recursos. Las cantidades S11 con densidad y con ley Cu respaldada corresponden a universos distintos. La clasificación S12 es una comparación académica, sin reserva profesional ni secuencia de extracción.

## Privacidad y límites

`.kai_local/` guarda SQLite, respuestas y entregables individuales por alias, y está excluido de Git. No publiques conversaciones ni credenciales. El controlador comprueba orden, integridad y valores de aplicación; la valoración semántica de respuestas corresponde al tutor humano/Copilot y no queda acreditada por una simulación automatizada.

La compatibilidad espacial usa las coordenadas locales del release; no hay certificación formal de CRS/datum. La litología preliminar no demuestra continuidad geológica. Consulta los manifiestos y validaciones antes de citar un resultado.
