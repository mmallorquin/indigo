export default async ({project}) => {
 const root = process.env.INDIGO_ROOT || "/home/user/indigo-v4";
 const olive = "#414D31", cream = "#F5F0E6";
 for (const name of ["editorial", "energia"]) {
  const display = name === "editorial" ? "Playfair Display" : "Anton";
  const p = await project({dir:root+"/"+name,size:"1080x1920",fps:30,background:cream});
  const base = await p.add(root+"/montaje-base.mp4");
  p.cut(base,{at:0,from:0,dur:20,fit:"contain"});
  const title = (text,at,dur,size) => {
   const soft = name === "editorial";
   p.compose(<frame width={1080} height={1920} layout="none">
    <frame x={96} y={220} width={888} height={173} layout="none" clip={true}
      reveal={{from:soft?"bottom":"left",duration:soft?.5:.35,easing:"ease-out"}}
      motion={{exit:{to:{y:soft?-14:-24,opacity:0},duration:soft?.2:.18,anchor:"end"}}}>
     <text x={0} y={0} width={872} height={158} fontFamily={display} fontSize={size} color={olive}
       motion={{by:"word",from:{y:soft?20:0,x:soft?0:28,opacity:0},duration:soft?.42:.3,overlap:.55,easing:"house"}}>{text}</text>
     <rect x={0} y={160} width={soft?80:210} height={soft?2:5} fill={olive}
       animate={[{property:"scaleX",from:.05,to:1,at:.1,duration:soft?.4:.28,easing:"ease-out"}]}/>
    </frame>
   </frame>,{at,dur,name:name+"-titulo-"+at});
  };
  if (name === "editorial") {
   title("Un jean.",.1,1.7,132);
   title("Varios looks.",2,2.1,90);
   title("Cambiá el look.",6,1.9,77);
   title("¿Cuál va con vos?",14,1.65,70);
  } else {
   title("¿BUSCÁS JEANS?",.1,1.7,103);
   title("TU ESTILO",2,1.8,110);
   title("TU MODELO",6,1.8,110);
   title("TU TALLE",9,1.8,110);
   title("TU CIUDAD",13,1.8,110);
  }
  p.compose(<frame width={1080} height={1920} layout="none">
   <frame x={96} y={235} width={800} height={340} layout="none"
     motion={{enter:{from:{x:name==="editorial"?0:-28,y:name==="editorial"?20:0,opacity:0},duration:.38}}}>
    <text x={0} y={0} width={740} height={42} fontFamily="DM Sans" fontSize={24} fontWeight={700} letterSpacing={3} color={olive}>ÍNDIGO PY</text>
    <text x={0} y={45} width={720} height={75} fontFamily="DM Sans" fontSize={56} fontWeight={700} color={olive}>Escribinos</text>
    <frame x={0} y={118} width={460} height={140} layout="none" clip={true}
     reveal={{from:"left",at:.1,duration:.35,easing:"ease-out"}}>
     <text x={0} y={0} width={460} height={138} fontFamily={display} fontSize={name==="editorial"?94:116} color={cream}>JEANS</text>
    </frame>
    <text x={0} y={260} width={450} height={64} fontFamily="DM Sans" fontSize={42} fontWeight={700} color={cream}>por WhatsApp</text>
   </frame>
  </frame>,{at:16,dur:4,name:name+"-cta"});
  for (const [tag,time] of [["gancho",.9],["demostracion",8.5],["cierre",17.4]]) {
   await p.frame(time,root+"/"+name+"-"+tag+".png");
  }
  await p.frame(.9,root+"/"+name+"-portada.png");
 }
};
