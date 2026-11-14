import {
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import {
  Page,
  Mark,
  Type,
  Photo,
  Clip,
  Note,
  Small,
  Rule,
  End,
  Music,
  C,
  ease,
} from "./Brand";

const CuellosOpening = () => {
  const f = useCurrentFrame();
  return (
    <Page dark>
      <Mark dark n="08" />
      <Type
        text="El detalle"
        y={305}
        size={116}
        serif
        italic
        color={C.cream}
        mode="track"
      />
      <Type
        text="está arriba."
        y={420}
        size={102}
        color={C.cream}
        mode="mask"
      />
      <Photo
        src="media/verde.jpg"
        x={88}
        y={615}
        w={840}
        h={840}
        reveal="circle"
        scale={1.07}
      />
      <div
        style={{
          position: "absolute",
          left: 725,
          top: 1320,
          width: 170,
          height: 170,
          border: `2px solid ${C.cream}`,
          borderRadius: "50%",
          scale: interpolate(f, [10, 45], [1.6, 1], ease),
        }}
      />
      <Note dark>Cuellos altos · una mirada de cerca</Note>
    </Page>
  );
};
const CuellosPair = () => {
  const f = useCurrentFrame();
  return (
    <Page>
      <Mark n="08" />
      <Small y={300}>DOS REFERENCIAS DE ÍNDIGO</Small>
      <Photo
        src="media/verde.jpg"
        x={86}
        y={470}
        w={525}
        h={580}
        radius={270}
        scale={1.05}
        reveal="up"
      />
      <Photo
        src="media/chocolate.jpg"
        x={460}
        y={910}
        w={468}
        h={545}
        radius={245}
        scale={1.07}
        reveal="up"
      />
      <Type
        text="verde"
        x={625}
        y={660}
        w={300}
        size={78}
        serif
        italic
        mode="letters"
      />
      <Type
        text="chocolate"
        x={85}
        y={1200}
        w={390}
        size={74}
        serif
        italic
        mode="letters"
        delay={12}
      />
      <div
        style={{
          position: "absolute",
          left: 85,
          top: 1520,
          width: 840,
          height: 3,
          background: C.olive,
          scale: `${interpolate(f, [0, 30], [0, 1], ease)} 1`,
          transformOrigin: "left",
        }}
      />
      <Note y={1570}>Inspiración de publicaciones anteriores.</Note>
    </Page>
  );
};
const CuellosClose = () => (
  <Page bg={C.sage}>
    <Mark n="08" />
    <Photo
      src="media/chocolate.jpg"
      x={90}
      y={295}
      w={838}
      h={810}
      scale={1.12}
    />
    <Type
      text="Cuello.\nTextura.\nPresencia."
      y={1140}
      size={83}
      mode="words"
    />
    <Note y={1570}>Un toque distinto para tu look.</Note>
  </Page>
);
export const Video08 = () => {
  const { fps } = useVideoConfig();
  return (
    <Page>
      <Music n="08" />
      <Sequence
        name="Gancho: detalle de cuello"
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <CuellosOpening />
      </Sequence>
      <Sequence
        name="Díptico diagonal verde y chocolate"
        from={4 * fps}
        durationInFrames={6 * fps}
        premountFor={fps}
      >
        <CuellosPair />
      </Sequence>
      <Sequence
        name="Detalle acanalado"
        from={10 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <CuellosClose />
      </Sequence>
      <Sequence
        name="Consulta cuellos"
        from={14 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <End cta="Consultá por" keyword="cuellos altos" number="08" dark />
      </Sequence>
    </Page>
  );
};

const PaletaOpening = () => {
  const f = useCurrentFrame();
  return (
    <Page bg={C.olive}>
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: 540,
          height: 1920,
          background: C.deep,
          translate: `${interpolate(f, [0, 30], [-300, 0], ease)}px 0`,
        }}
      />
      <Mark dark n="09" />
      <Type
        text="Azul"
        x={88}
        y={400}
        size={180}
        serif
        italic
        color={C.cream}
        mode="mask"
      />
      <Type
        text="+ crema"
        x={215}
        y={630}
        size={160}
        serif
        italic
        color={C.cream}
        mode="mask"
        delay={6}
      />
      <Photo
        src="media/azul-crema.jpg"
        x={366}
        y={945}
        w={562}
        h={580}
        reveal="up"
        scale={1.04}
      />
      <div
        style={{
          position: "absolute",
          left: 88,
          top: 980,
          fontSize: 170,
          color: C.cream,
          fontFamily: "Cormorant",
        }}
      >
        +
      </div>
    </Page>
  );
};
const PaletaPortrait = () => (
  <Page>
    <Mark n="09" />
    <Photo
      src="media/azul-crema.jpg"
      x={85}
      y={325}
      w={845}
      h={970}
      fit="contain"
      scale={1.02}
    />
    <Type
      text="Una idea para\ncombinar tonos."
      y={1330}
      size={78}
      mode="words"
    />
    <Rule y={1530} />
    <Note y={1570}>Inspiración de un look de Índigo.</Note>
  </Page>
);
const PaletaDetails = () => {
  const f = useCurrentFrame();
  return (
    <Page dark>
      <Mark dark n="09" />
      <Type
        text="Que el color\nconverse."
        y={300}
        size={101}
        color={C.cream}
        mode="track"
      />
      <Photo
        src="media/azul-crema.jpg"
        x={88}
        y={650}
        w={490}
        h={755}
        position="48% 65%"
        scale={1.09}
      />
      <div
        style={{
          position: "absolute",
          left: 626,
          top: 652,
          width: 292,
          height: 330,
          background: "#243B65",
          clipPath: `inset(0 0 ${interpolate(f, [0, 25], [100, 0], ease)}% 0)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 626,
          top: 1010,
          width: 292,
          height: 395,
          background: "#DDD5C7",
          clipPath: `inset(0 0 ${interpolate(f, [5, 30], [100, 0], ease)}% 0)`,
        }}
      />
      <Small x={657} y={735} w={210} color={C.cream}>
        AZUL
      </Small>
      <Small x={650} y={1170} w={210} color={C.ink}>
        CREMA
      </Small>
      <Note dark>Paleta de inspiración · tonos aproximados</Note>
    </Page>
  );
};
export const Video09 = () => {
  const { fps } = useVideoConfig();
  return (
    <Page>
      <Music n="09" />
      <Sequence
        name="Apertura bicolor"
        durationInFrames={3 * fps}
        premountFor={fps}
      >
        <PaletaOpening />
      </Sequence>
      <Sequence
        name="Look azul y crema"
        from={3 * fps}
        durationInFrames={6 * fps}
        premountFor={fps}
      >
        <PaletaPortrait />
      </Sequence>
      <Sequence
        name="Muestras cromáticas"
        from={9 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <PaletaDetails />
      </Sequence>
      <Sequence
        name="Consulta combinación"
        from={14 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <End cta="Escribinos por" keyword="azul + crema" number="09" />
      </Sequence>
    </Page>
  );
};

const JeansOpening = () => {
  const f = useCurrentFrame();
  return (
    <Page bg={C.deep}>
      <Mark dark n="10" />
      <Photo
        src="media/jean-detalle.jpg"
        x={88}
        y={600}
        w={835}
        h={800}
        reveal="left"
        scale={1.04}
      />
      <Type
        text="Antes de\nelegir tu jean…"
        y={300}
        size={94}
        color={C.cream}
        mode="letters"
      />
      <div
        style={{
          position: "absolute",
          top: 1440,
          left: 88,
          width: 835,
          height: 74,
          background: C.sage,
          scale: `${interpolate(f, [10, 40], [0, 1], ease)} 1`,
          transformOrigin: "left",
        }}
      />
      <Small y={1461} color={C.ink}>
        MIRÁ LOS DETALLES
      </Small>
    </Page>
  );
};
const JeansLook = () => (
  <Page>
    <Mark n="10" />
    <Small y={305}>01 / LA PRENDA</Small>
    <Clip
      src="media/jean-percha.mp4"
      x={88}
      y={435}
      w={835}
      h={890}
      start={3.3}
    />
    <Type text="De cerca." y={1390} size={113} serif italic mode="track" />
  </Page>
);
const JeansDetail = () => (
  <Page dark>
    <Mark dark n="10" />
    <Small y={305} color={C.sage}>
      02 / LOS DETALLES
    </Small>
    <Photo
      src="media/jean-detalle.jpg"
      x={88}
      y={500}
      w={625}
      h={880}
      fit="cover"
      scale={1.12}
    />
    <div
      style={{
        position: "absolute",
        left: 750,
        top: 500,
        height: 880,
        width: 175,
        border: `2px solid ${C.sage}`,
      }}
    />
    <div
      style={{
        position: "absolute",
        left: 762,
        top: 1180,
        rotate: "-90deg",
        transformOrigin: "left top",
        whiteSpace: "nowrap",
        fontSize: 64,
        letterSpacing: 7,
        color: C.cream,
      }}
    >
      MIRÁ LA COSTURA
    </div>
    <Type
      text="Elegí con más\ninformación."
      y={1425}
      size={67}
      color={C.cream}
      mode="mask"
    />
  </Page>
);
const JeansQuestion = () => (
  <Page bg={C.sage}>
    <Mark n="10" />
    <Small y={320}>03 / ANTES DE DECIDIR</Small>
    <Type text="Modelo.\nTalle.\nMedidas." y={600} size={130} mode="words" />
    <Rule y={1160} />
    <Type
      text="Tené esas preguntas\na mano."
      y={1270}
      size={76}
      serif
      italic
      mode="mask"
    />
  </Page>
);
export const Video10 = () => {
  const { fps } = useVideoConfig();
  return (
    <Page>
      <Music n="10" />
      <Sequence
        name="Hook detalle jean"
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <JeansOpening />
      </Sequence>
      <Sequence
        name="Jean en percha"
        from={4 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <JeansLook />
      </Sequence>
      <Sequence
        name="Detalle real de costura"
        from={8 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <JeansDetail />
      </Sequence>
      <Sequence
        name="Preguntas útiles"
        from={12 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <JeansQuestion />
      </Sequence>
      <Sequence
        name="Consulta jeans"
        from={16 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <End cta="Consultá por" keyword="jeans" number="10" dark />
      </Sequence>
    </Page>
  );
};
