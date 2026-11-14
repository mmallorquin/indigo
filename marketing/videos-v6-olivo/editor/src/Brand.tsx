import React from "react";
import {
  AbsoluteFill,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
  Interactive,
  type InteractivitySchema,
} from "remotion";
import { Video, Audio } from "@remotion/media";
import { loadFont } from "@remotion/fonts";

export const C = {
  olive: "#4F5533",
  deep: "#30371F",
  cream: "#F4F0E6",
  sage: "#CBD0B2",
  gold: "#C4AB79",
  ink: "#20251B",
  white: "#FFFFFF",
};
export const ease = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
  easing: Easing.bezier(0.16, 1, 0.3, 1),
};
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

export const Page: React.FC<
  React.PropsWithChildren<{ dark?: boolean; bg?: string }>
> = ({ children, dark = false, bg }) => (
  <AbsoluteFill
    style={{
      background: bg ?? (dark ? C.olive : C.cream),
      color: dark ? C.cream : C.ink,
      fontFamily: "Inter",
      overflow: "hidden",
    }}
  >
    {children}
  </AbsoluteFill>
);
export const Mark = ({
  dark = false,
  label = "ÍNDIGO PY",
  n = "01",
}: {
  dark?: boolean;
  label?: string;
  n?: string;
}) => (
  <div
    style={{
      position: "absolute",
      left: 86,
      right: 146,
      top: 162,
      display: "flex",
      justifyContent: "space-between",
      fontFamily: "Inter",
      fontWeight: 700,
      fontSize: 29,
      letterSpacing: 4,
      color: dark ? C.cream : C.olive,
      zIndex: 10,
    }}
  >
    <span>{label}</span>
    <span>{n} / 10</span>
  </div>
);
export const Note = ({
  children,
  dark = false,
  y = 1560,
}: {
  children: React.ReactNode;
  dark?: boolean;
  y?: number;
}) => (
  <div
    style={{
      position: "absolute",
      top: y,
      left: 88,
      width: 840,
      fontSize: 30,
      fontWeight: 500,
      lineHeight: 1.4,
      color: dark ? C.cream : C.olive,
    }}
  >
    {children}
  </div>
);
export const Small = ({
  children,
  x = 88,
  y = 290,
  w = 835,
  color = C.olive,
}: {
  children: React.ReactNode;
  x?: number;
  y?: number;
  w?: number;
  color?: string;
}) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: w,
      color,
      fontSize: 34,
      fontWeight: 700,
      letterSpacing: 2,
      lineHeight: 1.25,
    }}
  >
    {children}
  </div>
);

// One source template intentionally controls individual letter/word choreography.
type TypeProps = {
  text: string;
  x?: number;
  y?: number;
  w?: number;
  size?: number;
  color?: string;
  serif?: boolean;
  italic?: boolean;
  mode?: "words" | "letters" | "mask" | "track";
  delay?: number;
  align?: "left" | "center" | "right";
  style?: React.CSSProperties;
};
const TypeInner = ({
  text,
  x = 86,
  y = 320,
  w = 840,
  size = 100,
  color = C.ink,
  serif = false,
  italic = false,
  mode = "words",
  delay = 0,
  align = "left",
  style,
}: TypeProps) => {
  const f = useCurrentFrame();
  const chunks = text.replace(/\\n/g, "\n").split("\n");
  return (
    <Interactive.Div
      name="Texto animado"
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        fontFamily: serif ? "Cormorant" : "Inter",
        fontStyle: italic ? "italic" : "normal",
        fontWeight: serif ? 600 : 800,
        fontSize: size,
        lineHeight: serif ? 0.95 : 1.02,
        letterSpacing: serif ? -2 : -4,
        textAlign: align,
        color,
        ...style,
      }}
    >
      {chunks.map((line, li) => (
        <div
          key={li}
          style={{
            overflow: "hidden",
            paddingBottom: serif ? 18 : 9,
            marginBottom: serif ? -10 : -2,
          }}
        >
          {mode === "mask" || mode === "track" ? (
            <div
              style={{
                translate:
                  mode === "mask"
                    ? `0 ${interpolate(f, [delay + li * 5, delay + li * 5 + 24], [115, 0], ease)}%`
                    : undefined,
                opacity: interpolate(
                  f,
                  [delay + li * 5, delay + li * 5 + 12],
                  [0, 1],
                  ease,
                ),
                letterSpacing:
                  mode === "track"
                    ? interpolate(f, [delay, delay + 38], [18, -3], ease)
                    : undefined,
              }}
            >
              {line}
            </div>
          ) : (
            line.split(mode === "letters" ? "" : " ").map((unit, i) => (
              <span
                key={i}
                style={{
                  display: "inline-block",
                  whiteSpace: "pre",
                  opacity: interpolate(
                    f,
                    [
                      delay + li * 5 + i * (mode === "letters" ? 1.5 : 4),
                      delay + li * 5 + i * (mode === "letters" ? 1.5 : 4) + 10,
                    ],
                    [0, 1],
                    ease,
                  ),
                  translate: `0 ${interpolate(f, [delay + li * 5 + i * (mode === "letters" ? 1.5 : 4), delay + li * 5 + i * (mode === "letters" ? 1.5 : 4) + 22], [size * 0.85, 0], ease)}px`,
                  rotate:
                    mode === "letters"
                      ? `${interpolate(f, [delay + i * 1.5, delay + i * 1.5 + 24], [5, 0], ease)}deg`
                      : undefined,
                }}
              >
                {unit}
                {mode === "words" ? " " : ""}
              </span>
            ))
          )}
        </div>
      ))}
    </Interactive.Div>
  );
};
export const Type = Interactive.withSchema({
  Component: TypeInner,
  componentName: "<Type>",
  schema: {
    text: { type: "text-content", default: "Índigo", description: "Texto" },
    size: {
      type: "number",
      hiddenFromList: false,
      default: 100,
      description: "Tamaño",
    },
    color: { type: "color", default: "#20251B", description: "Color" },
    x: {
      type: "number",
      hiddenFromList: false,
      default: 86,
      description: "Posición X",
    },
    y: {
      type: "number",
      hiddenFromList: false,
      default: 320,
      description: "Posición Y",
    },
  } satisfies InteractivitySchema,
  wrapInSequence: true,
});

type MediaProps = {
  src: string;
  x?: number;
  y?: number;
  w?: number;
  h?: number;
  fit?: "cover" | "contain";
  position?: string;
  scale?: number;
  zoom?: number;
  pan?: number;
  radius?: number;
  rotate?: number;
  reveal?: "none" | "left" | "up" | "circle";
  border?: boolean;
  style?: React.CSSProperties;
};
export const Photo = ({
  src,
  x = 86,
  y = 600,
  w = 838,
  h = 800,
  fit = "cover",
  position = "50% 50%",
  scale = 1.04,
  zoom = 1,
  pan = 0,
  radius = 0,
  rotate = 0,
  reveal = "none",
  border = false,
  style,
}: MediaProps) => {
  const f = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        height: h,
        overflow: "hidden",
        borderRadius: radius,
        rotate: `${rotate}deg`,
        background: C.sage,
        border: border ? `12px solid ${C.cream}` : undefined,
        boxSizing: "border-box",
        clipPath:
          reveal === "left"
            ? `inset(0 ${interpolate(f, [0, 24], [100, 0], ease)}% 0 0)`
            : reveal === "up"
              ? `inset(${interpolate(f, [0, 25], [100, 0], ease)}% 0 0 0)`
              : reveal === "circle"
                ? `circle(${interpolate(f, [0, 32], [3, 80], ease)}% at 50% 50%)`
                : undefined,
        ...style,
      }}
    >
      <Img
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: fit,
          objectPosition: position,
          transformOrigin: position,
          scale: interpolate(
            f,
            [0, Math.max(1, durationInFrames - 1)],
            [zoom, zoom * scale],
            { extrapolateRight: "clamp" },
          ),
          translate: `${interpolate(f, [0, Math.max(1, durationInFrames - 1)], [0, pan])}px 0`,
        }}
      />
    </div>
  );
};
export const Clip = ({
  src,
  x = 86,
  y = 580,
  w = 838,
  h = 860,
  start = 0,
  fit = "cover",
  position = "50% 50%",
  radius = 0,
}: {
  src: string;
  x?: number;
  y?: number;
  w?: number;
  h?: number;
  start?: number;
  fit?: "cover" | "contain";
  position?: string;
  radius?: number;
}) => {
  const { fps } = useVideoConfig();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        height: h,
        overflow: "hidden",
        borderRadius: radius,
        background: C.sage,
      }}
    >
      <Video
        src={staticFile(src)}
        muted
        objectFit={fit}
        trimBefore={start * fps}
        premountFor={fps}
        style={{ width: "100%", height: "100%", objectPosition: position }}
      />
    </div>
  );
};
export const Rule = ({
  x = 88,
  y = 1480,
  w = 840,
  color = C.olive,
}: {
  x?: number;
  y?: number;
  w?: number;
  color?: string;
}) => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        height: 3,
        width: w,
        background: color,
        scale: `${interpolate(f, [5, 35], [0, 1], ease)} 1`,
        transformOrigin: "left",
      }}
    />
  );
};
export const Disc = ({
  x,
  y,
  size = 160,
  color = C.sage,
}: {
  x: number;
  y: number;
  size?: number;
  color?: string;
}) => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: size,
        height: size,
        borderRadius: "50%",
        background: color,
        scale: interpolate(f, [0, 25], [0.15, 1], ease),
      }}
    />
  );
};
export const End = ({
  cta,
  keyword,
  number,
  src,
  dark = false,
}: {
  cta: string;
  keyword: string;
  number: string;
  src?: string;
  dark?: boolean;
}) => {
  const f = useCurrentFrame();
  return (
    <Page dark={dark}>
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: 1080,
          height: 1920,
          background: dark ? C.deep : C.sage,
          clipPath: `inset(${interpolate(f, [0, 20], [100, 0], ease)}% 0 0)`,
        }}
      />
      <Mark dark={dark} n={number} />
      <Img
        src={staticFile("brand/logo.jpg")}
        style={{
          position: "absolute",
          left: 88,
          top: 285,
          width: 218,
          height: 218,
          objectFit: "contain",
          borderRadius: "50%",
          scale: interpolate(f, [0, 24], [0.88, 1], ease),
        }}
      />
      <Type
        text={cta}
        x={86}
        y={560}
        size={78}
        color={dark ? C.cream : C.ink}
        mode="mask"
      />
      <Type
        text={keyword}
        x={86}
        y={790}
        size={100}
        serif
        italic
        color={dark ? C.cream : C.olive}
        mode="letters"
        delay={8}
      />
      <div
        style={{
          position: "absolute",
          left: 90,
          top: 1065,
          width: 830,
          fontSize: 43,
          lineHeight: 1.5,
          color: dark ? C.cream : C.ink,
        }}
      >
        WhatsApp
        <br />
        <strong style={{ fontSize: 52 }}>+595 973 434 868</strong>
      </div>
      {src && (
        <Photo
          src={src}
          x={675}
          y={1160}
          w={235}
          h={270}
          radius={120}
          scale={1.02}
        />
      )}
      <Rule y={1470} color={dark ? C.sage : C.olive} />
      <Note dark={dark} y={1508}>
        Consultá disponibilidad, talles y precio.
      </Note>
    </Page>
  );
};
export const Music = ({ n }: { n: string }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const bpm =
    {
      "01": 100,
      "02": 102,
      "03": 104,
      "04": 106,
      "05": 108,
      "06": 110,
      "07": 112,
      "08": 103,
      "09": 105,
      "10": 109,
    }[n] ?? 100;
  const pulse = Math.pow(1 - ((frame / ((60 * fps) / bpm)) % 1), 4);
  return (
    <>
      <div
        aria-hidden
        style={{
          position: "absolute",
          left: 88,
          top: 120,
          width: 70,
          height: 4,
          background: C.gold,
          scale: `${0.8 + pulse * 0.35} 1`,
          transformOrigin: "left",
          opacity: 0.35 + pulse * 0.45,
          zIndex: 40,
        }}
      />
      <Audio
        src={staticFile(`audio/${n}.wav`)}
        premountFor={fps}
        volume={(f) =>
          interpolate(
            f,
            [0, 12, durationInFrames - 18, durationInFrames - 1],
            [0, 1, 1, 0],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
          )
        }
      />
    </>
  );
};
