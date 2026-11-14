from pathlib import Path
import subprocess,json
root=Path(__file__).resolve().parent; source=root/'source.mp4'
plans={'looks':[(321,60),(30,24),(125,43),(186,78),(366,161),(540,60),(630,108),(765,66)],'consulta':[(125,43),(30,24),(321,60),(186,78),(366,161),(540,60),(630,108),(765,66)]}
for name,cuts in plans.items():
 chain=[]
 for i,(start,count) in enumerate(cuts):
  chain.append(f'[0:v]trim=start_frame={start}:end_frame={start+count},setpts=PTS-STARTPTS[v{i}]')
 chain.append(''.join(f'[v{i}]' for i in range(len(cuts)))+f'concat=n={len(cuts)}:v=1:a=0,crop=590:1048:100:232,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p[v]')
 subprocess.run(['ffmpeg','-v','error','-i',str(source),'-filter_complex',';'.join(chain),'-map','[v]','-an','-c:v','libx264','-preset','fast','-crf','18','-g','1','-bf','0','-r','30','-y',str(root/f'{name}-base.mp4')],check=True)
 offset=0; timeline=[]
 for start,count in cuts:
  timeline.append({'at':offset/30,'from':start/30,'dur':count/30,'source_frames':[start,start+count-1]}); offset+=count
 (root/f'{name}-timeline.json').write_text(json.dumps(timeline,indent=2))
 for at in [0.4,2.4,5,8,13,16,19]:
  subprocess.run(['ffmpeg','-v','error','-i',str(root/f'{name}-base.mp4'),'-ss',str(at),'-frames:v','1','-vf','scale=270:480','-y',str(root/f'{name}-{at}.jpg')],check=True)
from PIL import Image,ImageDraw
sheet=Image.new('RGB',(7*270,510),'#111111')
for i,at in enumerate([0.4,2.4,5,8,13,16,19]):
 sheet.paste(Image.open(root/f'looks-{at}.jpg'),(i*270,30)); ImageDraw.Draw(sheet).text((i*270+5,5),f'{at}s',fill='white')
sheet.save(root/'base-review.jpg',quality=80)
