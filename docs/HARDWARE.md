# V1.2 hardware

Dimensions are mm. Quantities are for one mount. CAD hardware is simplified without detailed threads, end chamfers or runouts. Validate purchased parts and actual full-thread engagement. No tightening torque is established.

| Qty | Part | Application / requirement |
| ---: | --- | --- |
| 1 each | V1.2 ClampFront, ClampRear, AviaBracket | Three printed parts |
| 1 | **Elesa+Ganter GN.35258 — ISO7379-6-M5-50-NI**, AISI304 | Ø6 f9 smooth shoulder ×50 (+0.25), M5×0.8 thread ×9.5; head Ø10×4.5; 3 mm hex |
| 2 | M5×30 DIN912 / ISO4762 A2-70, pitch 0.8 | Closing side opposite hinge |
| 2 | M5×20 DIN912 / ISO4762 A2-70, pitch 0.8 | Tapered joint |
| 4 | DIN934 M5 A2-70, AF8 / H4 | Two closing nuts, two cone nuts |
| 1 | **norelem 07214-105**, M5 DIN985-type A2-70, AF8 / H5 | Hinge retention; threaded metal height 3.2 |
| 5 | Washers ID5.3 × OD10 ×1 | Four bolt heads + one hinge retaining washer |
| 2 | Stainless shims ID6.4 × OD12 ×0.5 | Lower/upper hinge thrust shims |
| 4 | M3×10 DIN912 / ISO4762 A2-70, pitch 0.5 | Sensor |
| 4 | Washers ID3.2 × OD7 ×0.5 | Sensor |

A generic M5 bolt is **not a replacement**. Threads must never be the moving bearing surface. Even unspecified ISO7379 M5 can have a different shoulder diameter (manufacturer notes ISO M5/6.5 deviation). Use the exact Ø6 execution and check transitions. No extra sleeve belongs to V1.2.

## Shoulder and engagement

Head underside / shoulder start Z=−126, smooth shoulder ends −76; printed bearings span −125…−77. Thread spans −76…−66.5, outside bearings. Lower shim −126…−125.5; upper shim −76.5…−76; retaining washer −76…−75; locknut −75…−70. Nominal tip projects 3.5 beyond the whole nut. Usable smooth shoulder must cover at least −125.5…−76.5. Actual retaining-washer ID must be ≤5.5 so it stops on metal. The nut does not preload the plastic stack.

| Fastener | Nominal geometric engagement | Nominal projection / pole clearance |
| --- | ---: | --- |
| Closing M5×30 | 4.0 | 5.5 projection; minimum 11.5 to pole |
| Cone M5×20 | 4.0 | 1.0 projection; 1.5 to pole |
| M3×10 +0.5 washer +7 plate | 2.5 | Confirm actual sensor limit |

Cone screws: conditional tolerance allocation gives minimum 0.171 projection and 0.621 pole clearance. These are geometric stacks, not proof of full thread form/preload. Measure real parts. Hinge endplay nominal 1.0, allocated 0.70–1.55.

Tools: straight 4 mm hex, 4 mm ball-end for 25° access, 3 mm hinge hex, 2.5 mm M3 hex, AF8 socket/wrench.

## Manufacturer sources

- [Elesa+Ganter ISO7379 catalogue / GN.35258](https://www.elesa.com/siteassets/PDF/PDF_EN/ISO%207379.pdf): exact pin dimensions/stainless execution. Does not establish plastic assembly torque.
- [norelem 07214 official family datasheet](https://norelem.co.uk/medias/07214-Datasheet-18389-Hexagon-nuts-with-polyamide-thread-lock-thin-type-DIN-985-enhanced-en.pdf): 07214-105. URL retained from report; packaging web check did not retrieve it. Reconfirm current product data before purchase.
- [Bondhus ball-end access](https://bondhus.com/goldguard-ball-end1).
- [Livox downloads/manuals](https://www.livoxtech.com/avia/downloads).

Links identify dimensional sources, not purchase orders or redistribution permission.


Public-reference edition, 2026-10-17: retained original bracket instructions. RS4 Pro is supported by the pole, independently of this bracket. Simplified reference geometry and animation do not extend prior verification.
