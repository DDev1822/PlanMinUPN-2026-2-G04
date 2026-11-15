# Kai Planeamiento · G04 · Cerro Rojo

![DrillStone](../assets/L1.png)

**Release:** DS04/EXP03, datos sintéticos. **Malla:** 20 × 20 × 10 m; 41,412 celdas. **Sondajes:** 35. **Compósitos:** 5332.

El recorrido tiene 30 actividades: 8 de E1, 16 de S11 y 6 de S12. Kai explica, pregunta una decisión y su razón, espera la respuesta, contrasta la evidencia y solo entonces avanza. El tutor valora el contenido de la respuesta; el registro controla orden y persistencia, no aprueba semánticamente.

## Datos y modelos propios

- E1: `data/raw/`, `data/processed/`, la ficha de 21 observaciones y el visor M01B.
- M01B: Malla 20 × 20 × 10 m; S11 usa la asignación preliminar conservadora con radio de 20 m.
- S11: IDW² de Cu/Mo/Au y densidad bajo las reglas PT-01, con vecinos, radios, litología preliminar y faltantes explícitos. El modelo de bloques completo y el manifiesto se encuentran bajo `outputs/g04_s11/`.
- S12: clasificación académica y escenarios A/B vinculados a la generación S11 del mismo grupo. No hay pit, secuencia física ni reservas profesionales. Productos bajo `outputs/g04_s12/`.
- Aplicación: 13 observaciones S11 y 13 S12, conciliadas con los productos verificados. Los estados y respuestas viven en `.kai_local/` y están excluidos de Git.

## Operación

El controlador `kai/recorrido_g04.py` procesa solicitudes JSON en `.kai_solicitud_recorrido_g04.json` con el comando constante `py -3 kai/recorrido_g04.py procesar-pendiente`. Consulta `estado` para obtener la actividad o campo pendiente. La ficha E1 usa `estado_ficha_e1` / `responder_ficha_e1`; la aplicación usa `estado_aplicacion` / `responder_aplicacion`; `entregar_individual` exige comprensión, 47 observaciones y productos grupales vigentes.

La secuencia pedagógica es **comprender → predecir → ejecutar → interpretar → validar → avanzar**. Los ejemplos teóricos de métodos no sustituyen la lectura de los modelos propios. Las respuestas reales y la aceptación conversacional mediante Copilot/PyCharm requieren comprobación humana separada.

## Límites

La topografía y los collars coinciden en las coordenadas locales del release, pero no existe certificación formal de CRS/datum. La asignación litológica es preliminar; cercanía no demuestra continuidad. Los resultados son académicos, con datos sintéticos. Los tonelajes con densidad y los tonelajes con Cu respaldado son poblaciones distintas. Los campos ausentes siguen ausentes.

![DrillStone · símbolo](../assets/L3.png)
