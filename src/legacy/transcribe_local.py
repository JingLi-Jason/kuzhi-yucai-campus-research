import os, sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / ".work_packages"))
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from faster_whisper import WhisperModel
import av
import numpy as np

def decode_local(path):
    chunks=[]
    resampler=av.AudioResampler(format="s16",layout="mono",rate=16000)
    with av.open(str(path)) as container:
        for frame in container.decode(audio=0):
            for outframe in resampler.resample(frame):
                chunks.append(outframe.to_ndarray().flatten())
        for outframe in resampler.resample(None):
            chunks.append(outframe.to_ndarray().flatten())
    return np.concatenate(chunks).astype(np.float32)/32768.0

base = Path(r"${ORIGINAL_USER_HOME}\Documents\WXWork\1688856569769957\Cache\File\2026-09")
out = Path("材料整理/录音转写")
out.mkdir(parents=True, exist_ok=True)
print("Loading local Chinese transcription model", flush=True)
model = WhisperModel(str(Path(".models/local_small").resolve()), device="cpu", compute_type="int8", cpu_threads=8,
                     download_root=str(Path(".models").resolve()))
for name in ["桂阳县苦志育才公益学校 2.m4a", "桂阳县苦志育才公益学校.m4a", "09.23访谈.MP3"]:
    target = out / (name + ".json")
    if target.exists():
        continue
    print("TRANSCRIBING", name, flush=True)
    segments, info = model.transcribe(decode_local(base / name), language="zh", beam_size=3,
        vad_filter=True, condition_on_previous_text=False,
        initial_prompt="以下是桂阳县苦志育才公益学校调研访谈。学校、公益、老师、学生、教室、操场、宿舍、校医室、资金、厕所、志愿者。")
    rows = []
    with (out / (name + ".txt")).open("w", encoding="utf-8") as f:
        for seg in segments:
            row = {"start": round(seg.start,2), "end":round(seg.end,2),
                   "text":seg.text, "avg_logprob":seg.avg_logprob,
                   "no_speech_prob":seg.no_speech_prob}
            rows.append(row)
            line = f"[{seg.start/60:.2f}–{seg.end/60:.2f}分] {seg.text}"
            f.write(line+"\n"); f.flush()
            print(line, flush=True)
    target.write_text(json.dumps({"source":name,"duration":info.duration,"model":"faster-whisper small int8","segments":rows},ensure_ascii=False,indent=2),encoding="utf-8")
print("ALL DONE",flush=True)
