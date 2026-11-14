import {
  AbsoluteFill,
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
type Node = {
  type: string;
  x?: number;
  y?: number;
  w?: number;
  h?: number;
  text?: string;
  size?: number;
  color?: string;
  serif?: boolean;
  italic?: boolean;
  weight?: number;
  lh?: number;
  tracking?: number;
  src?: string;
  fit?: string;
  crop?: number[] | null;
  d?: string;
  stroke?: number;
};
export type Layout = {
  id: string;
  bg: string;
  width: number;
  height: number;
  nodes: Node[];
};
const ease = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
  easing: Easing.bezier(0.16, 1, 0.3, 1),
};
export const Artwork = ({
  layout,
  animate = false,
}: {
  layout: Layout;
  animate?: boolean;
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: layout.bg }}>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width={layout.width}
        height={layout.height}
        viewBox={`0 0 ${layout.width} ${layout.height}`}
        style={{ overflow: "hidden" }}
      >
        {layout.nodes.map((n, i) => {
          const f = animate ? frame - (n.type === "photo" ? 3 : 0) : 1000;
          const a = animate
            ? interpolate(
                f,
                [0, 0.55 * fps],
                [n.type === "photo" ? 0.35 : 0.18, 1],
                ease,
              )
            : 1;
          if (n.type === "text")
            return (
              <g
                key={i}
                aria-label={n.text}
                opacity={a}
                fontFamily={n.serif ? "Cormorant" : "Inter"}
                fontWeight={n.serif ? 600 : n.weight}
                fontSize={n.size}
                fontStyle={n.italic ? "italic" : "normal"}
                fill={n.color}
                letterSpacing={
                  animate
                    ? interpolate(
                        f,
                        [0, 0.65 * fps],
                        [(n.tracking ?? 0) + 2.5, n.tracking ?? 0],
                        ease,
                      )
                    : n.tracking
                }
              >
                {(n.text ?? "").split("\n").map((line, k) => {
                  const y = (n.y ?? 0) + k * (n.size ?? 30) * (n.lh ?? 1.05);
                  const id = layout.id + "-" + i + "-" + k;
                  return (
                    <g key={k}>
                      <defs>
                        <clipPath id={id}>
                          <rect
                            x={(n.x ?? 0) - 5}
                            y={y - 15}
                            width={1200 - (n.x ?? 0)}
                            height={
                              animate
                                ? interpolate(
                                    f - k * 3,
                                    [0, 0.55 * fps],
                                    [
                                      (n.size ?? 30) * 0.2,
                                      (n.size ?? 30) * 1.6 + 30,
                                    ],
                                    ease,
                                  )
                                : (n.size ?? 30) * 1.6 + 30
                            }
                          />
                        </clipPath>
                      </defs>
                      <text
                        clipPath={`url(#${id})`}
                        x={n.x}
                        y={
                          y +
                          (n.size ?? 30) * 0.78 +
                          (animate
                            ? interpolate(
                                f - k * 3,
                                [0, 0.6 * fps],
                                [32, 0],
                                ease,
                              )
                            : 0)
                        }
                      >
                        {line}
                      </text>
                    </g>
                  );
                })}
              </g>
            );
          if (n.type === "photo") {
            const crop = n.crop;
            const zoom =
              animate && !crop && n.fit !== "meet"
                ? 1.012 + Math.sin(frame / 100) * 0.008
                : 1;
            return (
              <g
                key={i}
                opacity={a}
                style={{
                  translate: `0 ${animate ? interpolate(f, [0, 0.7 * fps], [32, 0], ease) : 0}px`,
                }}
              >
                <svg
                  x={n.x}
                  y={n.y}
                  width={n.w}
                  height={n.h}
                  viewBox={crop ? crop.join(" ") : `0 0 ${n.w} ${n.h}`}
                  preserveAspectRatio={crop ? "xMidYMid slice" : "none"}
                  overflow="hidden"
                >
                  <image
                    href={staticFile("media/" + n.src)}
                    width={crop ? 1440 : n.w}
                    height={crop ? 1920 : n.h}
                    preserveAspectRatio={"xMidYMid " + (n.fit ?? "slice")}
                    style={{ scale: zoom, transformOrigin: "50% 50%" }}
                  />
                </svg>
              </g>
            );
          }
          if (n.type === "logo")
            return (
              <g key={i}>
                <defs>
                  <clipPath id={layout.id + "-logo-" + i}>
                    <circle
                      cx={(n.x ?? 0) + (n.w ?? 0) / 2}
                      cy={(n.y ?? 0) + (n.h ?? 0) / 2}
                      r={(n.w ?? 0) / 2}
                    />
                  </clipPath>
                </defs>
                <image
                  href={staticFile("brand/logo.jpg")}
                  x={n.x}
                  y={n.y}
                  width={n.w}
                  height={n.h}
                  clipPath={"url(#" + layout.id + "-logo-" + i + ")"}
                />
              </g>
            );
          if (n.type === "rect")
            return (
              <rect
                key={i}
                x={n.x}
                y={n.y}
                width={
                  (n.w ?? 0) *
                  (animate
                    ? interpolate(f, [0, 0.7 * fps], [0.12, 1], ease)
                    : 1)
                }
                height={n.h}
                fill={n.color}
                opacity={a}
              />
            );
          if (n.type === "path")
            return (
              <path
                key={i}
                d={n.d}
                fill="none"
                stroke={n.color}
                strokeWidth={n.stroke}
                opacity={a}
                pathLength={1}
                strokeDasharray="1"
                strokeDashoffset={
                  animate ? interpolate(f, [0, 1.1 * fps], [1, 0], ease) : 0
                }
              />
            );
          return null;
        })}
      </svg>
    </AbsoluteFill>
  );
};
