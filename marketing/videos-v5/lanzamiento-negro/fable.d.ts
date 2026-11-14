// Type declarations for a fable edit script. Reference from a jsconfig.json (or
// `// @ts-check` plus a JSDoc cast) to get autocomplete and typechecking on the
// build API — the three silently-swallowed project() call shapes this API has
// already seen were all typing-time errors.
//
//   /** @type {import("./fable").BuildScript} */
//   export default async ({ project }) => {
//     const p = await project({ size: "1920x1080", fps: 30 });
//     ...
//   };

export interface Handle {
  readonly id: string;
  readonly name: string;
  /** Project-relative path to the imported native media. */
  readonly uri: string;
  readonly duration: number | null;
  readonly width: number | null;
  readonly height: number | null;
}

export type JsonValue = string | number | boolean | null | readonly JsonValue[] | JsonObject;

export interface JsonObject {
  readonly [key: string]: JsonValue;
}

export interface FrameReport {
  readonly time: number;
  readonly out: string;
  readonly byteSize: number;
  readonly width: number;
  readonly height: number;
  readonly renderMs: number;
  readonly diagnostics: readonly string[];
}

export interface RenderReport {
  readonly ok: true;
  readonly path: string;
  readonly frames: number;
  readonly durationSeconds: number;
  readonly diagnostics: readonly string[];
  /** Depth-10 windows that used the 8-bit compositor, with reasons. */
  readonly fallbacks: readonly string[];
  readonly backend: "cpu" | "gpu";
}

export interface CutOptions {
  /** Where to start inside the source file, in seconds. Defaults to 0. */
  from?: number;
  /** How long to play. Defaults to the rest of the source. */
  dur?: number;
  /** Absolute position on the timeline. Defaults to the end of the last cut. */
  at?: number;
  /** "cover" (default) fills the frame and crops; "contain" fits inside it. */
  fit?: "cover" | "contain" | "fill";
}

export interface RenderOptions {
  draft?: boolean;
  /** Native frame-window count. Defaults from timeline length and available workers; 1 disables splitting. */
  shards?: number;
  /** Native worker processes in flight. Defaults from CPU and memory capacity. */
  concurrency?: number;
  /**
   * 10 = HEVC Main10 where video assets never pass through the 8-bit
   * compositor (cuts, pans, zooms, fades, masks, blur; anything else falls
   * back per window and is reported). Node engine only. Default 8.
   */
  depth?: 8 | 10;
  /** With depth 10: x265 lossless instead of CRF 12 — a master that is not compressed, 10-30x the size. */
  lossless?: boolean;
  /**
   * Depth 10 only. "auto" (default) composites and encodes on an NVIDIA GPU
   * when ffmpeg reaches OpenCL and NVENC, else the CPU path; "cpu"/"gpu" force
   * it (gpu fails loudly without one). The render report names the backend.
   */
  accel?: "auto" | "cpu" | "gpu";
  /**
   * Depth 10 only. "hevc" (default) or "av1": 10-bit AV1 through libsvtav1 on
   * the CPU or NVENC on the GPU — no GPL encoder, royalty-free codec. With
   * lossless the master is FFV1 and the output must be .mkv or .mov.
   */
  codec?: "hevc" | "av1";
  /**
   * Target video bitrate in bits per second. Replaces CRF/CQ with bounded
   * ABR/VBR (`maxrate` = target, `bufsize` = 2x target); it is not CBR or an
   * exact final-size promise. Cannot be combined with lossless.
   */
  bitrate?: number;
}

export interface Project {
  /** Import a media file. Pass the handle to media(); use handle.id for shader texture assetId fields. */
  add(file: string): Promise<Handle>;
  /** Footage on the spine (lane 0), appended in declaration order. */
  cut(file: Handle, options?: CutOptions): void;
  /**
   * A tree of native clips -- text, rects, groups -- as one overlay.
   *
   * No ids: nesting is the parent-child relationship and animation rides on the
   * node it belongs to. Nothing goes near a browser; the compositor draws these.
   */
  compose(nodes: Node | readonly Node[], options: ComposeOptions): void;
  /** Total timeline length so far, in seconds. */
  duration(): number;
  /** Render native pixels at fixed timeline seconds to a PNG (project-relative path); no browser. */
  frame(time: number, out: string): Promise<FrameReport>;
  /** Native export to .mp4/.mov/.mkv (project-relative path); use frame() for PNG. */
  render(out: string, options?: RenderOptions): Promise<RenderReport>;
  /** The persisted document JSON as the renderer sees it. */
  read(): Promise<JsonObject>;
}

export interface ProjectOptions {
  /** Directory to build in. Defaults to the script's own directory. */
  dir?: string;
  /** "1920x1080". Set ONCE at creation — an existing project's size cannot change. */
  size?: string;
  fps?: number;
  /** CSS colour painted behind everything, so hard-cut gaps never flash white. */
  background?: string;
}

/** A value a keyframe can hold: a number, or a CSS colour. */
export type NodeValue = number | string;

/** One animation on one property, local to the node it rides on. */
/** A curve name, or four bezier handles [x1, y1, x2, y2] straight from a design tool. */
export type EasingOption =
  | "house" | "ease-out" | "ease-in" | "ease-in-out" | "smooth" | "linear" | "hold" | "bounce"
  | readonly [number, number, number, number];

export interface NodeKeyframe {
  /** Seconds from the node's own start. */
  at: number;
  value: NodeValue;
  /** The curve LEAVING this keyframe. Defaults to the animation's easing. */
  easing?: EasingOption;
}

export interface NodeAnimation {
  /** opacity, offsetX/Y, positionX/Y, scale, rotation, blur, color, volume, effectParam, ... */
  property: string;
  /** Required with property "effectParam": zero-based index in the node's effects array. */
  effectIndex?: number;
  /** Required with property "effectParam": the numeric effect parameter to animate. */
  effectParam?: string;
  /** The common case: two keyframes. */
  from?: NodeValue;
  to?: NodeValue;
  /** Seconds from the node's own start. Default 0. */
  at?: number;
  duration?: number;
  /**
   * The chain form: any number of keyframes, one track. An entrance and an
   * exit now fit on ONE property, so no wrapper group is needed for that.
   */
  keyframes?: readonly NodeKeyframe[];
  /**
   * Play the chain this many times, each cycle shifted by the chain's span.
   * A loop must end where it starts. It unrolls into explicit keyframes, so
   * a frame stays a pure function of t.
   */
  repeat?: number;
  easing?: EasingOption;
}
/** A drop shadow in scene pixels: { x, y, blur, color }. */
export interface NodeShadow {
  x?: number;
  y?: number;
  blur?: number;
  color?: string;
}

/**
 * A mask box: TOP-LEFT x/y in the node's own pixels (the centre conversion is
 * Fable's job). A reveal is a mask plus an animation on maskWidth/maskHeight.
 */
export interface NodeMask {
  x?: number;
  y?: number;
  /** Box shapes only; a path mask's size is its d. */
  width?: number;
  height?: number;
  // oxlint-disable-next-line anti-slop/no-shape-in-symbol-names -- `shape` is the persisted mask-domain field consumed by compose.
  shape?: "rectangle" | "ellipse" | "path";
  radius?: number;
  feather?: number;
  invert?: boolean;
  /** SVG path data (M/L/H/V/C/Q/Z, no arcs) in the node's own pixels; implies shape "path". */
  d?: string;
}

/**
 * Per-token entrance motion for a text node. One option does the whole thing:
 * it stores the motion and emits the textProgress track that drives it, so a
 * fifty-glyph staggered headline is ONE clip.
 */
export interface TextMotionOptions {
  by: "character" | "word" | "line";
  from?: { opacity?: number; x?: number; y?: number; scale?: number };
  at?: number;
  duration?: number;
  overlap?: number;
  easing?: "linear" | "ease-out" | "house";
}

/** A vector shape: SVG path data (M/L/H/V/C/Q/Z) in the node's own pixels. */
export interface PathOptions extends NodeCommon {
  d: string;
  /** Morph target sharing d's command skeleton; animate morphProgress 0..1. */
  morphTo?: string;
  x?: number;
  y?: number;
  width: number;
  height: number;
  /** A colour or gradient; omit for a pure stroke. */
  fill?: string | GradientOption;
  stroke?: { width: number; color?: string; cap?: "butt" | "round" };
  /** stroke-dasharray in the path's own units. */
  dash?: number[];
}

/** Sampling outside 0..1. Defaults to "clamp". */
export type ShaderTextureWrap = "clamp" | "repeat" | "mirror";
/** Texture interpolation. Defaults to "linear". */
export type ShaderTextureFilter = "linear" | "nearest";

export type ShaderTextureParams = JsonObject & {
  /** The id on the Handle returned by project.add(). URLs are not accepted. */
  readonly assetId: string;
  readonly wrap?: ShaderTextureWrap;
  readonly filter?: ShaderTextureFilter;
};

/** Up to eight named image textures; key `noise` is exposed to GLSL as `u_noise`. */
export type ShaderTextures = Readonly<Record<string, ShaderTextureParams>>;

export type ShaderEffectParams = JsonObject & {
  /** Function source defining `vec4 pixel(vec2 uv)`. The wrapper owns main(). */
  readonly glsl: string;
  readonly textures?: ShaderTextures;
};

export interface ShaderNodeEffect {
  readonly kind: "shader";
  readonly params: ShaderEffectParams;
}

/** One per-node effect: a bare extension id plus its params. */
export interface PluginNodeEffect {
  readonly kind: string;
  readonly params?: JsonObject;
}

/** Custom shaders get typed params; all installed and third-party effect ids remain valid. */
export type NodeEffect = ShaderNodeEffect | PluginNodeEffect;

/** Sequence children only: how this child cuts into the next one — exit + entrance centred on the cut. */
export interface NodeTransition {
  preset?: "fade" | "blur" | "grow" | "shrink" | "slide-left" | "slide-right" | "slide-up" | "slide-down" | "spin" | "twist";
  duration: number;
}

export interface NodeCommon {
  /** What shows of this node. Animate maskWidth/maskHeight for a wipe. */
  mask?: NodeMask;
  /** A drop shadow behind this node. */
  shadow?: NodeShadow;
  /** Per-node effects, applied in order before the shadow. */
  effects?: readonly NodeEffect[];
  /** true or { samples?, shutter? }: geometry sampled across the shutter and averaged. */
  motionBlur?: boolean | { samples?: number; shutter?: number };
  /** How this node's pixels combine with what is beneath it. Default "normal". */
  blendMode?: "normal" | "multiply" | "screen" | "overlay" | "darken" | "lighten" | "color-dodge" | "color-burn" | "hard-light" | "soft-light" | "difference" | "exclusion" | "hue" | "saturation" | "color" | "luminosity";
  /** Depth for the compose call's camera: 0 moves 1:1 with it, larger is farther. Top-level nodes only. */
  z?: number;
  /** Sibling stencil: this node shows only where that sibling has alpha. */
  matte?: string | { source: string; invert?: boolean };
  /** Sequence children only. */
  transition?: NodeTransition;
  /** Defaults to the enclosing beat's start. */
  at?: number;
  /** Defaults to the enclosing beat's length. */
  duration?: number;
  animate?: readonly NodeAnimation[];
}

export interface TextBendOptions {
  readonly amplitude: number;
  readonly wavelength: number;
  /** Radians. */
  readonly phase: number;
  readonly stretch: number;
}

/** Explicit font-byte shaping. Omit it to keep the legacy text path. */
export interface TextTypographyOptions {
  readonly fontAssetId: string;
  readonly axes?: Readonly<Record<string, number>>;
  readonly features?: Readonly<Record<string, number>>;
  readonly script?: string;
  readonly language?: string;
  readonly direction?: "ltr" | "rtl";
  readonly bend?: TextBendOptions | null;
  readonly drawProgress?: number;
}

export interface TextOptions extends NodeCommon {
  typography?: TextTypographyOptions;
  /** Staggered per-token entrance. */
  motion?: TextMotionOptions;
  /** Box left edge. Omit to centre the box in the scene. */
  x?: number;
  /** Box TOP edge — text is anchored top-left, not centred. */
  y?: number;
  /** Wrap width. Defaults to 80% of the scene. */
  width?: number;
  height?: number;
  fontFamily?: string;
  fontSize?: number;
  fontWeight?: number;
  italic?: boolean;
  letterSpacing?: number;
  lineHeight?: number;
  align?: "left" | "center" | "right";
  color?: string;
  /** Outline colour; defaults to `color`. Draw-on needs a visible stroke. */
  strokeColor?: string;
  strokeWidth?: number;
}

/** A stop along a gradient axis. `offset` is 0..1, where 0.5 is halfway. */
export interface GradientStopOption {
  offset: number;
  color: string;
  opacity?: number;
}

/** A gradient fill. `angle` is degrees, and applies to linear gradients only. */
export interface GradientOption {
  kind: "linear" | "radial";
  angle?: number;
  stops: readonly GradientStopOption[];
}

export interface RectOptions extends NodeCommon {
  x?: number;
  y?: number;
  width: number;
  height: number;
  /** A colour string, or a gradient. Overrides `color` when both are given. */
  fill?: string | GradientOption;
  color?: string;
  radius?: number;
  strokeColor?: string;
  strokeWidth?: number;
  opacity?: number;
}

export interface MediaOptions extends NodeCommon {
  /** The handle p.add() returned. Not a path. */
  readonly file: Handle;
  /** Left edge, in scene pixels. */
  readonly x: number;
  /** Top edge, in scene pixels. */
  readonly y: number;
  /** Box width in scene pixels. With fit "width", the height follows the picture. */
  readonly width: number;
  readonly height?: number;
  /** How the picture meets the box. Default "width". */
  readonly fit?: "width" | "contain" | "cover" | "fill";
  /** Corner rounding in DESIGN pixels; the verb converts it. */
  readonly radius?: number;
  /** Where to start inside a video, in source seconds. */
  readonly trimStart?: number;
  /** Silent by default: an overlay should not quietly add a second audio copy. */
  readonly muted?: boolean;
  readonly volume?: number;
}

/**
 * How a layout container sizes and spaces its children.
 *
 * Flex only: no grid, no block, no inline, no percentages, no min/max. Anything
 * else is refused by name rather than ignored.
 */
export interface LayoutOptions extends NodeCommon {
  readonly name?: string;
  /** Where the container's box sits in the scene; children follow from it. */
  readonly x?: number;
  readonly y?: number;
  /** Leave width off and the container is as wide as its widest child. */
  readonly width?: number;
  readonly height?: number;
  /** Space between children, declared once. */
  readonly gap?: number;
  readonly padding?: number | { top?: number; right?: number; bottom?: number; left?: number };
  readonly align?: "start" | "center" | "end" | "stretch";
  readonly justify?: "start" | "center" | "end" | "space-between" | "space-around" | "space-evenly";
  /** Give it a fill and the container is drawn; leave it off and it only measures. */
  readonly fill?: string | GradientOption;
  readonly color?: string;
  readonly radius?: number;
  readonly grow?: number;
  readonly shrink?: number;
  readonly basis?: number;
  readonly marginTop?: number;
  readonly marginRight?: number;
  readonly marginBottom?: number;
  readonly marginLeft?: number;
}

export interface GroupOptions extends NodeCommon {
  name?: string;
}

/** Frame transforms only. x/y are offsets, not layout coordinates. */
export interface MotionPose {
  x?: number;
  y?: number;
  /** Uniform multiplier; do not combine with scaleX/scaleY. Neutral 1. */
  scale?: number;
  scaleX?: number;
  scaleY?: number;
  opacity?: number;
  /** Degrees, neutral 0. */
  rotation?: number;
}

export type MotionPoseRef = MotionPose | string;
export type MotionAt = number | { cue: string; offset?: number };
export type MotionEasing = EasingOption
  | { kind: "steps"; count: number }
  /** Ease-out-back coefficient, default 1.70158; not a percentage. */
  | { kind: "overshoot"; amount?: number }
  /** Endpoint-normalized, sampled spring; defaults: 170 / 26 / 1. */
  | { kind: "spring"; stiffness?: number; damping?: number; mass?: number };

export type MotionPoseChange =
  | { from: MotionPoseRef; to?: MotionPoseRef }
  | { from?: never; to: MotionPoseRef };

export interface MotionTiming {
  /** Positive seconds. Motion spans never silently clip to their frame. */
  duration: number;
  easing?: MotionEasing;
}

export type MotionPhase = MotionTiming & MotionPoseChange & (
  | { anchor?: "start"; at?: MotionAt }
  /** at is a nonnegative lead before the frame end, not a cue. */
  | { anchor: "end"; at?: number }
);

export type MotionExit = MotionTiming & MotionPoseChange & (
  | { anchor?: "end"; at?: number }
  | { anchor: "start"; at?: MotionAt }
);

export type MotionBinding = MotionPoseChange & {
  /** Omit for self; otherwise the unique name of an immediate child frame. */
  target?: string;
  counter?: never;
};

export interface MotionCounterOptions {
  from: number;
  to: number;
  /** Fixed decimal places, integer 0..6. Default 0. */
  decimals?: number;
  /** Single-line strings, each at most 64 characters. */
  prefix?: string;
  suffix?: string;
}

export interface MotionCounterBinding {
  /** Fixed-size layout="none" child frame holding one static full-lifetime text template. */
  target: string;
  /** Bounded native text states; quantizes the WHOLE shared leaf to scene fps, maximum 256 samples. */
  counter: MotionCounterOptions;
  from?: never;
  to?: never;
}

export type MotionTween = MotionTiming & { at?: MotionAt; sequence?: never; parallel?: never; stagger?: never } & (
  | (MotionBinding & { targets?: never })
  /** One progress schedule mapped to all bindings; per-binding timing is invalid. */
  | { targets: readonly (MotionBinding | MotionCounterBinding)[]; target?: never; from?: never; to?: never }
);

/** Composable timing data, independent of the node-tree <sequence> element. */
export type MotionTimeline = MotionTween | ({
  at?: MotionAt;
  duration?: never;
  easing?: never;
  target?: never;
  targets?: never;
  from?: never;
  to?: never;
} & (
  | { sequence: readonly MotionTimeline[]; gap?: number; parallel?: never; stagger?: never; each?: never }
  | { parallel: readonly MotionTimeline[]; sequence?: never; stagger?: never; gap?: never; each?: never }
  | { stagger: readonly MotionTimeline[]; each: number; sequence?: never; parallel?: never; gap?: never }
));

/** Frame-only choreography; text.motion remains TextMotionOptions. */
export interface FrameMotion {
  poses?: Readonly<Record<string, MotionPose>>;
  /** Named beats in this frame's local seconds, not inherited by children. */
  cues?: Readonly<Record<string, number>>;
  enter?: MotionPhase;
  /** Begins after enter by default; omitted from continues the previous pose. */
  settle?: MotionPhase;
  /** Ends at the resolved local lifetime by default. */
  exit?: MotionExit;
  timeline?: MotionTimeline;
}

export interface FrameOptions extends Omit<NodeCommon, "mask"> {
  name?: string;
  motion?: FrameMotion;
  x?: number;
  y?: number;
  width?: number | "fill" | "hug";
  height?: number | "fill" | "hug";
  origin?: "top-left" | "center";
  layout?: "none" | "column" | "row" | "grid";
  columns?: number;
  wrap?: boolean;
  gap?: number;
  rowGap?: number;
  padding?: number | { top?: number; right?: number; bottom?: number; left?: number };
  align?: "start" | "center" | "end";
  justify?: "start" | "center" | "end" | "space-between";
  background?: string | GradientOption;
  radius?: number;
  clip?: boolean;
  reveal?: { from?: "left" | "right" | "top" | "bottom" | "center"; at?: number; duration?: number; easing?: EasingOption };
}

export interface SequenceOptions extends NodeCommon {
  name?: string;
  /** Seconds of hold inserted between children. Defaults to 0. */
  gap?: number;
}

// oxlint-disable-next-line anti-slop/no-unsafe-dictionary-type -- Builders expose authored node fields before compose validates them.
export type Node = Readonly<Record<string, unknown>>;

export interface ComposeOptions {
  /** Seconds. Required: an overlay is a beat, and a beat has a length. */
  dur: number;
  /** Seconds. Defaults to the start of the last cut, or zero before any cut. */
  at?: number;
  /** Names the group several nodes land in. */
  name?: string;
  /** 2.5D camera over the beat's z nodes. */
  camera?: { focal?: number; keyframes: { at: number; x?: number; y?: number; dolly?: number; easing?: string }[] };
}

export interface BuildContext {
  project(options?: ProjectOptions): Promise<Project>;
  /* Handed over, not imported: a project directory has no node_modules. */
  text(content: string, options?: TextOptions): Node;
  rect(options: RectOptions): Node;
  media(options: MediaOptions): Node;
  adjustment(options: AdjustmentOptions): Node;
  /** A vector shape node. */
  path(options: PathOptions): Node;
  group(options: GroupOptions, children: readonly Node[]): Node;
  frame(options: FrameOptions, children?: readonly Node[]): Node;
  /** A measured stack: children are laid out top to bottom, not placed by pixel. */
  column(options: LayoutOptions, children: readonly Node[]): Node;
  /** A measured row: children are laid out left to right. */
  row(options: LayoutOptions, children: readonly Node[]): Node;
  sequence(options: SequenceOptions, children: readonly Node[]): Node;
  /**
   * One built-in lucide icon as a native <path> node (stroke, round caps) —
   * recolorable, animatable, no SVG at edit time. Unknown names throw with
   * the closest matches; search the catalog with `higgsedit icons <query>`.
   */
  icon(name: string, options?: IconOptions): Node;
}

export interface IconOptions extends NodeCommon {
  x?: number;
  y?: number;
  /** Rendered square box in px. Default 48. */
  size?: number;
  /** Stroke colour. Default #ffffff. */
  color?: string;
  /** Stroke width in the icon's 24px design grid (lucide draws 2). Scales with size. */
  strokeWidth?: number;
}

/** The default export of an edit script. */
export type BuildScript = (ctx: BuildContext) => Promise<void> | void;

/*
 * JSX.
 *
 * Elements are lowercase and intrinsic, which is what lets an edit script use
 * them with no imports: a lowercase tag compiles to a string, so there is nothing
 * to resolve from a project directory that has no node_modules.
 *
 * A capitalised tag is an ordinary function taking props and returning a tree --
 * that is how a beat becomes reusable.
 *
 * For a .jsx or .tsx script, point the compiler at this file and set:
 *   "jsx": "react", "jsxFactory": "__fableJsx", "jsxFragmentFactory": "__fableFragment"
 * (the CLI's own transform does this for you; the setting is only so an editor
 * agrees with what runs).
 */
// oxlint-disable-next-line anti-slop/no-unsafe-dictionary-type -- Authored JSX children are validated by the runtime tree parser before composition.
type JsxChildren = Node | string | number | boolean | null | undefined | readonly JsxChildren[];

interface TextElementProps extends TextOptions {
  /** The words. Children win over this, because that is what the author sees. */
  text?: string;
  children?: JsxChildren;
  key?: string | number;
}

interface RectElementProps extends RectOptions {
  key?: string | number;
}

export interface AdjustmentOptions extends NodeCommon {
  name?: string;
  /** Region top-left. Omit the box entirely to grade the whole frame. */
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  /** Rounded corners on the region. */
  radius?: number;
}

interface AdjustmentElementProps extends AdjustmentOptions {}

interface MediaElementProps extends Omit<MediaOptions, "x" | "y" | "width" | "height"> {
  readonly x?: number;
  readonly y?: number;
  /** Omit inside a frame to fill its content box. */
  readonly width?: number | "fill" | "hug";
  readonly height?: number | "fill" | "hug";
  readonly key?: string | number;
}

  interface GroupElementProps extends GroupOptions {
  children?: JsxChildren;
  key?: string | number;
}

interface SequenceElementProps extends SequenceOptions {
  children?: JsxChildren;
  key?: string | number;
}

declare global {
  namespace JSX {
    interface Element extends Node {}
    interface ElementChildrenAttribute {
      children: Record<string, never>;
    }
    type LayoutElementProps = LayoutOptions & { readonly children?: JsxChildren };

    interface IntrinsicElements {
      /** Type, wrapped against its own box. Newlines are hard breaks. */
      text: TextElementProps;
      /** A filled box: a panel, a rule, a scrim behind type. */
      rect: RectElementProps;
      /** Wraps nodes so ONE transform and one set of keyframes moves all of them. */
      media: MediaElementProps;
      adjustment: AdjustmentElementProps;
      path: PathElementProps;
      group: GroupElementProps;
      frame: FrameOptions & { children?: JsxChildren; key?: string | number };
      /** A measured stack. Children are laid out, so a label that wraps moves
       * everything below it. */
      column: LayoutElementProps;
      /** A measured row, laid out left to right. */
      row: LayoutElementProps;
      /** Lays children end to end: each starts where the previous one ended. */
      sequence: SequenceElementProps;
    }
  }

  /** Installed by `higgsedit build` before an edit script is imported. */
  // oxlint-disable-next-line anti-slop/no-unknown-parameters -- Compiler-emitted JSX values enter the runtime parser through this global boundary.
  const __fableJsx: (kind: unknown, props: unknown, ...children: JsxChildren[]) => Node;
  const __fableFragment: unique symbol;
}

export type PathElementProps = PathOptions & { key?: never };
