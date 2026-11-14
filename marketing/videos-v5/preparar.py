from pathlib import Path
import subprocess, json

r=Path(__file__).resolve().parent
inputs=['jeans-percha.mp4','outfit-calle.mp4','prendas-tonos.mp4']
# Índice de fuente, cuadro inicial, cantidad de cuadros. Fin exclusivo.
plans={
 'lanzamiento-negro':[(0,0,75),(0,162,75),(0,174,60),(1,45,90),(0,0,75),(0,135,105),(1,24,120)],
 'lanzamiento-blanco':[(1,0,75),(2,123,60),(2,270,45),(0,165,75),(2,483,75),(1,90,60),(2,675,90),(2,285,120)]
}
(r/'beats.json').write_text(json.dumps({'bpm':120,'duration':20,'beats':[i*.5 for i in range(40)],
 'negro_cues':[0,2.5,5,7,10,12.5,16],'blanco_cues':[0,2.5,4.5,6,8.5,11,13,16]},indent=2))
for name,seq in plans.items():
 chain=[]; timeline=[]; offset=0
 for j,(source,start,count) in enumerate(seq):
  # Medio plano de calle: excluye el texto incrustado. No crea otra vista.
  crop='crop=432:600:180:250' if source==1 else 'crop=720:1000:0:0'
  chain.append(f'[{source}:v]trim=start_frame={start}:end_frame={start+count},setpts=PTS-STARTPTS,{crop},scale=720:1000:flags=lanczos,setsar=1[v{j}]')
  timeline.append({'at':offset/30,'source':inputs[source],'from':start/30,'dur':count/30,'source_frames':[start,start+count-1],'crop':crop})
  offset+=count
 assert offset==600
 chain.append(''.join(f'[v{j}]' for j in range(len(seq)))+f'concat=n={len(seq)}:v=1:a=0,format=yuv420p[out]')
 cmd=['ffmpeg','-v','error']
 for file in inputs:cmd+=['-i',str(r/'fuentes'/file)]
 cmd+=['-filter_complex',';'.join(chain),'-map','[out]','-an','-c:v','libx264','-preset','fast','-crf','17','-g','1','-bf','0','-r','30','-y',str(r/(name+'-base.mp4'))]
 subprocess.run(cmd,check=True)
 (r/(name+'-timeline.json')).write_text(json.dumps(timeline,indent=2))

