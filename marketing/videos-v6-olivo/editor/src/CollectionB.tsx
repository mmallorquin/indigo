import {
  Sequence,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {
  Page,
  Mark,
  Type,
  Photo,
  Small,
  Note,
  Rule,
  End,
  Music,
  C,
  ease,
} from "./Brand";

// The shared brand components are shifted into the requested text safe area.
const SafeMark = ({ n, dark = false }: { n: string; dark?: boolean }) => (
  <div style={{ position: "absolute", inset: 0 }}>
    <Mark n={n} dark={dark} />
  </div>
);

const SafeEnd = ({
  cta,
  keyword,
  number,
  dark = false,
}: {
  cta: string;
  keyword: string;
  number: string;
  dark?: boolean;
}) => (
  <div style={{ position: "absolute", inset: 0 }}>
    <End cta={cta} keyword={keyword} number={number} dark={dark} />
  </div>
);

const SastreroOpening = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Page>
      <SafeMark n="05" />
      <Type
        text="Sastrero.\nDe cerca."
        x={88}
        y={315}
        w={840}
        size={113}
        serif
        color={C.olive}
        mode="mask"
        premountFor={fps}
      />
      <div
        style={{
          position: "absolute",
          left: 88,
          top: 665,
          width: 164,
          height: 690,
          background: C.sage,
          scale: `1 ${interpolate(frame, [0, 0.8 * fps], [0, 1], ease)}`,
          transformOrigin: "top",
        }}
      />
      <Small x={108} y={735} w={130}>
        EL
        <br />
        CORTE
      </Small>
      <Rule x={108} y={925} w={116} />
      <Photo
        src="media/sastrero.jpg"
        x={304}
        y={605}
        w={624}
        h={850}
        fit="contain"
        reveal="left"
        scale={1.025}
      />
      <Note y={1508}>Inspiración de una publicación anterior.</Note>
    </Page>
  );
};

const SastreroStructure = () => {
  const { fps } = useVideoConfig();
  return (
    <Page bg={C.sage}>
      <SafeMark n="05" />
      <Type
        text="Una mirada\nal corte."
        x={88}
        y={310}
        w={840}
        size={94}
        mode="words"
        premountFor={fps}
      />
      <Photo
        src="media/sastrero.jpg"
        x={88}
        y={575}
        w={556}
        h={870}
        fit="contain"
        scale={1.025}
        reveal="up"
      />
      <Photo
        src="media/sastrero.jpg"
        x={680}
        y={670}
        w={248}
        h={435}
        position="50% 6%"
        zoom={2.4}
        scale={1.035}
      />
      <Small x={680} y={1170} w={248}>
        CINTURA
        <br />Y LÍNEAS
      </Small>
      <Rule x={680} y={1310} w={248} />
      <Note y={1508}>Detalles que inspiran una combinación.</Note>
    </Page>
  );
};

const SastreroPortrait = () => {
  const { fps } = useVideoConfig();
  return (
    <Page dark>
      <SafeMark n="05" dark />
      <Photo
        src="media/sastrero.jpg"
        x={88}
        y={310}
        w={840}
        h={890}
        fit="contain"
        reveal="left"
        scale={1.02}
      />
      <Type
        text="Una base para\ncombinar."
        x={88}
        y={1255}
        w={840}
        size={91}
        serif
        italic
        color={C.cream}
        mode="mask"
        premountFor={fps}
      />
      <Note y={1518} dark>
        Referencia de una publicación anterior.
      </Note>
    </Page>
  );
};

export const Video05 = () => {
  const { fps } = useVideoConfig();
  return (
    <Page>
      <Music n="05" />
      <Sequence
        name="Gancho: sastrero de cerca"
        durationInFrames={1.5 * fps}
        premountFor={fps}
      >
        <SastreroOpening />
      </Sequence>
      <Sequence
        name="Editorial asimétrica y cintura"
        from={1.5 * fps}
        durationInFrames={6.5 * fps}
        premountFor={fps}
      >
        <SastreroStructure />
      </Sequence>
      <Sequence
        name="La referencia de pantalón"
        from={8 * fps}
        durationInFrames={6 * fps}
        premountFor={fps}
      >
        <SastreroPortrait />
      </Sequence>
      <Sequence
        name="Consulta por sastrero"
        from={14 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <SafeEnd cta="Consultá por" keyword="un sastrero" number="05" dark />
      </Sequence>
    </Page>
  );
};

const BlusaOpening = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Page>
      <SafeMark n="06" />
      <Type
        text="La blusa\nprotagonista."
        x={88}
        y={320}
        w={840}
        size={107}
        serif
        italic
        color={C.olive}
        mode="mask"
        premountFor={fps}
      />
      <div
        style={{
          position: "absolute",
          left: 136,
          top: 610,
          width: 744,
          height: 744,
          borderRadius: "50%",
          border: `3px solid ${C.gold}`,
          scale: interpolate(frame, [0, 0.85 * fps], [0.82, 1.07], ease),
        }}
      />
      <Photo
        src="media/blusa.jpg"
        x={150}
        y={625}
        w={716}
        h={716}
        fit="contain"
        radius={358}
        reveal="circle"
        scale={1.025}
      />
      <Small x={88} y={1430} w={840}>
        SIN MANGAS · DETALLE FRUNCIDO
      </Small>
      <Note y={1518}>Inspiración de una publicación anterior.</Note>
    </Page>
  );
};

const BlusaHero = () => {
  const { fps } = useVideoConfig();
  return (
    <Page bg={C.sage}>
      <SafeMark n="06" />
      <Type
        text="Sin mangas."
        x={88}
        y={305}
        w={840}
        size={112}
        serif
        color={C.olive}
        mode="track"
        premountFor={fps}
      />
      <Photo
        src="media/blusa.jpg"
        x={88}
        y={495}
        w={840}
        h={930}
        fit="contain"
        scale={1.025}
        reveal="up"
      />
      <Rule y={1470} />
      <Note y={1518}>Una idea para tu próxima combinación.</Note>
    </Page>
  );
};

const BlusaDetail = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Page dark>
      <SafeMark n="06" dark />
      <Type
        text="El fruncido,\nde cerca."
        x={88}
        y={310}
        w={840}
        size={101}
        color={C.cream}
        mode="words"
        premountFor={fps}
      />
      {/* A photographic crop only: no generated folds or invented product detail. */}
      <Photo
        src="media/blusa.jpg"
        x={140}
        y={645}
        w={736}
        h={736}
        radius={368}
        position="50% 82%"
        zoom={1.7}
        reveal="circle"
        scale={1.09}
      />
      <div
        style={{
          position: "absolute",
          left: 120,
          top: 625,
          width: 776,
          height: 776,
          borderRadius: "50%",
          border: `2px solid ${C.sage}`,
          opacity: interpolate(frame, [0.35 * fps, 1 * fps], [0, 1], ease),
          rotate: `${interpolate(frame, [0, 5 * fps], [-8, 8], ease)}deg`,
        }}
      />
      <Small x={88} y={1450} w={840} color={C.sage}>
        UNA MIRADA AL DISEÑO
      </Small>
      <Note y={1530} dark>
        Detalle de una referencia anterior.
      </Note>
    </Page>
  );
};

export const Video06 = () => {
  const { fps } = useVideoConfig();
  return (
    <Page>
      <Music n="06" />
      <Sequence
        name="Gancho: blusa protagonista"
        durationInFrames={1.5 * fps}
        premountFor={fps}
      >
        <BlusaOpening />
      </Sequence>
      <Sequence
        name="Vista de la blusa sin mangas"
        from={1.5 * fps}
        durationInFrames={6.5 * fps}
        premountFor={fps}
      >
        <BlusaHero />
      </Sequence>
      <Sequence
        name="Máscara circular del fruncido"
        from={8 * fps}
        durationInFrames={6 * fps}
        premountFor={fps}
      >
        <BlusaDetail />
      </Sequence>
      <Sequence
        name="Consulta por blusa"
        from={14 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <SafeEnd cta="Consultá por" keyword="esta blusa" number="06" />
      </Sequence>
    </Page>
  );
};

const ConjuntosOpening = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Page bg={C.deep}>
      <SafeMark n="07" dark />
      <Type
        text="Tres ideas.\nA tu manera."
        x={88}
        y={315}
        w={840}
        size={104}
        serif
        italic
        color={C.cream}
        mode="mask"
        premountFor={fps}
      />
      <Photo
        src="media/conjunto-beige.jpg"
        x={105}
        y={735}
        w={346}
        h={648}
        fit="cover"
        position="60% 50%"
        border
        scale={1.02}
        style={{
          rotate: `${interpolate(frame, [0, 0.85 * fps], [-14, -7], ease)}deg`,
          translate: `${interpolate(frame, [0, 0.85 * fps], [-145, 0], ease)}px 0`,
        }}
      />
      <Photo
        src="media/conjunto-marron.jpg"
        x={651}
        y={805}
        w={265}
        h={600}
        fit="cover"
        position="60% 50%"
        border
        scale={1.02}
        style={{
          rotate: `${interpolate(frame, [0, 0.9 * fps], [14, 6], ease)}deg`,
          translate: `${interpolate(frame, [0, 0.9 * fps], [145, 0], ease)}px 0`,
        }}
      />
      <Photo
        src="media/conjunto-uva.jpg"
        x={364}
        y={660}
        w={344}
        h={730}
        fit="cover"
        position="60% 50%"
        border
        scale={1.02}
        style={{
          rotate: `${interpolate(frame, [0, 0.7 * fps], [-5, 1], ease)}deg`,
          translate: `0 ${interpolate(frame, [0, 0.7 * fps], [135, 0], ease)}px`,
        }}
      />
      <Note y={1518} dark>
        Combinaciones de publicaciones anteriores.
      </Note>
    </Page>
  );
};

const ConjuntosTriptych = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Page>
      <SafeMark n="07" />
      <Type
        text="Tres combinaciones."
        x={88}
        y={315}
        w={840}
        size={92}
        serif
        color={C.olive}
        mode="mask"
        premountFor={fps}
      />
      <Small y={465}>DE NUESTRO PERFIL</Small>
      <Photo
        src="media/conjunto-beige.jpg"
        x={88}
        y={595}
        w={258}
        h={785}
        fit="cover"
        position="60% 50%"
        scale={1.03}
        style={{
          translate: `0 ${interpolate(frame, [0, 0.9 * fps], [70, 0], ease)}px`,
        }}
      />
      <Photo
        src="media/conjunto-uva.jpg"
        x={379}
        y={650}
        w={258}
        h={785}
        fit="cover"
        position="60% 50%"
        scale={1.03}
        style={{
          translate: `0 ${interpolate(frame, [0.12 * fps, 1 * fps], [100, 0], ease)}px`,
        }}
      />
      <Photo
        src="media/conjunto-marron.jpg"
        x={670}
        y={595}
        w={258}
        h={785}
        fit="cover"
        position="60% 50%"
        scale={1.03}
        style={{
          translate: `0 ${interpolate(frame, [0.25 * fps, 1.15 * fps], [70, 0], ease)}px`,
        }}
      />
      <Note y={1530}>Referencias para inspirar una combinación.</Note>
    </Page>
  );
};

const ConjuntosCollage = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Page bg={C.sage}>
      <SafeMark n="07" />
      <Photo
        src="media/conjunto-beige.jpg"
        x={99}
        y={410}
        w={395}
        h={720}
        fit="cover"
        position="60% 50%"
        border
        scale={1.015}
        style={{
          rotate: `${interpolate(frame, [0, 1 * fps], [-10, -4], ease)}deg`,
          translate: `${interpolate(frame, [0, 1 * fps], [-45, 0], ease)}px 0`,
        }}
      />
      <Photo
        src="media/conjunto-marron.jpg"
        x={571}
        y={605}
        w={343}
        h={620}
        fit="cover"
        position="60% 50%"
        border
        scale={1.015}
        style={{
          rotate: `${interpolate(frame, [0, 1 * fps], [12, 5], ease)}deg`,
          translate: `${interpolate(frame, [0, 1 * fps], [45, 0], ease)}px 0`,
        }}
      />
      <Photo
        src="media/conjunto-uva.jpg"
        x={329}
        y={460}
        w={412}
        h={744}
        fit="cover"
        position="60% 50%"
        border
        scale={1.02}
        style={{
          rotate: `${interpolate(frame, [0, 1 * fps], [-3, 1], ease)}deg`,
          translate: `0 ${interpolate(frame, [0, 1 * fps], [70, 0], ease)}px`,
        }}
      />
      <Type
        text="Para inspirar\ntu próximo look."
        x={88}
        y={1260}
        w={840}
        size={86}
        mode="words"
        premountFor={fps}
      />
      <Note y={1518}>Inspiración de publicaciones anteriores.</Note>
    </Page>
  );
};

export const Video07 = () => {
  const { fps } = useVideoConfig();
  return (
    <Page>
      <Music n="07" />
      <Sequence
        name="Gancho: tres ideas"
        durationInFrames={1.5 * fps}
        premountFor={fps}
      >
        <ConjuntosOpening />
      </Sequence>
      <Sequence
        name="Tres combinaciones del perfil"
        from={1.5 * fps}
        durationInFrames={7.5 * fps}
        premountFor={fps}
      >
        <ConjuntosTriptych />
      </Sequence>
      <Sequence
        name="Collage animado de referencias"
        from={9 * fps}
        durationInFrames={7 * fps}
        premountFor={fps}
      >
        <ConjuntosCollage />
      </Sequence>
      <Sequence
        name="Consulta por conjuntos"
        from={16 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <SafeEnd cta="Consultá por" keyword="conjuntos" number="07" dark />
      </Sequence>
    </Page>
  );
};
