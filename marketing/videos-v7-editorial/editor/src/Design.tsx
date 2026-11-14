import React from "react";
import {
  AbsoluteFill,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { Audio } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
export const P = {
  olive: "#4F5533",
  stage: "#30371F",
  paper: "#F4F0E6",
  accent: "#C4AB79",
  ink: "#20251B",
  sage: "#CBD0B2",
};
export const ease = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
  easing: Easing.inOut(Easing.cubic),
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
export const Stage = ({
  n,
  dark = false,
  children,
}: {
  n: string;
  dark?: boolean;
  children: React.ReactNode;
}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        background: dark ? P.stage : P.paper,
        color: dark ? P.paper : P.ink,
        fontFamily: "Inter",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          left: -550,
          top: 140 + Math.sin(f / 45) * 12,
          width: 1000,
          height: 1000,
          borderRadius: "50%",
          background: dark ? P.olive : P.sage,
          filter: "blur(160px)",
          opacity: 0.25,
        }}
      />
      <div
        style={{
          position: "absolute",
          top: 150,
          left: 86,
          width: 842,
          display: "flex",
          justifyContent: "space-between",
          fontSize: 28,
          fontWeight: 700,
          letterSpacing: 4,
          color: dark ? P.paper : P.olive,
          zIndex: 10,
        }}
      >
        <span>ÍNDIGO PY</span>
        <span>{n}</span>
      </div>
      {children}
      <svg
        width="1080"
        height="1920"
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
          opacity: 0.024,
          zIndex: 20,
        }}
      >
        <filter id="grain">
          <feTurbulence
            type="fractalNoise"
            baseFrequency=".72"
            numOctaves="2"
            seed="11"
            stitchTiles="stitch"
          />
        </filter>
        <rect width="1080" height="1920" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};
export const Label = ({
  children,
  x = 88,
  y = 290,
  w = 840,
  dark = false,
  size = 31,
}: {
  children: React.ReactNode;
  x?: number;
  y?: number;
  w?: number;
  dark?: boolean;
  size?: number;
}) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: w,
      fontSize: size,
      fontWeight: 700,
      lineHeight: 1.3,
      letterSpacing: 2,
      color: dark ? P.sage : P.olive,
    }}
  >
    {children}
  </div>
);
export const Type = ({
  text,
  x = 86,
  y = 345,
  w = 842,
  size = 100,
  serif = false,
  italic = false,
  color = P.ink,
  mode = "mask",
  delay = 0,
}: {
  text: string;
  x?: number;
  y?: number;
  w?: number;
  size?: number;
  serif?: boolean;
  italic?: boolean;
  color?: string;
  mode?: "mask" | "letters" | "words" | "track";
  delay?: number;
}) => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        fontFamily: serif ? "Cormorant" : "Inter",
        fontWeight: serif ? 600 : 800,
        fontStyle: italic ? "italic" : "normal",
        fontSize: size,
        lineHeight: serif ? 1 : 1.04,
        color,
        letterSpacing: serif ? -1 : -3,
      }}
    >
      {text
        .replace(/\\n/g, "\n")
        .split("\n")
        .map((line, l) => (
          <div
            key={l}
            style={{ overflow: "hidden", paddingBottom: 14, marginBottom: -5 }}
          >
            {mode === "mask" || mode === "track" ? (
              <div
                style={{
                  translate:
                    mode === "mask"
                      ? `0 ${interpolate(f, [delay + l * 5, delay + l * 5 + 21], [112, 0], ease)}%`
                      : undefined,
                  opacity: interpolate(
                    f,
                    [delay + l * 5, delay + l * 5 + 12],
                    [0, 1],
                    ease,
                  ),
                  letterSpacing:
                    mode === "track"
                      ? interpolate(
                          f,
                          [delay, delay + 30],
                          [9, serif ? -1 : -3],
                          ease,
                        )
                      : undefined,
                }}
              >
                {line}
              </div>
            ) : (
              line.split(mode === "letters" ? "" : " ").map((s, i) => (
                <span
                  key={i}
                  style={{
                    display: "inline-block",
                    whiteSpace: "pre",
                    opacity: interpolate(
                      f,
                      [
                        delay + l * 5 + i * (mode === "letters" ? 1.2 : 4),
                        delay + l * 5 + i * (mode === "letters" ? 1.2 : 4) + 10,
                      ],
                      [0, 1],
                      ease,
                    ),
                    translate: `0 ${interpolate(f, [delay + l * 5 + i * (mode === "letters" ? 1.2 : 4), delay + l * 5 + i * (mode === "letters" ? 1.2 : 4) + 18], [size * 0.7, 0], ease)}px`,
                  }}
                >
                  {s}
                  {mode === "words" ? " " : ""}
                </span>
              ))
            )}
          </div>
        ))}
    </div>
  );
};
export const Photo = ({
  src,
  x = 86,
  y = 620,
  w = 842,
  h = 840,
  fit = "cover",
  position = "60% 50%",
  zoom = 1,
  radius = 26,
  tilt = 0,
  delay = 0,
}: {
  src: string;
  x?: number;
  y?: number;
  w?: number;
  h?: number;
  fit?: "contain" | "cover";
  position?: string;
  zoom?: number;
  radius?: number;
  tilt?: number;
  delay?: number;
}) => {
  const f = useCurrentFrame();
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
        background: P.sage,
        boxShadow: "0 18px 55px #20251B18",
        opacity: interpolate(f, [delay, delay + 18], [0, 1], ease),
        translate: `0 ${interpolate(f, [delay, delay + 21], [48, 0], ease)}px`,
        rotate: `${tilt + Math.sin(f / 60) * 0.15}deg`,
      }}
    >
      <Img
        src={staticFile("media/" + src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: fit,
          objectPosition: position,
          transformOrigin: position,
          scale: zoom * (1.016 + 0.014 * Math.sin(f / 58)),
        }}
      />
    </div>
  );
};
export const Line = ({
  x = 88,
  y = 1530,
  w = 840,
  color = P.accent,
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
        width: w,
        height: 3,
        background: color,
        scale: `${interpolate(f, [0, 28], [0, 1], ease)} 1`,
        transformOrigin: "left",
      }}
    />
  );
};
export const Foot = ({
  children,
  dark = false,
  y = 1580,
}: {
  children: React.ReactNode;
  dark?: boolean;
  y?: number;
}) => (
  <div
    style={{
      position: "absolute",
      left: 88,
      top: y,
      width: 840,
      fontSize: 29,
      lineHeight: 1.35,
      color: dark ? P.sage : P.olive,
      fontWeight: 500,
    }}
  >
    {children}
  </div>
);
export const TitleCard = ({
  n,
  title,
  subtitle,
}: {
  n: string;
  title: string;
  subtitle: string;
}) => (
  <Stage n={n} dark>
    <Label y={570} dark>
      ÍNDIGO · IDEAS PARA TU LOOK
    </Label>
    <Type text={title} y={740} size={112} serif color={P.paper} mode="mask" />
    <Line y={1190} />
    <Foot y={1250} dark>
      {subtitle}
    </Foot>
  </Stage>
);
export const EndCard = ({ n, cta }: { n: string; cta: string }) => {
  const f = useCurrentFrame();
  return (
    <Stage n={n} dark>
      <Img
        src={staticFile("brand/logo.jpg")}
        style={{
          position: "absolute",
          left: 88,
          top: 320,
          width: 230,
          height: 230,
          borderRadius: "50%",
          scale: 1.014 + 0.013 * Math.sin(f / 43),
        }}
      />
      <Type
        text="Seguimos\ncombinando."
        y={675}
        serif
        italic
        size={139}
        color={P.paper}
        mode="track"
      />
      <Type text={cta} y={1130} size={71} color={P.paper} mode="words" />
      <Line y={1520} />
      <Foot dark y={1570}>
        @indigopy_ · inspiración de nuestro perfil
      </Foot>
    </Stage>
  );
};
// The straight SVG segment is exactly 520 px long. Its dash uses that length.
export const Arrow = ({
  x = 88,
  y = 1390,
  w = 840,
  labels = ["BASE", "TONO"],
  dark = false,
}: {
  x?: number;
  y?: number;
  w?: number;
  labels?: string[];
  dark?: boolean;
}) => {
  const f = useCurrentFrame();
  return (
    <svg
      width={w}
      height={90}
      viewBox="0 0 840 90"
      style={{ position: "absolute", left: x, top: y }}
    >
      <text
        x="0"
        y="54"
        fontFamily="Inter"
        fontWeight="700"
        fontSize="36"
        fill={dark ? P.paper : P.olive}
      >
        {labels[0]}
      </text>
      <path
        d="M 125 42 H 645"
        stroke={P.accent}
        strokeWidth="3"
        fill="none"
        strokeDasharray={520}
        strokeDashoffset={interpolate(f, [15, 48], [520, 0], ease)}
      />
      <path
        d="M 631 31 L 645 42 L 631 53"
        stroke={P.accent}
        strokeWidth="3"
        fill="none"
        opacity={interpolate(f, [43, 50], [0, 1], ease)}
      />
      <text
        x="690"
        y="54"
        fontFamily="Inter"
        fontWeight="700"
        fontSize="36"
        fill={dark ? P.paper : P.olive}
      >
        {labels[1]}
      </text>
    </svg>
  );
};
export const Sound = ({ a, b, n }: { a: string; b: string; n: string }) => {
  const { fps, durationInFrames } = useVideoConfig();
  return (
    <>
      <Audio src={staticFile("audio/sfx-" + n + ".wav")} premountFor={fps} />
      <Sequence name="Música A" durationInFrames={15 * fps} premountFor={fps}>
        <Audio
          src={staticFile("audio/" + a + ".wav")}
          volume={(f) =>
            interpolate(
              f,
              [0, 0.7 * fps, 11 * fps, 15 * fps],
              [0, 0.74, 0.74, 0],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
            )
          }
          premountFor={fps}
        />
      </Sequence>
      <Sequence
        name="Música B — crossfade 4 s"
        from={11 * fps}
        durationInFrames={durationInFrames - 11 * fps}
        premountFor={fps}
      >
        <Audio
          src={staticFile("audio/" + b + ".wav")}
          volume={(f) =>
            interpolate(
              f,
              [
                0,
                4 * fps,
                (durationInFrames / fps - 17) * fps,
                (durationInFrames / fps - 16) * fps,
                (durationInFrames / fps - 12) * fps,
                (durationInFrames / fps - 11) * fps,
              ],
              [0, 0.74, 0.74, 0.93, 0.93, 0],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
            )
          }
          premountFor={fps}
        />
      </Sequence>
    </>
  );
};
