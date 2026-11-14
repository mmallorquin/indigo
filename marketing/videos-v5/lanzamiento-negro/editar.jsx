export default async ({project}) => {
 const root=process.env.INDIGO_ROOT || "/home/user/indigo-v5";
 const black="#08090B", white="#F7F8FA";
 for(const name of ["lanzamiento-negro","lanzamiento-blanco"]){
  const dark=name==="lanzamiento-negro";
  const bg=dark?black:white, ink=dark?white:black;
  const p=await project({dir:root+"/"+name,size:"1080x1920",fps:30,background:bg});
  const video=await p.add(root+"/"+name+"-base.mp4");
  // Un solo video continuo: geometría proporcional, sin estirar la prenda.
  const states=dark?
   [[0,840,120,650],[2.25,840,120,650],[2.5,1080,0,420],
    [4.75,1080,0,420],[5,540,540,620],[6.75,540,540,620],
    [7,920,80,630],[9.75,920,80,630],[10,680,380,550],
    [12.25,680,380,550],[12.5,1080,0,420],[15.65,1080,0,420],[16,520,560,1060],[20,520,560,1060]]:
   [[0,840,120,730],[2.25,840,120,730],[2.5,540,540,340],
    [4.25,540,540,340],[4.5,1080,0,520],[8.25,1080,0,520],
    [8.5,680,380,580],[10.75,680,380,580],[11,920,80,630],
    [12.75,920,80,630],[13,1080,0,420],[15.65,1080,0,420],[16,520,560,1060],[20,520,560,1060]];
  const track=(property,index,base=0)=>({property,keyframes:states.map(s=>({at:s[0],value:s[index]-base,easing:"house"}))});
  p.compose(<frame width={1080} height={1920} layout="none">
   <frame x={120} y={650} width={840} height={1166.6667} layout="column" clip={true}
    animate={[track("width",1),{property:"height",keyframes:states.map(s=>({at:s[0],value:s[1]*1000/720,easing:"house"}))},track("offsetX",2,120),track("offsetY",3,650)]}
    reveal={{from:"bottom",duration:.45,easing:"ease-out"}}>
    <media file={video} width="fill" height="fill" trimStart={0} fit="contain"/>
   </frame>
  </frame>,{at:0,dur:20,name:"producto-en-movimiento"});
  const words=(lines,at,dur,{x=72,y=240,size=180,gap=0,width=936}={})=>{
   p.compose(<frame width={1080} height={1920} layout="none">
    <frame x={x} y={y} width={width} height={(size*1.2+gap)*lines.length} layout="none" clip={true}
     motion={{enter:{from:{y:60,scale:.94,opacity:0},duration:.42},exit:{to:{y:-35,opacity:0},duration:.18,anchor:"end"}}}>
     {lines.map((line,i)=><frame x={0} y={i*(size*1.2+gap)} width={width} height={size*1.2} layout="none" clip={true}
      reveal={{from:"bottom",at:i*.08,duration:.35,easing:"ease-out"}}>
      <text width={width} height={size*1.2} fontFamily="Inter" fontWeight={800} fontSize={size} letterSpacing={-size*.045} lineHeight={1.12} color={ink}>{line}</text>
     </frame>)}
    </frame>
   </frame>,{at,dur,name:"mensaje-"+at});
  };
  if(dark){
   words(["JEANS."],0,2.2,{size:232,y:235});
   words(["ELEGÍ EL TUYO."],2.5,2.2,{size:114,y:230});
   words(["TU","ESTILO."],5,1.8,{size:120,x:72,y:660,width:445});
   words(["LLEVALO","A TU MANERA."],7,2.7,{size:105,y:230});
   words(["MIRÁ.","ELEGÍ."],10,2.2,{size:94,x:72,y:620,width:295});
   words(["ENCONTRÁ","EL TUYO."],12.5,3.1,{size:119,y:180});
  }else{
   words(["TU PRÓXIMO"],0,2.2,{size:97,y:235});
   words(["LOOK."],.15,2.05,{size:245,y:365});
   words(["ELEGÍ."],2.5,1.8,{size:115,x:72,y:440,width:445});
   words(["COMBINÁ."],4.5,3.65,{size:161,y:240});
   words(["A TU","MANERA"],8.5,2.15,{size:68,x:72,y:560,width:295});
   words(["SALÍ."],11,1.7,{size:224,y:230});
   words(["ARMÁ","TU LOOK."],13,2.55,{size:145,y:160});
  }
  const keyword=dark?"JEANS":"LOOK";
  p.compose(<frame width={1080} height={1920} layout="none">
   <frame x={72} y={245} width={936} height={760} layout="none"
    motion={{enter:{from:{y:45,opacity:0},duration:.38}}}>
    <text x={0} y={0} width={936} height={64} fontFamily="Inter" fontWeight={700} fontSize={34} letterSpacing={4} color={ink}>ÍNDIGO PY</text>
    <text x={0} y={220} width={936} height={100} fontFamily="Inter" fontWeight={500} fontSize={69} letterSpacing={-2} color={ink}>Escribinos</text>
    <frame x={0} y={327} width={936} height={240} layout="none" clip={true} reveal={{from:"left",at:.1,duration:.38,easing:"ease-out"}}>
     <text width={936} height={238} fontFamily="Inter" fontWeight={800} fontSize={dark?210:238} letterSpacing={-10} color={ink}>{keyword}</text>
    </frame>
    <text x={0} y={604} width={936} height={95} fontFamily="Inter" fontWeight={500} fontSize={57} letterSpacing={-1} color={ink}>por WhatsApp</text>
   </frame>
  </frame>,{at:16,dur:4,name:"consulta-whatsapp"});
  // Acentos de paso suaves: no destellos ni rebotes continuos.
  for(const t of (dark?[2.5,5,7,10,12.5]:[2.5,4.5,8.5,11,13])){
   p.compose(<rect x={0} y={0} width={1080} height={1920} fill={bg}
    animate={[{property:"opacity",from:.14,to:0,duration:.18,easing:"ease-out"}]}/>,{at:t,dur:.18,name:"acento-corte-"+t});
  }
  for(const [tag,time] of [["portada",1.3],["producto",6.2],["look",9.1],["cierre",17.4]]){
   await p.frame(time,root+"/"+name+"-"+tag+".png");
  }
 }
};

