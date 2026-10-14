from pathlib import Path
root=Path(__file__).parent
b=root/'论文与作品集/工作文件/ppt_build'
s=(b/'build_publication.mjs').read_text('utf-8')
for a,v in [
    ('../../对外展示修订版','../../英文15页紧凑版'),
    ("['EN','ZH']","['EN']"),
    ('publication_layout_','tight15_layout_'),
    ('publication_candidate_','tight15_candidate_'),
    ('publication_exact_','tight15_exact_'),
    ('Campus_Research_Portfolio_${lang}_Final.pptx','Campus_Research_Portfolio_${lang}_15pages_Final.pptx'),
    ('validation_publication_${lang}_Final.json','validation_tight15_${lang}_Final.json'),
    ('explicitTotalSlideCount:24,requiredNativeChartOwnerSlides:[6]',
     'explicitTotalSlideCount:15,requiredNativeChartOwnerSlides:[3,4]'),
]:
    s=s.replace(a,v)
(b/'build_tight15.mjs').write_text(s,'utf-8')
s=(root/'export_publication_checks.ps1').read_text('utf-8')
for a,v in [
    ("@('EN','ZH')","@('EN')"),
    ('对外展示修订版','英文15页紧凑版'),
    ('Campus_Research_Portfolio_${language}_Final.pptx','Campus_Research_Portfolio_${language}_15pages_Final.pptx'),
    ('Publication_metrics_','Tight15_metrics_'),
    ('Publication_${language}.pdf','Tight15_${language}.pdf'),
]:
    s=s.replace(a,v)
(root/'export_tight15_checks.ps1').write_text(s,'utf-8')
s=(root/'review_publication.py').read_text('utf-8')
for a,v in [
    ("['EN','ZH']","['EN']"),
    ('对外展示修订版','英文15页紧凑版'),
    ('publication_review','tight15_review'),
    ('Campus_Research_Portfolio_{lang}_Final.pptx','Campus_Research_Portfolio_{lang}_15pages_Final.pptx'),
    ('len(names)==24','len(names)==15'),
    ('Publication_metrics_','Tight15_metrics_'),
    ('Publication_{lang}.pdf','Tight15_{lang}.pdf'),
]:
    s=s.replace(a,v)
(root/'review_tight15.py').write_text(s,'utf-8')
