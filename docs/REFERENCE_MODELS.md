# Independent references

## Avia

Sources checked: [official downloads](https://www.livoxtech.com/avia/downloads), [Avia User Manual 202204](https://terra-1-g.djicdn.com/65c028cd298f4669a7f0e40e50ba1131/Download/Avia/Livox%20Avia%20User%20Manual%20202204.pdf), section 3.3 / appendix 1 and FOV section. The PDF is linked, not bundled. Dimensions were checked from the published drawing, not generated from STEP.

| Parameter | Definition |
| --- | --- |
| Length / cross-section | 91 /64.8 /61.2 mm in bracket coordinates |
| Upper allowance | Additional 6 mm, approximate clearance only |
| Mount centers | X=25.8 /104.8, Y=25.3 /71.3 mm; 79 ×46 mm pitch |
| Contact plane | Z=-69.1 mm before V1.2 tilt |
| Bore markers | Four Ø3 ×4 mm cylinders, no thread form or permitted penetration claim |
| V1.2 tilt | Existing 20° down around (104.8,48.3,-69.1) mm |
| FOV | Rectangular ruled loft, H70.4° ×V77.2°, local forward -X |
| Near FOV aperture | Enlarged 64.8 ×61.2 mm rectangle centered on nominal axis |
| Far half size | Near half size + extent ×tan(full angle/2), per axis |
| FOV extent | 300 mm default; illustration/checking extent, not sensor range |
| Connector/cable | Provisional Ø30 ×80 mm keepout at inherited connector coordinates |

The block has no copied fins, optical detail, labels or surfaces. The upper allowance does not prove every real feature is enclosed. Simplified references do not certify fit or unrestricted optics. Check the real assembly and current manufacturer instructions.

## Reach RS4 Pro

Sources checked 2026-10-17: [official specs/CAD links](https://docs.emlid.com/reachrs4/specifications/specs/), [product specs](https://emlid.com/reachrs4pro/). Published envelope 128.6 ×128.6 ×99.3 mm; mass 943 g. Public geometry is only a cylinder and nominal 5/8-UNC interface marker, independently built without reading/sampling Emlid STEP geometry.

`PublicParameters.PoleTopZ=110 mm` sets the receiver base/ARP height in assembly coordinates. X/Y follow the pole center (132.8,48.3). This is an illustrative height; set it from measurement. `PoleDisplayBottomZ=-260 mm` controls the displayed pole segment. No quick release is assumed. The nominal 15.875 mm stud diameter and 10 mm engagement marker are illustrative, not a thread-fit or safe-penetration specification.

Cameras, ports and the separate radio antenna are omitted. GNSS APC/ARP and Avia-to-GNSS lever-arm calibration are outside this reference. Do not use display coordinates as survey offsets. Added equipment/mass requires a new system assessment, including on a tilted pole.

The user supplied a STEP whose header says `Reach RS4.step`; it is not substituted for Pro. The distinct official Pro STEP was retrieved and kept unchanged. After the owner explicitly confirmed permission for GitHub/FreeCAD publication and rendering, it was added to [vendor/emlid](../cad/vendor/emlid/README.md) and embedded as `EmlidRS4ProOfficial` in V1.2. Source +Y maps to global +Z, origin to the pole top; its placement follows `PoleTopZ`. The simplified cylinder remains hidden for approximate checks. The actual manufacturer's ports/cameras/housing are displayed; camera view and calibration are not certified. No Livox manufacturer solid is included.
