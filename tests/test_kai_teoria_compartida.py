"""Comprueba que el recorrido operativo usa modelos propios y persistencia local."""
from __future__ import annotations
import importlib
import json
from pathlib import Path
import sys
import zipfile
import pytest

ROOT = Path(__file__).resolve().parent.parent
GROUP = json.loads((ROOT / 'kai/config_teoria_v2.json').read_text(encoding='utf-8'))['grupo']
sys.path.insert(0, str(ROOT / 'kai'))
controller = importlib.import_module('recorrido_' + GROUP.lower())
theory = controller.theory


@pytest.fixture
def private_data(tmp_path, monkeypatch):
    folder = tmp_path / 'private'
    monkeypatch.setattr(theory, 'DATA', folder)
    monkeypatch.setattr(controller, 'DATA', folder)
    monkeypatch.setattr(controller.e1, 'DATA', folder)
    return folder


def test_identidad_y_contrato(private_data):
    state = controller.process({'operacion': 'estado', 'alumno': 'AlumnoDemo'})
    assert state['actividad_actual'] == 'E1.01'
    assert state['eventos'] == 0
    assert state['entrega_final_lista'] is False
    assert [sum(a['etapa'] == k for a in theory.ACTIVIDADES) for k in ('E1', 'S11', 'S12')] == [8, 16, 6]
    assert all(state['productos_grupales'][s]['status'] == 'VALIDATED' for s in ('S11', 'S12'))
    assert state['ficha_e1']['total'] == 21
    assert state['aplicacion_individual_v3']['total'] == 26
    assert all('G05' not in json.dumps(a, ensure_ascii=False) and 'Santa Elena' not in json.dumps(a, ensure_ascii=False) for a in theory.ACTIVIDADES)


def test_rechazo_recuperacion_y_excel(private_data):
    alias = 'AlumnoDemo'
    base = {'alumno': alias, 'operacion': 'registrar', 'actividad': 'E1.01',
            'estado': 'DEMOSTRADO', 'tipo_evidencia': 'RAZONAMIENTO_PROPIO',
            'criterio_observado': 'Razón espacial propia'}
    with pytest.raises(ValueError):
        controller.process(dict(base, respuesta='Sí'))
    with pytest.raises(ValueError):
        controller.process({'operacion': 'iniciar_etapa', 'alumno': alias, 'etapa': 'S11'})
    answer = 'No extendería una muestra a todo el depósito porque solo representa su ubicación.'
    state = controller.process(dict(base, respuesta=answer))
    assert state['actividad_actual'] == 'E1.02' and state['eventos'] == 1
    reload = controller.process({'operacion': 'estado', 'alumno': alias})
    assert reload['actividad_actual'] == 'E1.02' and reload['eventos'] == 1
    assert controller.process(dict(base, respuesta=answer))['duplicado'] is True
    other = controller.process({'operacion': 'estado', 'alumno': 'OtraPersona'})
    assert other['eventos'] == 0 and other['actividad_actual'] == 'E1.01'
    with zipfile.ZipFile(state['xlsx']) as archive:
        assert archive.testzip() is None and 'xl/workbook.xml' in archive.namelist()
    assert controller.process({'operacion': 'verificar', 'alumno': alias})['integridad_sqlite'] == 'ok'
    with pytest.raises(ValueError):
        controller.process({'operacion': 'entregar_individual', 'alumno': alias})
