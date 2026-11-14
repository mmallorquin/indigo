export default async ({ project }) => {
  const ink = "#475139", paper = "#F7F4EC";
  const font = "DM Sans";
  const variants = [
    {name:"looks", cuts:[[0,0,3],[3,3,3],[6,6,3],[9,9,4],[13,18,3],[16,21,4]], labels:[[0,6,"Un jean.","Más de un look."],[6,7,"Cambiá la combinación.","Elegí tu estilo."],[13,7,"¿Cuál usarías vos?","Índigo Py · Ciudad del Este"]]},
    {name:"whatsapp", cuts:[[0,9,4],[4,0,4],[8,6,4],[12,18,4],[16,21,4]], labels:[[0,4,"¿Buscás jeans?","Mirá cómo se combinan."],[4,8,"Contanos qué buscás.","Modelo, talle y ciudad."],[12,8,"Consultá las opciones.","Te confirmamos disponibilidad."]]}
  ];
  for (const v of variants) {
    const p = await project({dir:"/home/user/indigo/"+v.name,size:"1080x1920",fps:30,background:paper});
    const source = await p.add("/home/user/indigo/source.mp4");
    for (const [at,from,dur] of v.cuts) p.cut(source,{at,from,dur,fit:"contain"});
    for (const [at,dur,title,sub] of v.labels) {
      p.compose(<frame width={1080} height={360} layout="none" background={paper}>
        <text x={84} y={108} width={800} height={52} fontFamily={font} fontSize={31} fontWeight={700} letterSpacing={3} color={ink}>ÍNDIGO PY</text>
        <text x={84} y={176} width={868} height={88} fontFamily={font} fontSize={62} fontWeight={700} color={ink}>{title}</text>
        <text x={86} y={282} width={860} height={50} fontFamily={font} fontSize={32} color={ink}>{sub}</text>
        <rect x={84} y={352} width={140} height={5} fill={ink}/>
      </frame>,{at,dur,name:v.name+"-header-"+at});
    }
    p.compose(<frame width={1080} height={1920} layout="none" background={paper}>
      <text x={100} y={270} width={850} height={70} fontFamily={font} fontSize={37} fontWeight={700} letterSpacing={5} color={ink}>ÍNDIGO PY</text>
      <rect x={100} y={388} width={150} height={7} fill={ink}/>
      <text x={100} y={550} width={850} height={140} fontFamily={font} fontSize={71} fontWeight={700} color={ink}>Escribinos JEANS</text>
      <text x={100} y={705} width={850} height={95} fontFamily={font} fontSize={57} color={ink}>por WhatsApp</text>
      <rect x={100} y={893} width={826} height={112} fill={ink} radius={20}/>
      <text x={132} y={916} width={762} height={70} fontFamily={font} fontSize={43} fontWeight={700} color={paper}>+595 973 434 868</text>
      <text x={100} y={1080} width={820} height={150} fontFamily={font} fontSize={37} color={ink}>Consultá modelos, talles</text>
      <text x={100} y={1140} width={820} height={60} fontFamily={font} fontSize={37} color={ink}>y disponibilidad.</text>
      <text x={100} y={1430} width={800} height={60} fontFamily={font} fontSize={30} color={ink}>@indigopy_ · Ciudad del Este</text>
    </frame>,{at:20,dur:4,name:v.name+"-cierre"});
    await p.frame(1,"/home/user/indigo/"+v.name+"-cover.png");
    await p.frame(21,"/home/user/indigo/"+v.name+"-end.png");
  }
};
