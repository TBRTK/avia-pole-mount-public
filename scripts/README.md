# New public-edition utilities

Scripts are MIT licensed. They do not download models. The separate Emlid model has its own source and copyright record and is excluded from MIT/CC grants.

- `clean_cad.py PRIVATE_CAD_DIR OUTPUT_CAD_DIR`: run with FreeCAD Python on local private source copies. Does not save originals or touch Git; refuses output overwrite. Retains native user features, replaces imports, checks print equivalence and removes old GUI records/thumbnails.
- `style_views.FCMacro`: run in FreeCAD GUI after cleaning; saves only public files with clean visibility/colours. Backups are excluded from packaging.
- `add_emlid_reference.py`: FreeCAD Python, adds the local official Pro STEP to V1.2 after reviewing its source record and rights notice. Run between cleaning and GUI styling; refuses to add a duplicate. Manufacturer data remains separately owned by Emlid.
- `render_media.FCMacro`: reads clean V1.2, including Emlid reference CAD, creates a separate shape-copy presentation, renders 84 frames/stills. Does not save the source. 6 fps /14 seconds, plus a 4-second final concept image during GIF encoding; selected illustrative stages, not verified motion.
- `finish_media.py`: Python/Pillow captions and GIF encoding after rendering.
- `verify_public.py`: FreeCAD Python reopen/recompute, parameter, reference and export checks without source saves.
- `package_prototype.py`: builds the complete prototype ZIP, separate English GIF/PNG and SHA256 checksums under the sibling `releases/` folder. Does not publish or modify Git.

The concept illustration uses the clean assembly still. Prompt/tool/limits: `assets/images/illustration-provenance.json`.
