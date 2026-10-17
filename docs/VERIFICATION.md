# Verification of the public edition

FreeCAD 1.1.4 / OCCT, checked 2026-10-17. [Initial cleanup](geometry-checks.json) and [reopen/parameter/export checks](reopen-checks.json) provide results.

- Original and cleaned ClampFront, ClampRear and AviaBracket: **0 mm³ symmetric difference** for all nine version/part combinations. All outputs are valid, closed single solids; full BOP checks pass.
- Reopened and force-recomputed all three public CAD files: no invalid/error states. Native user designs remain; only imported Livox nodes/origins were removed.
- Independent body length 91→93→91 mm: envelope rebuilds, all printable solids remain unchanged.
- V1.2 pole-top height 110→140→110 mm: pole top and RS4 envelope move together; print geometry remains unchanged.
- Official Emlid model: 4,876 faces /11 solids; source mounting origin maps to Z=110 mm and follows height changes. The source STEP remains byte-identical. Emlid inclusion relies on the owner's expressly confirmed publication/rendering approval, separately recorded.
- Original native sensor tilt 20→22→20° and rear hinge opening 0→15→0° rebuild successfully; reset geometry equals nominal.
- Added nominal RS4 envelope has zero volumetric overlap with the three print parts, independent Avia block and conservative FOV. These are nominal display-configuration checks, not real receiver/camera/radio clearance certification.
- Each unchanged V1.2 STEP reimports as one valid solid and has zero symmetric difference from its CAD output within OCCT tolerance. Three STL meshes are closed, single connected components.
- Every original file and all six print export files are checked by SHA256 against the baseline. Old manufacturer reference BREP records are absent from cleaned FCStd archives; clean GUI views are freshly generated.
- New GIF frames are decoded and staged views visually reviewed. The 14-second CAD sequence is followed by a 4-second concept image, total 18 seconds. Animation is illustrative, not a new continuously collision-free motion proof.

Original private evidence reports 113 discrete hinge positions, not a complete continuous sweep. Physical strength, preload, long-term play, creep, real tool access, all thread limits and calibration remain unqualified. Added receiver/system mass and RPi installation require fresh physical assessment. See [limitations](LIMITATIONS.md).
