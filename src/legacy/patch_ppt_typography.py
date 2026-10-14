from pathlib import Path
import json,zipfile,sys,re
from lxml import etree as E
src=Path(sys.argv[1]);layout=Path(sys.argv[2]);out=Path(sys.argv[3])
data=json.loads(layout.read_text(encoding='utf-8'))
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
A='{'+ns['a']+'}'
count=0
with zipfile.ZipFile(src) as z,zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as dest:
    for info in z.infolist():
        raw=z.read(info.filename)
        m=re.fullmatch(r'ppt/slides/slide(\d+)\.xml',info.filename)
        if m:
            i=int(m.group(1))-1;root=E.fromstring(raw)
            objs=[o for o in data['slides'][i]['objects'] if o['kind']=='text']
            shapes=[s for s in root.findall('.//p:sp',ns) if s.find('p:txBody',ns) is not None and s.xpath('.//a:t',namespaces=ns)]
            assert len(shapes)==len(objs),(i,len(shapes),len(objs))
            for s,o in zip(shapes,objs):
                body=s.find('p:txBody',ns)
                for p in body.findall('a:p',ns):
                    pr=p.find('a:pPr',ns)
                    if pr is None:pr=E.Element(A+'pPr');p.insert(0,pr)
                    for tag in ['lnSpc','spcBef','spcAft']:
                        node=pr.find('a:'+tag,ns)
                        if node is not None:pr.remove(node)
                    sp=E.SubElement(pr,A+'lnSpc');E.SubElement(sp,A+'spcPts',val=str(round(o['leading']*100)))
                    for tag in ['spcBef','spcAft']:
                        sp=E.SubElement(pr,A+tag);E.SubElement(sp,A+'spcPts',val='0')
                count+=1
            raw=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
        dest.writestr(info,raw)
print('Exact point spacing applied to',count,'editable text boxes.')
