from pathlib import Path
import subprocess,json,re,sys
root=Path(__file__).resolve().parents[2]
for src in sorted((root/'work').glob('*-mix.mp4')):
 if len(sys.argv)>1 and not any(src.name.startswith(n) for n in sys.argv[1:]):continue
 analyze=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af','loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json','-vn','-f','null','-'],capture_output=True,text=True,check=True)
 m=re.search(r'\{\s*"input_i".*?\}',analyze.stderr,re.S);r=json.loads(m.group())
 filt='loudnorm=I=-14:TP=-1.8:LRA=11:measured_I='+r['input_i']+':measured_LRA='+r['input_lra']+':measured_TP='+r['input_tp']+':measured_thresh='+r['input_thresh']+':offset='+r['target_offset']+':linear=true:print_format=json'
 dest=root/'reels'/src.name.replace('-mix','')
 done=subprocess.run(['ffmpeg','-hide_banner','-y','-i',str(src),'-map','0:v:0','-map','0:a:0','-c:v','copy','-af',filt,'-ar','48000','-c:a','aac','-b:a','320k','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(dest)],capture_output=True,text=True,check=True)
 (root/'qa'/(dest.stem+'-master.json')).write_text(json.dumps(dict(primera_pasada=r,segunda_pasada=re.findall(r'\{\s*"input_i".*?\}',done.stderr,re.S),objetivo=dict(lufs=-14,true_peak_maximo_dbtp=-1.5,margen_antes_aac=-1.8)),ensure_ascii=False,indent=2))
 print('MASTER '+dest.name,flush=True)
