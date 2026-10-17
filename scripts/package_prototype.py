"""Build a complete local prototype ZIP and separate media/checksums.
SPDX-License-Identifier: MIT
No publishing, tagging, Git mutation, or private-source access.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
TAG='v1.2.0-prototype.1'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def package():
    names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    names=sorted({n for n in names if n and (ROOT/n).is_file() and n!='SHA256SUMS.txt'})
    assert not any(n.startswith(('.git/','private-audit/','sources/')) or n.endswith(('.FCBak','.bundle')) for n in names)
    assert len([n for n in names if n.endswith('.FCStd')])==3
    assert len([n for n in names if n.endswith('.stl')])==3
    assert len([n for n in names if n.endswith('.step')])==4
    (ROOT/'SHA256SUMS.txt').write_text(''.join(digest(ROOT/n)+'  '+n+'\n' for n in names),encoding='utf-8')
    names.append('SHA256SUMS.txt')
    out=ROOT.parent/'releases'/TAG;out.mkdir(parents=True,exist_ok=True)
    dest=out/('Avia_35mm_'+TAG+'.zip')
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for n in sorted(names):z.write(ROOT/n,'avia-pole-mount/'+n)
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256(z.read('avia-pole-mount/'+n)).hexdigest()==h,n
    media=[('assets/animations/public-rs4-assembly.gif','Avia_35mm_assembly_en.gif'),
           ('assets/images/complete-setup-person.png','Avia_35mm_complete_setup_en.png')]
    assets=[dest]
    for src,name in media:
        shutil.copyfile(ROOT/src,out/name);assets.append(out/name)
    (out/'SHA256SUMS.txt').write_text(''.join(digest(a)+'  '+a.name+'\n' for a in assets),encoding='utf-8')
    assets.append(out/'SHA256SUMS.txt')
    summary={'tag':TAG,'packaged_files':len(names),'archive_CRC':'passed','embedded_manifest':'passed',
             'assets':[{'name':a.name,'bytes':a.stat().st_size,'sha256':digest(a)} for a in assets]}
    (out/'release-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':package()
