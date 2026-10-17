"""Add local owner-approved manufacturer Emlid CAD to an already clean V1.2.
Copyright Emlid applies to model data; script SPDX-License-Identifier: MIT
"""
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'cad/vendor/emlid/Reach_RS4_Pro.step'
assert (source.parent/'permission-record.json').exists(),'Review scoped permission before adding vendor CAD'
d=App.openDocument(str(ROOT/'cad/Avia_PoleMount_35mm_V1.2_Public.FCStd'))
if d.getObject('EmlidRS4ProOfficial'):raise RuntimeError('Official model already present; no changes saved')
s=Part.Shape();s.read(str(source))
o=d.addObject('Part::Feature','EmlidRS4ProOfficial');o.Shape=s
o.Placement=App.Placement(App.Vector(132.8,48.3,110),App.Rotation(App.Vector(1,0,0),90))
for field,e in [('x','Parameters.RodX'),('y','Parameters.CenterY'),('z','PublicParameters.PoleTopZ')]:
    o.setExpression('Placement.Base.'+field,e)
o.addProperty('App::PropertyString','RightsNotice')
o.RightsNotice='Copyright Emlid; owner-stated publication/rendering approval; excluded from TBRTK CC/MIT. See cad/vendor/emlid/permission-record.json.'
d.AssemblyReferences.addObject(o);d.recompute();d.save();App.closeDocument(d.Name)
print('Approved Emlid geometry added. Run style_views.FCMacro for GUI styling.')
