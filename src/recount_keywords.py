from pathlib import Path
import csv,sys
root=Path(__file__).resolve().parents[1]
corpus=(root/'data/processed/questionnaire_answer_corpus_zh.txt').read_text('utf-8-sig')
with (root/'figures/wordclouds/Word_Cloud_Data.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
errors=[]
for row in rows:
    actual=corpus.count(row['Chinese term'])
    if actual!=int(row['Occurrences']):errors.append(row['Chinese term'])
    row['Recounted occurrences']=actual
out=root/'build';out.mkdir(exist_ok=True)
with (out/'recounted_wordcloud_frequencies.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('FAIL: '+str(errors) if errors else f'PASS: {len(rows)} word-cloud entries match the answer corpus.')
sys.exit(bool(errors))
