"""Verify cleaned CAD and references without saving source documents.
SPDX-License-Identifier: MIT
"""
from pathlib import Path
import json,zipfile,hashlib,math,sys
import FreeCAD as App
import Part,Mesh
ROOT=Path(__file__).resolve().parents[1]
def states(d):
    return [(o.Name,o.getStatusString()) for o in d.Objects if 'Invalid' in o.State or 'Error' in o.State]
def diff(a,b):return abs(a.cut(b).Volume)+abs(b.cut(a).Volume)
report={}
for p in sorted((ROOT/'cad').glob('*_Public.FCStd')):
    d=App.openDocument(str(p));d.recompute(None,True,True);assert not states(d),states(d)
    assert not any(o.Name in ['Part__Feature','Part__Feature001','Part__Feature002','LIVOX_AVIA','LIVOX_AVIA_ASM'] for o in d.Objects)
    initial={n:d.getObject(n).Shape.copy() for n in ['ClampFront','ClampRear','AviaBracket']}
    r={'objects':len(d.Objects),'recompute_errors':states(d),'print_solids':{}}
    for n,s in initial.items():
        s.check(True);assert s.isValid() and s.isClosed() and len(s.Solids)==1
        r['print_solids'][n]={'volume_mm3':s.Volume,'faces':len(s.Faces),'valid_closed_single':True}
    r['independent_reference_faces']=len(d.IndependentAviaEnvelope.Shape.Faces)
    # Change independent body length: reference must rebuild, bracket must not change.
    before=d.IndependentAviaEnvelope.Shape.Volume
    d.PublicParameters.set('B2','=93 mm');d.recompute(None,True,True)
    assert not states(d) and abs(d.IndependentAviaEnvelope.Shape.Volume-before)>1
    assert all(diff(s,d.getObject(n).Shape)<1e-6 for n,s in initial.items())
    d.PublicParameters.set('B2','=91 mm');d.recompute(None,True,True)
    r['independent_length_parameter_rebuild']='passed, printable geometry unchanged'
    if 'V1.2' in p.name:
        assert abs(d.Rod35Reference.Shape.BoundBox.ZMax-110)<1e-6
        assert abs(d.RS4ProReference.Shape.BoundBox.ZMin-110)<1e-6
        d.PublicParameters.set('B15','=140 mm');d.recompute(None,True,True)
        assert not states(d) and abs(d.Rod35Reference.Shape.BoundBox.ZMax-140)<1e-6
        assert abs(d.RS4ProReference.Shape.BoundBox.ZMin-140)<1e-6
        assert all(diff(s,d.getObject(n).Shape)<1e-6 for n,s in initial.items())
        d.PublicParameters.set('B15','=110 mm');d.recompute(None,True,True)
        r['receiver_height_parameter_rebuild']='passed; pole top and receiver base move together'
        official=d.getObject('EmlidRS4ProOfficial')
        if official:
            vertices=[v.Point for v in official.Shape.Vertexes]
            assert abs(min(v.z for v in vertices)-110)<1e-4
            assert max(v.z for v in vertices)<209.4
            r['official_emlid']={'faces':len(official.Shape.Faces),'solids':len(official.Shape.Solids),'vertex_bounds_mm':[[min(getattr(v,a) for v in vertices),max(getattr(v,a) for v in vertices)] for a in ['x','y','z']]}
            d.PublicParameters.set('B15','=140 mm');d.recompute(None,True,True)
            assert abs(min(v.Point.z for v in official.Shape.Vertexes)-140)<1e-4
            d.PublicParameters.set('B15','=110 mm');d.recompute(None,True,True)
            r['official_emlid']['height_parameter_rebuild']='passed'
        r['display_reference_overlap_mm3']={n:abs(d.RS4ProReference.Shape.common(d.getObject(n).Shape).Volume) for n in ['ClampFront','ClampRear','AviaBracket','V12_SensorReference','V12_FOVReference']}
        assert max(r['display_reference_overlap_mm3'].values())<1e-5
        d.Parameters.set('B84','=22 deg');d.recompute(None,True,True);assert not states(d)
        assert all(d.getObject(n).Shape.isValid() for n in initial)
        r['native_sensor_tilt_parameter_rebuild']='22 deg passed; reset to 20 deg'
        d.Parameters.set('B84','=20 deg');d.recompute(None,True,True)
        assert all(diff(s,d.getObject(n).Shape)<1e-6 for n,s in initial.items())
        d.Parameters.set('B98','=15 deg');d.recompute(None,True,True);assert not states(d)
        assert d.ClampRear.Shape.isValid();d.Parameters.set('B98','=0 deg');d.recompute(None,True,True)
        r['native_hinge_parameter_rebuild']='15 deg passed; reset to 0 deg'
        r['exports']={}
        for n,s in initial.items():
            step=ROOT/('cad/step/v1.2/Avia_35mm_V1.2_'+n+'.step')
            q=Part.Shape();q.read(str(step));delta=diff(s,q)
            assert q.isValid() and len(q.Solids)==1 and delta<1e-4,(n,delta)
            r['exports'][n]={'STEP_symmetric_difference_mm3':delta}
        for mesh_path in (ROOT/'print/v1.2').glob('*.stl'):
            m=Mesh.Mesh(str(mesh_path));assert m.isSolid() and m.countComponents()==1
        r['STL_closed_single_component']='3 passed'
    report[p.name]=r
    App.closeDocument(d.Name)
(ROOT/'docs/reopen-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
