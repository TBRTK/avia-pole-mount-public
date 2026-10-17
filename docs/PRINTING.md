# Printing V1.2 — proposals, not qualified settings

**PETG is a provisional trial material.** No V1.2 print time, printer profile, load rating or measured strength is established. Old interface tests do not qualify V1.2. Use the [three current STLs](../print/v1.2/README.md).

Import STL as **mm**. Meshes retain assembly coordinates: arrange/orient them in the slicer. STEP also uses mm and contains only own print solids.

| Part | Suggested first trial orientation | Support / inspection |
| --- | --- | --- |
| Front/rear clamp | A global-Z end on bed; pole/hinge bores vertical | Removable supports under protruding lugs, tongue, horizontal holes/nut roofs; inspect lower lug near M3 access |
| 20° bracket | Sensor contact plane on bed; turn normal (−sin20°,0,cos20°) to −Z, e.g. global-Y rotation 200° | Receiver, tapered pocket, ribs, horizontal recesses/nut/washer details |

These are trial starting points. Support must not damage flanks, reduce 0.4 mm gaps or seize bearings. Many perimeters and locally dense material around bores/seats/roots are suggestions, not validated strength settings. Check overhangs, bed contact and layer directions in the slicer and record changes.

Measure hinge bore 6.30–6.50, total printed hinge height 47.8–48.2, gaps and hardware stack. Confirm three-flank contact, positive reserves, nut insertion and tool access on real parts. Report material/orientation/settings and measurements. See [physical validation](LIMITATIONS.md).


Public-reference edition, 2026-10-17: retained original bracket instructions. RS4 Pro is supported by the pole, independently of this bracket. Simplified reference geometry and animation do not extend prior verification.
