import {
  Composition,
  Sequence,
  useVideoConfig,
  useCurrentFrame,
  interpolate,
} from "remotion";
import {
  Stage,
  Type,
  Photo,
  Label,
  Foot,
  Line,
  Arrow,
  EndCard,
  TitleCard,
  Sound,
  P,
  ease,
} from "./Design";

const Hook11 = () => (
  <Stage n="11" dark>
    <Type
      text="¿Por dónde\nempezás?"
      y={330}
      size={119}
      color={P.paper}
      mode="words"
    />
    <Photo src="conjunto-uva.jpg" x={146} y={675} w={620} h={835} tilt={-3} />
    <Photo
      src="conjunto-beige.jpg"
      x={712}
      y={1020}
      w={216}
      h={410}
      delay={7}
      tilt={5}
    />
  </Stage>
);
const Beige = () => (
  <Stage n="11">
    <Label>UNA REFERENCIA</Label>
    <Type text="Beige + negro" y={365} size={96} serif mode="track" />
    <Photo src="conjunto-beige.jpg" x={88} y={590} w={558} h={865} />
    <Label x={705} y={745} w={220}>
      BASE
    </Label>
    <Type text="beige" x={700} y={810} w={225} size={74} serif italic />
    <Label x={705} y={1050} w={220}>
      TONO
    </Label>
    <Type
      text="negro"
      x={700}
      y={1115}
      w={225}
      size={74}
      serif
      italic
      delay={12}
    />
    <Line y={1510} />
    <Foot>Un punto de partida para tu combinación.</Foot>
  </Stage>
);
const Vino = () => {
  const f = useCurrentFrame();
  return (
    <Stage n="11" dark>
      <Type
        text="Un tono.\nOtro acento."
        y={300}
        size={102}
        color={P.paper}
        mode="mask"
      />
      <Photo src="conjunto-uva.jpg" x={240} y={595} w={630} h={860} />
      <div
        style={{
          position: "absolute",
          left: 86,
          top: 730,
          width: 90,
          height: 600,
          border: "2px solid #C4AB79",
          scale: `1 ${interpolate(f, [0, 30], [0, 1], ease)}`,
          transformOrigin: "top",
        }}
      />
      <Label dark y={1535} size={41}>
        VINO + VIOLETA
      </Label>
    </Stage>
  );
};
const Marron = () => (
  <Stage n="11">
    <Photo src="conjunto-marron.jpg" x={148} y={335} w={720} h={1000} />
    <Type
      text="En la misma\nfamilia de tonos."
      y={1375}
      size={74}
      serif
      italic
      mode="words"
    />
    <Foot y={1580}>Marrón + marrón · referencia del perfil</Foot>
  </Stage>
);
const Trio = () => {
  const f = useCurrentFrame();
  return (
    <Stage n="11">
      <Label>PARA PENSAR TU LOOK</Label>
      <Type
        text="Primero la base.\nDespués el tono."
        y={370}
        size={88}
        mode="words"
      />
      <div
        style={{
          position: "absolute",
          left: 860,
          top: 291,
          font: "600 70px Cormorant",
          color: P.olive,
        }}
      >
        {Math.min(3, Math.floor(f / 12) + 1)}
      </div>
      <Photo src="conjunto-beige.jpg" x={88} y={655} w={258} h={630} />
      <Photo src="conjunto-uva.jpg" x={379} y={655} w={258} h={630} delay={9} />
      <Photo
        src="conjunto-marron.jpg"
        x={670}
        y={655}
        w={258}
        h={630}
        delay={18}
      />
      <Type text="Beige\n+ negro" x={88} y={1310} w={258} size={42} />
      <Type
        text="Vino\n+ violeta"
        x={379}
        y={1310}
        w={258}
        size={42}
        delay={9}
      />
      <Type
        text="Marrón\n+ marrón"
        x={670}
        y={1310}
        w={258}
        size={42}
        delay={18}
      />
      <Arrow y={1450} />
      <Foot y={1600}>Inspiración de publicaciones anteriores.</Foot>
    </Stage>
  );
};
export const V11 = () => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Sound a="03" b="07" n="11" />
      <Sequence
        name="Gancho: por dónde empezar"
        durationInFrames={3 * fps}
        premountFor={fps}
      >
        <Hook11 />
      </Sequence>
      <Sequence
        name="Título editorial"
        from={3 * fps}
        durationInFrames={1.5 * fps}
        premountFor={fps}
      >
        <TitleCard
          n="11"
          title="Una base.\nTres ideas."
          subtitle="Combinaciones de nuestro perfil."
        />
      </Sequence>
      <Sequence
        name="Referencia beige y negro"
        from={4.5 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <Beige />
      </Sequence>
      <Sequence
        name="Referencia vino y violeta"
        from={9.5 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <Vino />
      </Sequence>
      <Sequence
        name="Referencia marrón"
        from={14.5 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <Marron />
      </Sequence>
      <Sequence
        name="Resumen y diagrama"
        from={19.5 * fps}
        durationInFrames={6 * fps}
        premountFor={fps}
      >
        <Trio />
      </Sequence>
      <Sequence
        name="CTA comentario"
        from={25.5 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <EndCard n="11" cta="Comentá cuál combinación\nquerés ver de cerca." />
      </Sequence>
    </>
  );
};

const Hook12 = () => (
  <Stage n="12">
    <Type
      text="Mirá más\nque el color."
      y={340}
      size={119}
      serif
      italic
      mode="mask"
    />
    <Photo
      src="blusa.jpg"
      x={88}
      y={710}
      w={840}
      h={785}
      position="50% 80%"
      zoom={1.35}
    />
    <Label y={1560}>UNA MIRADA A LA PRENDA</Label>
  </Stage>
);
const Cuello = () => (
  <Stage n="12" dark>
    <Label dark>01 / EL CUELLO</Label>
    <Type
      text="Dos referencias\nde cuello alto."
      y={370}
      size={92}
      color={P.paper}
      mode="letters"
    />
    <Photo src="verde.jpg" x={88} y={750} w={395} h={650} position="50% 50%" />
    <Photo src="chocolate.jpg" x={531} y={750} w={395} h={650} delay={12} />
    <Line y={1460} />
    <Foot dark y={1530}>
      Verde y chocolate · mirá el diseño del cuello.
    </Foot>
  </Stage>
);
const Mangas = () => {
  const f = useCurrentFrame();
  return (
    <Stage n="12">
      <Label>02 / LAS MANGAS</Label>
      <Type text="Una referencia\nsin mangas." y={370} size={96} mode="words" />
      <Photo src="blusa.jpg" x={88} y={655} w={600} h={835} />
      <div
        style={{
          position: "absolute",
          left: 746,
          top: 860,
          fontFamily: "Cormorant",
          fontSize: 124,
          color: P.olive,
          translate: `0 ${interpolate(f, [0, 24], [30, 0], ease)}px`,
        }}
      >
        02
      </div>
      <Label x={748} y={1050} w={185} size={37}>
        MIRÁ
        <br />
        EL
        <br />
        CORTE
      </Label>
      <Foot>Observá cómo se ve la prenda completa.</Foot>
    </Stage>
  );
};
const Fruncido = () => {
  const f = useCurrentFrame();
  return (
    <Stage n="12" dark>
      <Label dark>03 / LOS DETALLES</Label>
      <Type
        text="El fruncido,\nde cerca."
        y={370}
        size={102}
        serif
        italic
        color={P.paper}
        mode="track"
      />
      <Photo
        src="blusa.jpg"
        x={88}
        y={685}
        w={840}
        h={740}
        position="50% 86%"
        zoom={1.65}
      />
      <svg
        width="840"
        height="100"
        style={{ position: "absolute", left: 88, top: 1400 }}
      >
        <path
          d="M 130 3 V 50 H 580"
          fill="none"
          stroke={P.accent}
          strokeWidth="3"
          strokeDasharray={497}
          strokeDashoffset={interpolate(f, [20, 65], [497, 0], ease)}
        />
        <circle cx="130" cy="3" r="7" fill={P.accent} />
        <text
          x="610"
          y="63"
          fill={P.paper}
          fontFamily="Inter"
          fontSize="32"
          fontWeight="700"
        >
          DETALLE
        </text>
      </svg>
      <Foot dark y={1580}>
        Acercamiento a una foto real de la prenda.
      </Foot>
    </Stage>
  );
};
const Checklist = () => {
  const f = useCurrentFrame();
  return (
    <Stage n="12">
      <Type
        text="De la foto general\na los detalles."
        y={335}
        size={90}
        serif
        mode="mask"
      />
      <Photo src="blusa.jpg" x={88} y={650} w={425} h={820} />
      <div style={{ position: "absolute", left: 590, top: 750, width: 340 }}>
        {["Cuello", "Mangas", "Detalles"].map((s, i) => (
          <div
            key={s}
            style={{
              fontSize: 57,
              fontWeight: 700,
              lineHeight: 1.4,
              padding: "34px 0",
              borderBottom: "2px solid #CBD0B2",
              opacity: interpolate(f, [i * 19, i * 19 + 14], [0, 1], ease),
              translate: `0 ${interpolate(f, [i * 19, i * 19 + 21], [30, 0], ease)}px`,
            }}
          >
            {s}
          </div>
        ))}
      </div>
      <Foot y={1580}>
        Referencias anteriores para mirar con más información.
      </Foot>
    </Stage>
  );
};
export const V12 = () => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Sound a="05" b="08" n="12" />
      <Sequence
        name="Gancho de detalle"
        durationInFrames={3 * fps}
        premountFor={fps}
      >
        <Hook12 />
      </Sequence>
      <Sequence
        name="Título editorial"
        from={3 * fps}
        durationInFrames={1.5 * fps}
        premountFor={fps}
      >
        <TitleCard
          n="12"
          title="Tres cosas\npara mirar."
          subtitle="Cuello, mangas y detalles visibles."
        />
      </Sequence>
      <Sequence
        name="Diseño de cuellos"
        from={4.5 * fps}
        durationInFrames={5.5 * fps}
        premountFor={fps}
      >
        <Cuello />
      </Sequence>
      <Sequence
        name="Blusa sin mangas"
        from={10 * fps}
        durationInFrames={5.5 * fps}
        premountFor={fps}
      >
        <Mangas />
      </Sequence>
      <Sequence
        name="Acercamiento fruncido"
        from={15.5 * fps}
        durationInFrames={5.5 * fps}
        premountFor={fps}
      >
        <Fruncido />
      </Sequence>
      <Sequence
        name="Checklist revelado"
        from={21 * fps}
        durationInFrames={4.5 * fps}
        premountFor={fps}
      >
        <Checklist />
      </Sequence>
      <Sequence
        name="CTA comentario"
        from={25.5 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <EndCard n="12" cta="Comentá qué detalle\nquerés ver de cerca." />
      </Sequence>
    </>
  );
};

const Hook13 = () => (
  <Stage n="13" dark>
    <Type
      text="Una capa.\nOtra idea."
      y={345}
      size={134}
      color={P.paper}
      mode="letters"
    />
    <Photo
      src="chaleco-a.jpg"
      x={88}
      y={770}
      w={840}
      h={740}
      position="50% 66%"
      zoom={1.18}
    />
  </Stage>
);
const Chaleco = () => {
  const f = useCurrentFrame();
  return (
    <Stage n="13">
      <Label>IDEA PARA COMBINAR</Label>
      <Type
        text="Camisa\n+ chaleco"
        y={390}
        size={139}
        serif
        italic
        mode="mask"
      />
      <Photo src="chaleco-a.jpg" x={450} y={850} w={478} h={650} />
      <svg
        width="320"
        height="380"
        viewBox="0 0 320 380"
        style={{ position: "absolute", left: 88, top: 900 }}
      >
        <path
          d="M 115 45 L 55 85 L 15 190 L 70 210 L 95 148 L 95 335 L 245 335 L 245 148 L 270 210 L 305 190 L 280 85 L 215 45 L 175 93 Z"
          fill="none"
          stroke={P.olive}
          strokeWidth="3"
          strokeDasharray={1264.58434}
          strokeDashoffset={interpolate(f, [0, 65], [1264.58434, 0], ease)}
        />
        <path
          d="M 115 45 L 175 93 L 215 45 M 175 93 V 335"
          fill="none"
          stroke={P.accent}
          strokeWidth="3"
        />
      </svg>
      <Foot y={1580}>Diagrama de una idea · chalecos reales del perfil</Foot>
    </Stage>
  );
};
const AzulCrema = () => (
  <Stage n="13" dark>
    <Label dark>OTRA REFERENCIA</Label>
    <Type
      text="Azul + crema"
      y={375}
      size={112}
      serif
      italic
      color={P.paper}
      mode="track"
    />
    <Photo src="azul-crema.jpg" x={158} y={620} w={720} h={950} />
  </Stage>
);
const DosCapas = () => (
  <Stage n="13">
    <Type
      text="Dos ideas para\nmirar las capas."
      y={340}
      size={92}
      mode="words"
    />
    <Photo src="chaleco-a.jpg" x={88} y={685} w={395} h={710} />
    <Photo src="azul-crema.jpg" x={531} y={685} w={395} h={710} delay={12} />
    <Type text="Chaleco" x={88} y={1430} w={395} size={55} serif />
    <Type
      text="Capa crema"
      x={531}
      y={1430}
      w={395}
      size={55}
      serif
      delay={12}
    />
    <Foot y={1600}>Inspiración de publicaciones anteriores.</Foot>
  </Stage>
);
const Steps = () => {
  const f = useCurrentFrame();
  return (
    <Stage n="13" dark>
      <Label dark>PARA TU PRÓXIMA COMBINACIÓN</Label>
      <Type
        text="Mirá el look\npor partes."
        y={405}
        size={122}
        serif
        color={P.paper}
        mode="mask"
      />
      <svg
        width="120"
        height="670"
        style={{ position: "absolute", left: 88, top: 770 }}
      >
        <path
          d="M 55 30 V 610"
          stroke={P.accent}
          strokeWidth="3"
          fill="none"
          strokeDasharray={580}
          strokeDashoffset={interpolate(f, [0, 60], [580, 0], ease)}
        />
        {[30, 310, 610].map((y, i) => (
          <circle
            key={y}
            cx="55"
            cy={y}
            r="12"
            fill={P.accent}
            opacity={interpolate(f, [i * 20, i * 20 + 10], [0, 1], ease)}
          />
        ))}
      </svg>
      <Type
        text="Base"
        x={255}
        y={780}
        size={104}
        color={P.paper}
        mode="letters"
      />
      <Type
        text="Capa"
        x={255}
        y={1060}
        size={104}
        color={P.paper}
        mode="letters"
        delay={20}
      />
      <Type
        text="Tonos"
        x={255}
        y={1360}
        size={104}
        color={P.paper}
        mode="letters"
        delay={40}
      />
    </Stage>
  );
};
export const V13 = () => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Sound a="09" b="02" n="13" />
      <Sequence
        name="Gancho de capas"
        durationInFrames={3 * fps}
        premountFor={fps}
      >
        <Hook13 />
      </Sequence>
      <Sequence
        name="Título editorial"
        from={3 * fps}
        durationInFrames={1.5 * fps}
        premountFor={fps}
      >
        <TitleCard
          n="13"
          title="El look\npor capas."
          subtitle="Dos referencias, dos ideas distintas."
        />
      </Sequence>
      <Sequence
        name="Idea de camisa y chaleco"
        from={4.5 * fps}
        durationInFrames={6 * fps}
        premountFor={fps}
      >
        <Chaleco />
      </Sequence>
      <Sequence
        name="Look real azul y crema"
        from={10.5 * fps}
        durationInFrames={6 * fps}
        premountFor={fps}
      >
        <AzulCrema />
      </Sequence>
      <Sequence
        name="Comparación de referencias"
        from={16.5 * fps}
        durationInFrames={6 * fps}
        premountFor={fps}
      >
        <DosCapas />
      </Sequence>
      <Sequence
        name="Diagrama de partes"
        from={22.5 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <Steps />
      </Sequence>
      <Sequence
        name="CTA comentario"
        from={26.5 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <EndCard
          n="13"
          cta="Comentá qué combinación\nquerés en el próximo video."
        />
      </Sequence>
    </>
  );
};
export const RemotionRoot = () => (
  <>
    <Composition
      id="11-Combinaciones"
      component={V11}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={915}
    />
    <Composition
      id="12-Detalles"
      component={V12}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={915}
    />
    <Composition
      id="13-Capas"
      component={V13}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={945}
    />
  </>
);
