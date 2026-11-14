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

const ConsultaHook = () => {
  const f = useCurrentFrame();
  return (
    <Page dark>
      <Mark dark n="01" />
      <Type
        text="¿Viste algo\nque te gustó?"
        y={325}
        size={105}
        color={C.cream}
        mode="words"
      />
      <Photo
        src="media/conjunto-uva.jpg"
        x={88}
        y={690}
        w={485}
        h={720}
        rotate={-5}
        border
        reveal="up"
      />
      <Photo
        src="media/blusa.jpg"
        x={536}
        y={872}
        w={382}
        h={510}
        rotate={7}
        border
        reveal="left"
      />
      <div
        style={{
          position: "absolute",
          left: 680,
          top: 665,
          width: 135,
          height: 135,
          border: `3px solid ${C.cream}`,
          borderRadius: "50%",
          scale: interpolate(f, [0, 25], [0.2, 1], ease),
          fontSize: 78,
          textAlign: "center",
          lineHeight: "122px",
          color: C.cream,
        }}
      >
        +
      </div>
      <Note dark>Tu próxima consulta empieza por una prenda.</Note>
    </Page>
  );
};
const ConsultaSteps = () => {
  const f = useCurrentFrame();
  return (
    <Page>
      <Mark n="01" />
      <Small y={300}>PARA HACER TU CONSULTA</Small>
      <Type text="Con estos\ndos datos." y={430} size={105} mode="mask" />
      <div
        style={{
          position: "absolute",
          left: 88,
          top: 810,
          width: 840,
          height: 250,
          borderTop: `2px solid ${C.olive}`,
          borderBottom: `2px solid ${C.olive}`,
          translate: `${interpolate(f, [5, 30], [200, 0], ease)}px 0`,
        }}
      >
        <Small x={25} y={37} color={C.olive}>
          01
        </Small>
        <Type
          text="La foto"
          x={150}
          y={49}
          w={660}
          size={100}
          serif
          italic
          mode="words"
          delay={5}
        />
      </div>
      <div
        style={{
          position: "absolute",
          left: 88,
          top: 1085,
          width: 840,
          height: 250,
          borderBottom: `2px solid ${C.olive}`,
          translate: `${interpolate(f, [15, 40], [200, 0], ease)}px 0`,
        }}
      >
        <Small x={25} y={37}>
          02
        </Small>
        <Type
          text="Tu talle"
          x={150}
          y={49}
          w={660}
          size={100}
          serif
          italic
          mode="words"
          delay={15}
        />
      </div>
      <Note>Así podemos identificar qué prenda te gustó.</Note>
    </Page>
  );
};
const ConsultaMensaje = () => (
  <Page bg={C.sage}>
    <Mark n="01" />
    <Small y={310}>UNA CONSULTA SIMPLE</Small>
    <Type
      text="“Hola, me gustó\nesta prenda.\n¿Hay en mi talle?”"
      y={520}
      size={92}
      serif
      italic
      mode="words"
    />
    <Photo
      src="media/blusa.jpg"
      x={630}
      y={1110}
      w={280}
      h={350}
      radius={140}
    />
    <Rule y={1490} />
    <Note y={1550}>Disponibilidad y precio se confirman al consultar.</Note>
  </Page>
);
export const Video01 = () => {
  const { fps } = useVideoConfig();
  return (
    <Page>
      <Music n="01" />
      <Sequence
        name="Gancho collage de prendas"
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <ConsultaHook />
      </Sequence>
      <Sequence
        name="Dos datos para consultar"
        from={4 * fps}
        durationInFrames={6 * fps}
        premountFor={fps}
      >
        <ConsultaSteps />
      </Sequence>
      <Sequence
        name="Ejemplo de consulta"
        from={10 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <ConsultaMensaje />
      </Sequence>
      <Sequence
        name="CTA único"
        from={15 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <End cta="Mandanos la foto" keyword="y tu talle" number="01" dark />
      </Sequence>
    </Page>
  );
};

const ChalecoHook = () => {
  const f = useCurrentFrame();
  return (
    <Page bg={C.sage}>
      <Mark n="02" />
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 400,
          width: 1080,
          height: 165,
          background: C.olive,
          translate: `${interpolate(f, [0, 25], [-1080, 0], ease)}px 0`,
        }}
      />
      <Type
        text="Sumá una capa."
        y={400}
        x={86}
        size={92}
        color={C.cream}
        mode="mask"
      />
      <Photo
        src="media/chaleco-a.jpg"
        x={156}
        y={650}
        w={712}
        h={810}
        reveal="up"
        scale={1.04}
      />
      <Note>Chalecos para pensar otras combinaciones.</Note>
    </Page>
  );
};
const ChalecoPanels = () => {
  const f = useCurrentFrame();
  return (
    <Page dark>
      <Mark dark n="02" />
      <Type
        text="El chaleco,\nprotagonista."
        y={315}
        size={91}
        color={C.cream}
        mode="track"
      />
      <Photo
        src="media/chaleco-a.jpg"
        x={88}
        y={620}
        w={400}
        h={750}
        fit="cover"
        position="30% 50%"
        scale={1.07}
      />
      <Photo
        src="media/chaleco-b.jpg"
        x={530}
        y={740}
        w={395}
        h={750}
        fit="cover"
        position="70% 55%"
        zoom={1.45}
        scale={1.05}
        reveal="up"
      />
      <div
        style={{
          position: "absolute",
          left: 89,
          top: 1440,
          width: 395,
          height: 3,
          background: C.sage,
          scale: `${interpolate(f, [0, 35], [0, 1], ease)} 1`,
          transformOrigin: "left",
        }}
      />
      <Note dark>Distintos diseños, una misma idea: combinar.</Note>
    </Page>
  );
};
const ChalecoIdea = () => (
  <Page>
    <Mark n="02" />
    <Small y={300}>IDEA PARA TU LOOK</Small>
    <Type
      text="Camisa\n+ chaleco"
      y={455}
      size={125}
      serif
      italic
      mode="letters"
    />
    <div
      style={{
        position: "absolute",
        left: 84,
        top: 790,
        fontSize: 190,
        color: C.olive,
      }}
    >
      +
    </div>
    <Photo
      src="media/chaleco-b.jpg"
      x={345}
      y={820}
      w={580}
      h={630}
      radius={290}
      scale={1.06}
    />
    <Note y={1540}>Una combinación sugerida por Índigo.</Note>
  </Page>
);
export const Video02 = () => {
  const { fps } = useVideoConfig();
  return (
    <Page>
      <Music n="02" />
      <Sequence
        name="Franja y revelado vertical"
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <ChalecoHook />
      </Sequence>
      <Sequence
        name="Dos vistas de chalecos"
        from={4 * fps}
        durationInFrames={6 * fps}
        premountFor={fps}
      >
        <ChalecoPanels />
      </Sequence>
      <Sequence
        name="Idea camisa más chaleco"
        from={10 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <ChalecoIdea />
      </Sequence>
      <Sequence
        name="Consulta chalecos"
        from={14 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <End cta="Preguntanos por" keyword="chalecos" number="02" />
      </Sequence>
    </Page>
  );
};

const BasicaHook = () => {
  const f = useCurrentFrame();
  return (
    <Page>
      <Mark n="03" />
      <Photo
        src="media/basica-beige.jpg"
        x={88}
        y={370}
        w={840}
        h={900}
        scale={1.04}
        reveal="left"
      />
      <div
        style={{
          position: "absolute",
          left: 88,
          top: 1240,
          width: 840,
          height: 295,
          background: C.olive,
          translate: `0 ${interpolate(f, [0, 30], [180, 0], ease)}px`,
        }}
      />
      <Type
        text="Una buena\nbase."
        x={120}
        y={1290}
        w={760}
        size={103}
        color={C.cream}
        mode="mask"
      />
    </Page>
  );
};
const BasicaStructure = () => {
  const f = useCurrentFrame();
  return (
    <Page bg={C.sage}>
      <Mark n="03" />
      <Small y={300}>EMPEZÁ POR LO SIMPLE</Small>
      <Type text="Básica" y={440} size={178} serif mode="track" />
      <div
        style={{
          position: "absolute",
          left: 90,
          top: 678,
          width: 840,
          height: 3,
          background: C.olive,
          scale: `${interpolate(f, [0, 30], [0, 1], ease)} 1`,
          transformOrigin: "left",
        }}
      />
      <Photo
        src="media/basica-beige.jpg"
        x={90}
        y={770}
        w={430}
        h={650}
        position="50% 50%"
        scale={1.13}
      />
      <Type
        text="+\nTu\nestilo"
        x={575}
        y={820}
        w={350}
        size={112}
        mode="words"
      />
      <Note>Un punto de partida para tu combinación.</Note>
    </Page>
  );
};
const BasicaLook = () => (
  <Page dark>
    <Mark dark n="03" />
    <Photo
      src="media/conjunto-beige.jpg"
      x={200}
      y={300}
      w={625}
      h={1000}
      fit="contain"
      scale={1.01}
    />
    <Type
      text="Otra idea\npara combinar."
      y={1330}
      size={88}
      color={C.cream}
      serif
      italic
      mode="mask"
    />
    <Note dark y={1590}>
      Inspiración de publicaciones anteriores.
    </Note>
  </Page>
);
export const Video03 = () => {
  const { fps } = useVideoConfig();
  return (
    <Page>
      <Music n="03" />
      <Sequence
        name="Básica primer plano"
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <BasicaHook />
      </Sequence>
      <Sequence
        name="Fórmula modular"
        from={4 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <BasicaStructure />
      </Sequence>
      <Sequence
        name="Básica combinada"
        from={9 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <BasicaLook />
      </Sequence>
      <Sequence
        name="Consulta básicas"
        from={14 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <End cta="Consultá por" keyword="básicas" number="03" dark />
      </Sequence>
    </Page>
  );
};

const MangasHook = () => {
  const f = useCurrentFrame();
  return (
    <Page dark>
      <Mark dark n="04" />
      <Type text="Mangas" y={305} size={140} color={C.cream} mode="letters" />
      <Type
        text="largas."
        x={233}
        y={458}
        w={696}
        size={160}
        color={C.sage}
        serif
        italic
        mode="track"
      />
      <Photo
        src="media/mangas.jpg"
        x={88}
        y={755}
        w={840}
        h={710}
        scale={1.04}
        reveal="left"
      />
      <div
        style={{
          position: "absolute",
          left: 86,
          top: 660,
          height: 4,
          width: 842,
          background: C.cream,
          scale: `${interpolate(f, [0, 30], [0, 1], ease)} 1`,
          transformOrigin: "left",
        }}
      />
      <Note dark>Otra forma de empezar tu look.</Note>
    </Page>
  );
};
const MangasGreen = () => (
  <Page>
    <Mark n="04" />
    <Small y={300}>EN UN LOOK REAL</Small>
    <Clip
      src="media/manga-verde.mp4"
      x={150}
      y={420}
      w={720}
      h={920}
      fit="contain"
    />
    <Type
      text="Un toque\nde verde."
      y={1380}
      size={84}
      serif
      italic
      mode="mask"
    />
  </Page>
);
const MangasLilac = () => (
  <Page bg={C.sage}>
    <Mark n="04" />
    <Type text="O un tono\ndistinto." y={300} size={99} mode="words" />
    <Clip
      src="media/manga-lila.mp4"
      x={155}
      y={595}
      w={720}
      h={905}
      fit="contain"
    />
    <Note y={1570}>Ideas para combinar mangas largas.</Note>
  </Page>
);
export const Video04 = () => {
  const { fps } = useVideoConfig();
  return (
    <Page>
      <Music n="04" />
      <Sequence
        name="Mangas largas tipografía en dos niveles"
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <MangasHook />
      </Sequence>
      <Sequence
        name="Verde en uso real"
        from={4 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <MangasGreen />
      </Sequence>
      <Sequence
        name="Lila en uso real"
        from={9 * fps}
        durationInFrames={5 * fps}
        premountFor={fps}
      >
        <MangasLilac />
      </Sequence>
      <Sequence
        name="Consulta mangas largas"
        from={14 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <End cta="Escribinos por" keyword="mangas largas" number="04" />
      </Sequence>
    </Page>
  );
};
