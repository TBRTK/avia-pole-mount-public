"""Build clean native FreeCAD copies from a LOCAL PRIVATE source directory.

Run with FreeCAD's Python: clean_cad.py PRIVATE_CAD_DIR OUTPUT_CAD_DIR
No downloads, original writes, Git operations, or manufacturer-solid sampling.
SPDX-License-Identifier: MIT
"""
from pathlib import Path
import sys, json, zipfile, hashlib, math
import FreeCAD as App
import Part, Sketcher
V=App.Vector

def expr(obj, prop, value):
    obj.setExpression(prop, value)

def new_references(d, rs4=False):
    p=d.addObject('Spreadsheet::Sheet','PublicParameters')
    p.Label='Independent reference parameters (mm / deg)'
    rows=[
        ('BodyLength','91 mm'),('BodyWidth','64.8 mm'),('BodyHeight','61.2 mm'),
        ('TopAllowance','6 mm'),('NominalM3Diameter','3 mm'),('NominalThreadDepth','4 mm'),
        ('FOVHorizontal','70.4 deg'),('FOVVertical','77.2 deg'),('FOVLength','300 mm'),
        ('FOVApertureHalfY','32.4 mm'),('FOVApertureHalfZ','30.6 mm'),
        ('RS4Diameter','128.6 mm'),('RS4Height','99.3 mm'),('PoleTopZ','110 mm'),
        ('PoleDisplayBottomZ','-260 mm'),('StudDiameter','15.875 mm'),
        ('StudEngagement','10 mm')]
    for i,(name,value) in enumerate(rows,2):
        p.set('A'+str(i),name);p.set('B'+str(i),'='+value);p.setAlias('B'+str(i),name)
    p.set('C5','Extra clearance, illustrative; not manufacturer geometry')
    p.set('C15','Illustrative installation height; adjust to measured pole')
    p.set('C18','Visual stud only; not a thread/engagement specification')
    box=d.addObject('Part::Box','IndependentAviaBox')
    for prop,formula in [('Length','PublicParameters.BodyLength'),('Width','PublicParameters.BodyWidth'),
                         ('Height','PublicParameters.BodyHeight + PublicParameters.TopAllowance'),
                         ('Placement.Base.x','Parameters.AviaHoleX1 - 6 mm'),
                         ('Placement.Base.y','Parameters.CenterY - PublicParameters.BodyWidth / 2'),
                         ('Placement.Base.z','Parameters.AviaMountZ')]:expr(box,prop,formula)
    holes=[]
    for i,(x,y) in enumerate([('AviaHoleX1','AviaHoleY1'),('AviaHoleX1','AviaHoleY2'),
                               ('AviaHoleX2','AviaHoleY1'),('AviaHoleX2','AviaHoleY2')],1):
        o=d.addObject('Part::Cylinder','IndependentMountBore'+str(i))
        for prop,f in [('Radius','PublicParameters.NominalM3Diameter / 2'),('Height','PublicParameters.NominalThreadDepth'),
                       ('Placement.Base.x','Parameters.'+x),('Placement.Base.y','Parameters.'+y),
                       ('Placement.Base.z','Parameters.AviaMountZ')]:expr(o,prop,f)
        holes.append(o)
    cutter=d.addObject('Part::MultiFuse','IndependentMountBores');cutter.Shapes=holes
    env=d.addObject('Part::Cut','IndependentAviaEnvelope');env.Base=box;env.Tool=cutter
    env.Label='Independent Avia clearance block / four nominal M3 bores'
    cable=d.addObject('Part::Cylinder','IndependentConnectorEnvelope')
    for prop,f in [('Radius','Parameters.ConnectorKeepoutRadius'),('Height','80 mm'),
                   ('Placement.Base.x','Parameters.AviaConnectorX'),('Placement.Base.y','Parameters.AviaConnectorY'),
                   ('Placement.Base.z','Parameters.AviaMountZ + PublicParameters.BodyHeight')]:expr(cable,prop,f)
    cable.Label='Provisional connector / cable keepout, not connector CAD'
    sections=[]
    # Two rectangles perpendicular to -X, defined from angles with tan(theta/2).
    for index in range(2):
        s=d.addObject('Sketcher::SketchObject','IndependentFOVSection'+str(index))
        s.Placement.Rotation=App.Rotation(V(0,0,1),V(-1,0,0))
        expr(s,'Placement.Base.x','Parameters.AviaHoleX1 - 6 mm'+(' - PublicParameters.FOVLength' if index else ''))
        expr(s,'Placement.Base.y','Parameters.CenterY')
        expr(s,'Placement.Base.z','Parameters.AviaMountZ + PublicParameters.BodyHeight / 2')
        # Local sketch X maps to world Z; sketch Y maps to world Y.
        a='PublicParameters.FOVApertureHalfZ'+(' + PublicParameters.FOVLength * tan(PublicParameters.FOVVertical / 2)' if index else '')
        b='PublicParameters.FOVApertureHalfY'+(' + PublicParameters.FOVLength * tan(PublicParameters.FOVHorizontal / 2)' if index else '')
        for j,(sa,sb) in enumerate([(-1,-1),(1,-1),(1,1),(-1,1)]):
            g=s.addGeometry(Part.Point(V(sa*30,sb*32,0)))
            ix=s.addConstraint(Sketcher.Constraint('DistanceX',g,1,sa*30.0))
            iy=s.addConstraint(Sketcher.Constraint('DistanceY',g,1,sb*32.0))
            expr(s,'Constraints['+str(ix)+']',('' if sa==1 else '-(')+a+('' if sa==1 else ')'))
            expr(s,'Constraints['+str(iy)+']',('' if sb==1 else '-(')+b+('' if sb==1 else ')'))
        # Lines coincident to the four parametrized points.
        for j in range(4):
            g=s.addGeometry(Part.LineSegment(V(0,0,0),V(1,1,0)),False)
            s.addConstraint(Sketcher.Constraint('Coincident',g,1,j,1))
            s.addConstraint(Sketcher.Constraint('Coincident',g,2,(j+1)%4,1))
        sections.append(s)
    fov=d.addObject('Part::Loft','IndependentFOVKeepout');fov.Sections=sections;fov.Solid=True;fov.Ruled=True
    fov.Label='Independent conservative FOV, 70.4 x 77.2 deg'
    group=d.addObject('App::DocumentObjectGroup','IndependentReferenceConstruction')
    for o in [box,*holes,cutter,*sections]:group.addObject(o)
    if rs4:
        r=d.addObject('Part::Cylinder','RS4ProEnvelope')
        for prop,f in [('Radius','PublicParameters.RS4Diameter / 2'),('Height','PublicParameters.RS4Height'),
                       ('Placement.Base.x','Parameters.RodX'),('Placement.Base.y','Parameters.CenterY'),
                       ('Placement.Base.z','PublicParameters.PoleTopZ')]:expr(r,prop,f)
        r.Label='Reach RS4 Pro - independent diameter/height envelope'
        rod=d.getObject('Rod35Reference')
        expr(rod,'Placement.Base.z','PublicParameters.PoleDisplayBottomZ')
        expr(rod,'Height','PublicParameters.PoleTopZ - PublicParameters.PoleDisplayBottomZ')
        stud=d.addObject('Part::Cylinder','SurveyPoleStudReference')
        for prop,f in [('Radius','PublicParameters.StudDiameter / 2'),('Height','PublicParameters.StudEngagement'),
                       ('Placement.Base.x','Parameters.RodX'),('Placement.Base.y','Parameters.CenterY'),
                       ('Placement.Base.z','PublicParameters.PoleTopZ')]:expr(stud,prop,f)
        stud.Label='5/8 UNC nominal interface marker; unthreaded, illustrative'
        # Cylinder bore uses nominal major diameter for a clearance marker only.
        tool=d.addObject('Part::Cylinder','RS4MountBoreMarker')
        for prop,f in [('Radius','PublicParameters.StudDiameter / 2'),('Height','PublicParameters.StudEngagement'),
                       ('Placement.Base.x','Parameters.RodX'),('Placement.Base.y','Parameters.CenterY'),
                       ('Placement.Base.z','PublicParameters.PoleTopZ')]:expr(tool,prop,f)
        cut=d.addObject('Part::Cut','RS4ProReference');cut.Base=r;cut.Tool=tool
        cut.Label='Reach RS4 Pro - simplified independent envelope'
        group.addObject(r);group.addObject(tool)
        d.AssemblyReferences.addObject(cut);d.AssemblyReferences.addObject(stud)
    return env,cable,fov

def strip_archive(path):
    # Old thumbnails and GUI property records may depict the removed reference.
    # A fresh GUI presentation is generated separately, never copied from source.
    with zipfile.ZipFile(path) as z:
        payload={n:z.read(n) for n in z.namelist() if n not in ['GuiDocument.xml'] and not n.lower().startswith('thumbnails/')}
    temp=path.with_suffix('.clean-tmp')
    with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in payload.items():z.writestr(n,b)
    temp.replace(path)

def clean(source,out):
    source,out=Path(source),Path(out);out.mkdir(parents=True,exist_ok=True)
    all_checks={}
    for path in sorted(source.glob('Avia_PoleMount_35mm_V*.FCStd')):
        d=App.openDocument(str(path))
        before={o.Name for o in d.Objects}
        own={n:d.getObject(n).Shape.copy() for n in ['ClampFront','ClampRear','AviaBracket']}
        # Record exact old BREP members to catch hidden, cached duplicates later.
        with zipfile.ZipFile(path) as z:
            old_breps={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith(('Part__Feature.','Part__Feature001.','Part__Feature002.','V12_SensorReference.','V12_ConnectorReference.','V12_FOVReference.'))}
        env,cable,fov=new_references(d,rs4='V1.2' in path.name)
        for name,new in [('V12_SensorReference',env),('V12_ConnectorReference',cable),('V12_FOVReference',fov)]:
            o=d.getObject(name)
            if o:o.Links=[new];o.Label=new.Label+' / follows sensor tilt'
        removed=['Part__Feature','Part__Feature001','Part__Feature002','LIVOX_AVIA','LIVOX_AVIA_ASM']
        for name in ['LIVOX_AVIA','LIVOX_AVIA_ASM']:
            o=d.getObject(name)
            if o:
                org=o.Origin
                removed.extend([x.Name for x in org.OriginFeatures]+[org.Name])
        for name in removed:
            if d.getObject(name):d.removeObject(name)
        if 'V1.2' not in path.name:
            for o in [env,cable,fov]:d.AssemblyReferences.addObject(o)
        d.Label=path.stem+' - Public references'
        d.CreatedBy='TBRTK';d.LastModifiedBy='TBRTK'
        d.Comment='Own bracket preserved. Independently built Avia / RS4 reference geometry. See NOTICE.md.'
        for o in d.Objects:
            if 'EngineeringReport' in o.PropertiesList:
                o.EngineeringReport='Historical engineering report retained privately. Public reference edition: see docs/VERIFICATION.md and docs/LIMITATIONS.md. Original bracket geometry retained; physical validation pending.'
            if 'ValidationJSON' in o.PropertiesList:
                o.ValidationJSON=json.dumps({'status':'prototype, physical validation pending','historical_evidence':'preserved privately','public_checks':'docs/reopen-checks.json'})
            if 'OfficialManual' in o.PropertiesList:o.OfficialManual=''
        d.recompute(None,True,True)
        checks={}
        for n,s in own.items():
            q=d.getObject(n).Shape
            delta=s.cut(q).Volume+q.cut(s).Volume
            checks[n]={'valid':q.isValid(),'closed':q.isClosed(),'solids':len(q.Solids),'volume_mm3':q.Volume,'symmetric_difference_mm3':delta}
            assert q.isValid() and q.isClosed() and len(q.Solids)==1 and delta<1e-6,(n,checks[n])
        assert before-{o.Name for o in d.Objects}<=set(removed),'Unexpected removal of original objects'
        assert env.Shape.isValid() and fov.Shape.isValid() and len(fov.Shape.Solids)==1
        assert not [(o.Name,o.getStatusString()) for o in d.Objects if 'Invalid' in o.State or 'Error' in o.State]
        dest=out/(path.stem+'_Public.FCStd')
        if dest.exists():raise FileExistsError(dest)
        d.saveAs(str(dest));App.closeDocument(d.Name);strip_archive(dest)
        with zipfile.ZipFile(dest) as z:
            assert not any(hashlib.sha256(z.read(n)).hexdigest() in old_breps for n in z.namelist()),'Old reference BREP survived'
        all_checks[dest.name]={'preserved_print_parts':checks,'removed_import_objects':removed,'old_reference_BREP_absent':True}
        print(dest.name,checks,flush=True)
    return all_checks

if __name__=='__main__':
    checks=clean(sys.argv[1],sys.argv[2])
    (Path(sys.argv[2]).parent/'docs').mkdir(exist_ok=True)
    (Path(sys.argv[2]).parent/'docs/geometry-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
