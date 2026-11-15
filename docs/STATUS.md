# Estado técnico · G04 · 2026-11-15

**Release:** DS04/EXP03, Cerro Rojo, con fuentes y malla propias.

El M01B propio contiene 5,332 compósitos y 41,412 bloques; conserva clases topográficas, asignación geológica preliminar y atributos sin soporte. S11 y S12 tienen generaciones propias con validación técnica `VALIDATED`, manifiestos SHA, informes y visores interactivos. `python -m src.missions.g04 verificar` comprueba las generaciones vigentes. La suite automatizada aprobó 103 pruebas; la simulación de estudiante completó 30 actividades y 47 observaciones, comprobó tres bases SQLite y el ZIP individual; Chrome verificó navegación, filtros, selección de bloque, escenarios y ausencia de errores JavaScript. El entregable grupal incluye las fuentes, modelos y software de esta distribución.

**Límites:** CRS/datum no certificados; la asignación litológica a 20 m es preliminar y no demuestra continuidad. Los tonelajes con densidad y con ley Cu respaldado son universos distintos. S12 clasifica candidatos académicos y compara A/B; no declara reservas profesionales, pit ni secuencia minera física. La conversación real con Kai en Copilot/PyCharm y su aceptación pedagógica humana siguen pendientes.

`DISTRIBUCION_INICIAL_MANIFEST.json` documenta exclusivamente el commit inicial conceptual; `DISTRIBUCION_FINAL_MANIFEST.json` documenta el contenido IMP-008 actual.
