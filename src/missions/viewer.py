"""HTML local enlazado a la tabla íntegra y a su generación verificada."""
import html
import json
import base64
import gzip
from src.mod1.loader import load_raw_data
from src.mod1.desurvey import desurvey


def render_view(root, folder, stage, run_id, blocks, summary, scenarios=None):
    raw=load_raw_data(root/'data/raw')
    tracks=desurvey(raw['collar'],raw['survey'])
    visible_fields={'block_id','x_min','x_max','y_min','y_max','z_min','z_max',
        'lith_code','lith_status','topo_status','volume_status','cell_volume_m3',
        'rock_volume_m3','rock_fraction','cu_pct_est','mo_pct_est','au_gt_est',
        'density_t_m3_est','tonnage_t','tonnage_reason','cu_pct_n','cu_pct_holes',
        'cu_pct_reason','cu_pct_sample_ids','cu_pct_distances_m','cu_pct_weights',
        'density_t_m3_n','density_t_m3_holes','density_t_m3_reason',
        'density_t_m3_sample_ids','density_t_m3_distances_m','cu_pct_est_r50',
        'cu_pct_reason_r50','candidate_class','candidate_reason','reserve_classification',
        'allocation_rule','scenario_A_fraction','scenario_B_fraction',
        'scenario_A_allocated_t','scenario_B_allocated_t',
        'scenario_A_processed_t','scenario_B_processed_t',
        'scenario_A_remaining_t','scenario_B_remaining_t',
        'scenario_A_mining_opex_usd','scenario_B_mining_opex_usd',
        'scenario_A_processing_opex_usd','scenario_B_processing_opex_usd',
        'scenario_A_general_opex_usd','scenario_B_general_opex_usd',
        'scenario_A_opex_usd','scenario_B_opex_usd',
        'scenario_A_truck_capex_share_usd','scenario_B_truck_capex_share_usd'}
    def compact(block):
        result={k:v for k,v in block.items() if k in visible_fields and v is not None
                and not (isinstance(v,(list,tuple)) and len(v)==0)}
        # El filtro del visor necesita distinguir la ausencia de Cu del valor cero.
        result['cu_pct_est']=block['cu_pct_est']
        return result
    payload=dict(stage=stage,run_id=run_id,blocks=[compact(b) for b in blocks],summary=summary,
                 max_display_blocks=6000,scenarios=scenarios or [],
                 trajectories=[dict(hole_id=h,**{k:[p[k] for p in rows] for k in 'xyz'}) for h,rows in tracks.items()])
    serialized=json.dumps(payload,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode('utf-8')
    data=base64.b64encode(gzip.compress(serialized,compresslevel=9,mtime=0)).decode('ascii')
    title=summary['product']
    s=stage.lower()
    page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Cerro Rojo G04</title><link rel="stylesheet" href="../../../assets/quantitative.css">
<script src="../../../assets/plotly-4.1.1.min.js"></script></head><body><main>
<span class="badge">{stage} · CERRO ROJO · DS04/EXP03 · DATOS SINTÉTICOS</span>
<h1>{html.escape(title)}</h1><p class="muted">Corrida <code id="run-id"></code>. Estimaciones en centro de celda y cantidades bajo las reglas de aula.</p>
<p><a href="../../../index.html#{s}" target="_top">Volver al recorrido</a> · <a href="block_model_{s}.csv" download>Modelo completo CSV</a> · <a href="{s}_summary.json">Resumen</a> · <a href="{s}_validation.json">Controles</a> · <a href="manifest.json">Fuentes y hashes</a></p>
<div class="metrics" id="metrics"></div><div class="controls">
<label>Propiedad del bloque<select id="color-mode"></select></label>
<label>Clase candidata<select id="class-filter"><option value="ALL">Todas</option><option>ORE_CANDIDATE</option><option>WASTE_CANDIDATE</option><option>UNCLASSIFIED</option></select></label>
<label><span>Contexto sin ley</span><input id="show-missing" type="checkbox" checked></label>
<label><span>Sondajes</span><input id="show-holes" type="checkbox" checked></label></div>
<p id="drawing-count" class="muted"></p><p id="legend" class="muted"></p><p id="plot-error" role="alert"></p>
<div class="layout"><div class="panel" id="plot" aria-label="Modelo tridimensional G04; arrastra para girar"></div>
<aside class="panel"><h2>Inspeccionar un bloque</h2><p class="muted">Pulsa una caja o escribe su ID, por ejemplo G04-00000.</p>
<label>ID del bloque<input id="block-id" aria-label="ID del bloque"></label><button id="inspect">Consultar bloque</button>
<div class="scroll" id="block-detail" aria-live="polite"></div></aside></div>
<p class="hint">Las cajas muestran la malla geométrica. La porción de roca se integra bajo el TIN y figura en rock_fraction y rock_volume_m3. Gris conserva faltantes. Ocultar una capa no cambia el inventario completo.</p>
<section id="scenario-section" class="panel"><h2>Escenarios de 22 días</h2><div id="scenario-table"></div><p>G04-ALLOC-01: cada bloque participa proporcionalmente dentro de su clase. La asignación es fraccionaria y contable, sin secuencia ni accesibilidad inferidas. A y B conservan el mismo inventario y las mismas tasas de costo; cambia el ciclo y la flota necesaria.</p>
<a href="block_scenario_s12.csv" download>Relación de cada bloque con A/B</a> · <a href="scenario_s12.csv" download>Comparación completa</a></section>
<details><summary>Dato, estimación y supuesto</summary><p>Las muestras y trayectorias proceden de G04. Ley y densidad del bloque son IDW² con soporte comprobado. Igualdad de código litológico es una restricción preliminar, sin continuidad demostrada. Volumen se integra sobre el TIN local adoptado; CRS y datum siguen sin documentarse. El valor en centro representa un proxy académico del bloque. Parámetros de operación y conexión con escenarios son supuestos explícitos. No se asigna clasificación profesional de reserva.</p></details>
</main><script>window.G04_MODEL_GZIP="{data}";</script><script src="../../../assets/quantitative.js"></script></body></html>'''
    (folder/(s+'_model_3d.html')).write_text(page,encoding='utf-8')
