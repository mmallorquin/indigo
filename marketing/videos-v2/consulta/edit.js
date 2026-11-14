// Re-running this whole-edit script replaces its timeline.
/** @type {import("./fable").BuildScript} */
export default async function edit({ project, text, rect }) {
  const p = await project({ size: "1080x1920", fps: 30, background: "#0b0b10" });
  p.compose([
    text("It renders.", { x: 162, y: 730,
      width: 756, fontSize: 269, color: "#f4f4f5",
      animate: [{ property: "opacity", from: 0, to: 1, duration: 0.9, easing: "house" }] }),
    rect({ x: 162, y: 1152, width: 238, height: 6, fill: "#ff6a2b",
      animate: [{ property: "scaleX", from: 0, to: 1, at: 0.5, duration: 0.7, easing: "house" }] }),
  ], { dur: 4 });
  await p.frame(1.2, "renders/first.png");
  await p.render("renders/first.mp4");
}
