import React from "react";
import {
  AbsoluteFill,
  Composition,
  Img,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { loadFont } from "@remotion/fonts";
Promise.all([
  loadFont({
    family: "Inter",
    url: staticFile("fonts/inter-500.woff2"),
    weight: "500",
  }),
  loadFont({
    family: "Inter",
    url: staticFile("fonts/inter-700.woff2"),
    weight: "700",
  }),
  loadFont({
    family: "Inter",
    url: staticFile("fonts/inter-800.woff2"),
    weight: "800",
  }),
  loadFont({
    family: "Cormorant",
    url: staticFile("fonts/cormorant-normal.ttf"),
    weight: "600",
  }),
  loadFont({
    family: "Cormorant",
    url: staticFile("fonts/cormorant-italic.ttf"),
    weight: "600",
    style: "italic",
  }),
]);
const P = {
  stage: "#30371F",
  olive: "#4F5533",
  paper: "#F4F0E6",
  accent: "#C4AB79",
  ink: "#20251B",
  sage: "#CBD0B2",
};
const ease = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
  easing: Easing.inOut(Easing.cubic),
};
type Props = { cameraSrc: string };
const Text = ({
  children,
  y = 350,
  size = 85,
  serif = false,
  color = P.ink,
}: {
  children: React.ReactNode;
  y?: number;
  size?: number;
  serif?: boolean;
  color?: string;
}) => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: 88,
        top: y,
        width: 830,
        fontFamily: serif ? "Cormorant" : "Inter",
        fontSize: size,
        fontWeight: serif ? 600 : 800,
        lineHeight: 1.05,
        letterSpacing: serif ? -1 : -3,
        color,
        opacity: interpolate(f, [0, 15], [0, 1], ease),
        translate: `0 ${interpolate(f, [0, 21], [35, 0], ease)}px`,
      }}
    >
      {children}
    </div>
  );
};
const Header = ({ n }: { n: string }) => (
  <div
    style={{
      position: "absolute",
      left: 88,
      right: 144,
      top: 168,
      color: P.paper,
      font: "700 28px Inter",
      letterSpacing: 4,
      display: "flex",
      justifyContent: "space-between",
    }}
  >
    <span>ÍNDIGO PY</span>
    <span>{n}</span>
  </div>
);
const Camera = ({ src, small = false }: { src: string; small?: boolean }) => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: 88,
        top: 288,
        width: 904,
        height: small ? 530 : 1130,
        borderRadius: 40,
        overflow: "hidden",
        background: "#41492C",
        border: "1px solid #C4AB7938",
        boxShadow: "0 18px 65px #14180E55",
        scale: interpolate(f, [0, 900], [1, 1.012], {
          extrapolateRight: "clamp",
        }),
      }}
    >
      {src ? (
        <OffthreadVideo
          src={staticFile(src)}
          muted
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      ) : (
        <div
          style={{
            width: "100%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            color: P.paper,
          }}
        >
          <Img
            src={staticFile("brand/logo.jpg")}
            style={{ width: 150, height: 150, borderRadius: "50%" }}
          />
          <div
            style={{ marginTop: 26, font: "700 26px Inter", letterSpacing: 3 }}
          >
            ESPACIO PARA TU GRABACIÓN
          </div>
          <div style={{ marginTop: 14, font: "500 24px Inter", opacity: 0.65 }}>
            Maqueta · la persona todavía no está incorporada
          </div>
        </div>
      )}
    </div>
  );
};
const Base: React.FC<React.PropsWithChildren<{ n: string }>> = ({
  n,
  children,
}) => (
  <AbsoluteFill
    style={{
      background: P.stage,
      fontFamily: "Inter",
      color: P.paper,
      overflow: "hidden",
    }}
  >
    <div
      style={{
        position: "absolute",
        width: 900,
        height: 900,
        left: -480,
        top: 100,
        borderRadius: "50%",
        background: P.olive,
        filter: "blur(170px)",
        opacity: 0.28,
      }}
    />
    <Header n={n} />
    {children}
    <div
      style={{
        position: "absolute",
        left: 88,
        bottom: 245,
        color: P.sage,
        font: "500 25px Inter",
      }}
    >
      PREPARACIÓN · PENDIENTE DE GRABACIÓN REAL
    </div>
  </AbsoluteFill>
);
const Paper: React.FC<React.PropsWithChildren> = ({ children }) => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: 60,
        top: 885,
        width: 960,
        height: 760,
        borderRadius: 40,
        background: P.paper,
        translate: `0 ${interpolate(f, [0, 21], [90, 0], ease)}px`,
        opacity: interpolate(f, [0, 12], [0, 1], ease),
        color: P.ink,
        boxShadow: "0 22px 60px #14180E33",
      }}
    >
      {children}
    </div>
  );
};
const Card = ({
  src,
  x,
  w = 240,
  h = 355,
  delay = 0,
  label,
}: {
  src: string;
  x: number;
  w?: number;
  h?: number;
  delay?: number;
  label: string;
}) => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: 200,
        width: w,
        opacity: interpolate(f, [delay, delay + 15], [0, 1], ease),
        translate: `0 ${interpolate(f, [delay, delay + 21], [50, 0], ease)}px`,
      }}
    >
      <Img
        src={staticFile("media/" + src)}
        style={{
          width: w,
          height: h,
          objectFit: "cover",
          objectPosition: "60% 50%",
          borderRadius: 20,
        }}
      />
      <div
        style={{
          marginTop: 22,
          fontSize: 24,
          fontWeight: 700,
          letterSpacing: 0,
          lineHeight: 1.3,
        }}
      >
        {label}
      </div>
    </div>
  );
};
const Diagram = () => {
  const f = useCurrentFrame();
  const length = 480;
  return (
    <svg
      width="780"
      height="75"
      viewBox="0 0 780 75"
      style={{ position: "absolute", left: 88, top: 626 }}
    >
      <text
        x="0"
        y="47"
        fill={P.olive}
        fontSize="27"
        fontFamily="Inter"
        fontWeight="700"
      >
        BASE
      </text>
      <path
        d="M 112 37 H 592"
        fill="none"
        stroke={P.accent}
        strokeWidth="3"
        strokeDasharray={length}
        strokeDashoffset={interpolate(f, [25, 60], [length, 0], ease)}
      />
      <path
        d="M 582 29 L 592 37 L 582 45"
        fill="none"
        stroke={P.accent}
        strokeWidth="3"
        opacity={interpolate(f, [55, 62], [0, 1], ease)}
      />
      <text
        x="610"
        y="47"
        fill={P.olive}
        fontSize="25"
        fontFamily="Inter"
        fontWeight="700"
      >
        TONO
      </text>
    </svg>
  );
};
const Combinaciones = () => (
  <Paper>
    <Text y={52} size={66} serif>
      Tres ideas para combinar.
    </Text>
    <Card src="conjunto-beige.jpg" x={88} label="Beige + negro" />
    <Card src="conjunto-uva.jpg" x={360} label="Vino + violeta" delay={10} />
    <Card
      src="conjunto-marron.jpg"
      x={632}
      label="Marrón + marrón"
      delay={20}
    />
    <Diagram />
  </Paper>
);
const Detalles = () => {
  const f = useCurrentFrame();
  return (
    <Paper>
      <Text y={52} size={66} serif>
        Una mirada de cerca.
      </Text>
      <div
        style={{
          position: "absolute",
          left: 88,
          top: 210,
          width: 400,
          height: 460,
          borderRadius: 22,
          overflow: "hidden",
        }}
      >
        <Img
          src={staticFile("media/blusa.jpg")}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            scale: interpolate(f, [0, 180], [1, 1.16], ease),
            transformOrigin: "50% 80%",
          }}
        />
      </div>
      <div style={{ position: "absolute", left: 560, top: 232, width: 300 }}>
        {["Cuello", "Mangas", "Detalles"].map((s, i) => (
          <div
            key={s}
            style={{
              fontSize: 50,
              fontWeight: 700,
              lineHeight: 1.3,
              padding: "21px 0",
              borderBottom: "1px solid #CBD0B2",
              opacity: interpolate(f, [i * 20, i * 20 + 15], [0, 1], ease),
              translate: `0 ${interpolate(f, [i * 20, i * 20 + 21], [30, 0], ease)}px`,
            }}
          >
            {s}
          </div>
        ))}
      </div>
    </Paper>
  );
};
const Capas = () => {
  const f = useCurrentFrame();
  return (
    <Paper>
      <Text y={52} size={66} serif>
        Dos referencias de capas.
      </Text>
      <Card
        src="chaleco-a.jpg"
        x={88}
        w={345}
        h={430}
        label="Idea: camisa + chaleco"
      />
      <Card
        src="azul-crema.jpg"
        x={515}
        w={345}
        h={430}
        label="Referencia: azul + crema"
        delay={14}
      />
      <div
        style={{
          position: "absolute",
          left: 88,
          top: 690,
          width: 770,
          height: 3,
          background: P.accent,
          scale: `${interpolate(f, [10, 55], [0, 1], ease)} 1`,
          transformOrigin: "left",
        }}
      />
    </Paper>
  );
};
const Opening = ({
  cameraSrc,
  n,
  text,
}: {
  cameraSrc: string;
  n: string;
  text: string;
}) => (
  <Base n={n}>
    <Camera src={cameraSrc} />
    <Text y={1460} size={80} color={P.paper}>
      {text}
    </Text>
  </Base>
);
const Content = ({
  cameraSrc,
  n,
  children,
}: React.PropsWithChildren<{ cameraSrc: string; n: string }>) => (
  <Base n={n}>
    <Camera src={cameraSrc} small />
    {children}
  </Base>
);
const End = ({ n, cta }: { n: string; cta: string }) => (
  <Base n={n}>
    <Img
      src={staticFile("brand/logo.jpg")}
      style={{
        position: "absolute",
        left: 88,
        top: 340,
        width: 260,
        height: 260,
        borderRadius: "50%",
      }}
    />
    <Text y={805} serif size={116} color={P.paper}>
      Seguimos combinando.
    </Text>
    <Text y={1080} size={71} color={P.paper}>
      {cta}
    </Text>
  </Base>
);
const V11 = ({ cameraSrc }: Props) => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Sequence
        name="Gancho provisional"
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <Opening cameraSrc={cameraSrc} n="11" text="Una base. Otra idea." />
      </Sequence>
      <Sequence
        name="Gráficas de combinaciones — cue pendiente"
        from={4 * fps}
        durationInFrames={22 * fps}
        premountFor={fps}
      >
        <Content cameraSrc={cameraSrc} n="11">
          <Combinaciones />
        </Content>
      </Sequence>
      <Sequence
        name="Cierre provisional"
        from={26 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <End n="11" cta="Comentá cuál combinación querés ver de cerca." />
      </Sequence>
    </>
  );
};
const V12 = ({ cameraSrc }: Props) => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Sequence
        name="Gancho provisional"
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <Opening cameraSrc={cameraSrc} n="12" text="Mirá más que el color." />
      </Sequence>
      <Sequence
        name="Gráficas de detalles — cue pendiente"
        from={4 * fps}
        durationInFrames={22 * fps}
        premountFor={fps}
      >
        <Content cameraSrc={cameraSrc} n="12">
          <Detalles />
        </Content>
      </Sequence>
      <Sequence
        name="Cierre provisional"
        from={26 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <End n="12" cta="Comentá qué detalle querés ver de cerca." />
      </Sequence>
    </>
  );
};
const V13 = ({ cameraSrc }: Props) => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Sequence
        name="Gancho provisional"
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <Opening cameraSrc={cameraSrc} n="13" text="Una capa abre otra idea." />
      </Sequence>
      <Sequence
        name="Gráficas de capas — cue pendiente"
        from={4 * fps}
        durationInFrames={22 * fps}
        premountFor={fps}
      >
        <Content cameraSrc={cameraSrc} n="13">
          <Capas />
        </Content>
      </Sequence>
      <Sequence
        name="Cierre provisional"
        from={26 * fps}
        durationInFrames={4 * fps}
        premountFor={fps}
      >
        <End
          n="13"
          cta="Comentá qué combinación querés para el próximo video."
        />
      </Sequence>
    </>
  );
};
export const RemotionRoot = () => (
  <>
    <Composition
      id="11-Combinaciones-Maqueta"
      component={V11}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={900}
      defaultProps={{ cameraSrc: "" }}
    />
    <Composition
      id="12-Detalles-Maqueta"
      component={V12}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={900}
      defaultProps={{ cameraSrc: "" }}
    />
    <Composition
      id="13-Capas-Maqueta"
      component={V13}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={900}
      defaultProps={{ cameraSrc: "" }}
    />
  </>
);
