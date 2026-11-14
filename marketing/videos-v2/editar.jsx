export default async ({project}) => {
 const root="/home/user/indigo-v2", ink="#475139", paper="#F7F4EC", font="DM Sans";
 const variants=[
  {name:"looks",cuts:[[0,10.7,3.5],[3.5,1,1.5],[5,4.15,1.45],[6.45,6,2.8],[9.25,14.2,3.35],[12.6,18,2],[14.6,21,3.6],[18.2,25.5,1.8]],
   labels:[[0,5.5,"Un jean.","Varios looks.","Ideas para combinarlo"],[5.5,6,"Cambiá el look.","Elegí tu estilo.","Combinaciones reales"],[11.5,8.5,"¿Cuál va con vos?","Elegí tu estilo.","Consultá las opciones"]]},
  {name:"consulta",cuts:[[0,1,1.5],[1.5,4.15,1.45],[2.95,10.7,6.85],[9.8,6,2.8],[12.6,18,2],[14.6,21,3.6],[18.2,25.5,1.8]],
   labels:[[0,4,"¿Buscás jeans?","Mirá estas ideas.","Combinaciones reales"],[4,8,"Contanos el modelo,","tu talle y tu ciudad.","Así empezamos tu consulta"],[12,8,"Consultá modelos","y disponibilidad.","Índigo Py · Ciudad del Este"]]}
 ];
 for(const v of variants){
  const p=await project({dir:root+"/"+v.name,size:"1080x1920",fps:30,background:paper});
  // from values below refer to the original source; clean clips are decoded trims.
  for(const [at,from,dur] of v.cuts){
   const h=await p.add(root+"/clips/clip-"+from+"-"+dur+".mp4");
   p.cut(h,{at,from:0,dur,fit:"contain"});
  }
  for(const [at,dur,t1,t2,sub] of v.labels){
   const enter=[{property:"opacity",from:0,to:1,duration:.22},{property:"offsetY",from:8,to:0,duration:.25}];
   p.compose(<frame width={1080} height={416} layout="none" background={paper}>
    <text x={84} y={94} width={840} height={52} fontFamily={font} fontSize={31} fontWeight={700} letterSpacing={3} color={ink}>ÍNDIGO PY</text>
    <text x={84} y={167} width={880} height={89} fontFamily={font} fontSize={v.name==="consulta"?64:72} fontWeight={700} color={ink} animate={enter}>{t1}</text>
    <text x={84} y={253} width={880} height={83} fontFamily={font} fontSize={60} fontWeight={700} color={ink} animate={enter}>{t2}</text>
    <text x={86} y={354} width={858} height={46} fontFamily={font} fontSize={31} color={ink}>{sub}</text>
    <rect x={84} y={408} width={164} height={5} fill={ink} animate={[{property:"scaleX",from:.25,to:1,duration:.35}]}/>
   </frame>,{at,dur,name:v.name+"-header-"+at});
  }
  p.compose(<frame width={1080} height={1920} layout="none" background={paper}>
    <text x={100} y={260} width={840} height={75} fontFamily={font} fontSize={37} fontWeight={700} letterSpacing={5} color={ink}>ÍNDIGO PY</text>
    <rect x={100} y={388} width={148} height={7} fill={ink}/>
    <frame x={100} y={530} width={850} height={242} layout="none" motion={{enter:{from:{y:14,opacity:0},duration:.3}}}>
     <text width={850} height={115} fontFamily={font} fontSize={75} fontWeight={700} color={ink}>Escribinos JEANS</text>
     <text y={122} width={850} height={100} fontFamily={font} fontSize={60} color={ink}>por WhatsApp</text>
    </frame>
    <rect x={100} y={864} width={822} height={122} fill={ink} radius={18}/>
    <text x={134} y={893} width={750} height={74} fontFamily={font} fontSize={47} fontWeight={700} color={paper}>+595 973 434 868</text>
    <text x={100} y={1080} width={820} height={66} fontFamily={font} fontSize={39} color={ink}>Modelo · talle · ciudad</text>
    <text x={100} y={1170} width={820} height={64} fontFamily={font} fontSize={34} color={ink}>Consultá las opciones disponibles.</text>
    <text x={100} y={1470} width={820} height={60} fontFamily={font} fontSize={30} color={ink}>@indigopy_ · Ciudad del Este</text>
  </frame>,{at:20,dur:4,name:v.name+"-cta"});
  await p.frame(.8,root+"/"+v.name+"-portada.png");
  await p.frame(21,root+"/"+v.name+"-cierre.png");
 }
};
