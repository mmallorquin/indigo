export default async ({project}) => {
 const root = process.env.INDIGO_ROOT || "/home/user/indigo-v3";
 const ink = "#172346", cobalt = "#3155E7";
 const titleFont = "Bebas Neue", infoFont = "DM Sans";
 const reveal = {by:"word", from:{opacity:0,y:35,scale:.94}, duration:.42, overlap:.4, easing:"house"};
 const entrance = {enter:{from:{x:-35,opacity:0,scale:.97},duration:.32}, exit:{to:{y:-22,opacity:0},duration:.2,anchor:"end"}};
 for (const name of ["looks", "consulta"]) {
  const p = await project({dir:root+"/"+name,size:"1080x1920",fps:30,background:"#F4F1EB"});
  const base = await p.add(root+"/"+name+"-base.mp4");
  p.cut(base,{at:0,from:0,dur:20,fit:"contain"});
  const word = (text, at, dur, size=145, y=110) => {
   p.compose(<frame width={1080} height={1920} layout="none">
    <frame x={70} y={y} width={925} height={245} layout="none" motion={entrance}>
     <text width={925} height={220} fontFamily={titleFont} fontSize={size} color={ink} motion={reveal}>{text}</text>
     <rect x={0} y={size+25} width={225} height={8} fill={cobalt} animate={[{property:"scaleX",from:.1,to:1,at:.1,duration:.3}]}/>
    </frame>
   </frame>,{at,dur,name:name+"-title-"+at});
  };
  if (name === "looks") {
   word("UN JEAN",.03,1.77,210,80);
   p.compose(<frame width={1080} height={1920} layout="none">
    <frame x={70} y={72} width={920} height={330} layout="none" motion={entrance}>
     <text width={900} height={160} fontFamily={titleFont} fontSize={145} color={ink} motion={{...reveal,by:"character"}}>VARIOS</text>
     <text y={147} width={900} height={165} fontFamily={titleFont} fontSize={145} color={cobalt} motion={{...reveal,at:.12,from:{x:45,opacity:0}}}>LOOKS</text>
    </frame>
   </frame>,{at:1.93,dur:2.1,name:"looks-resolucion-gancho"});
   word("CAMBIÁ EL LOOK",6.97,1.95,112,95);
   word("¿CUÁL VA CON VOS?",12.25,1.7,96,105);
  } else {
   p.compose(<frame width={1080} height={1920} layout="none">
    <frame x={70} y={70} width={920} height={340} layout="none" motion={entrance}>
     <text width={900} height={155} fontFamily={titleFont} fontSize={141} color={ink} motion={reveal}>¿BUSCÁS</text>
     <text y={143} width={900} height={170} fontFamily={titleFont} fontSize={165} color={cobalt} motion={{...reveal,at:.12}}>JEANS?</text>
    </frame>
   </frame>,{at:.03,dur:2.12,name:"consulta-gancho"});
   word("TU MODELO",4.55,1.55,135,105);
   word("TU TALLE",7.3,1.55,135,105);
   word("TU CIUDAD",12.25,1.7,135,105);
  }
  // CTA sobre una toma real en movimiento. La lectura queda estable después de la entrada.
  p.compose(<frame width={1080} height={1920} layout="none">
   <frame x={70} y={65} width={850} height={500} layout="none" motion={{enter:{from:{x:-40,opacity:0},duration:.35}}}>
    <text x={0} y={0} width={790} height={50} fontFamily={infoFont} fontSize={29} fontWeight={700} letterSpacing={3} color={ink}>ÍNDIGO PY</text>
    <text x={0} y={55} width={790} height={95} fontFamily={titleFont} fontSize={80} color={ink} motion={{...reveal,duration:.3}}>ESCRIBINOS</text>
    <text x={0} y={125} width={455} height={170} fontFamily={titleFont} fontSize={144} color={cobalt} motion={{...reveal,at:.13,duration:.3}}>JEANS</text>
    <text x={0} y={270} width={415} height={55} fontFamily={infoFont} fontSize={40} fontWeight={700} color={ink} motion={{...reveal,at:.2,duration:.3}}>por WhatsApp</text>
   </frame>
  </frame>,{at:16,dur:4,name:name+"-cta-sobre-producto"});
  await p.frame(.72,root+"/"+name+"-portada.png");
  for (const [tag,time] of [["gancho",.72],["demostracion",10],["cierre",17.1]]) {
   await p.frame(time,root+"/"+name+"-"+tag+".png");
  }
 }
};

