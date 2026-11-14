import { bundle } from "@remotion/bundler";
import {
  getCompositions,
  renderMedia,
  renderStill,
  openBrowser,
} from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";
const mode = process.argv[2] || "preview";
const wanted = process.argv.slice(3);
const serveUrl = await bundle({
  entryPoint: path.resolve("src/index.ts"),
  webpackOverride: (c) => c,
});
const browser = await openBrowser("chrome");
const comps = (
  await getCompositions(serveUrl, { puppeteerInstance: browser })
).filter(
  (c) =>
    /^\d\d-/.test(c.id) &&
    (!wanted.length || wanted.some((w) => c.id.startsWith(w))),
);
for (const comp of comps) {
  const name = comp.id.toLowerCase();
  if (mode === "preview") {
    for (const seconds of [
      ["05", "06", "07"].some((n) => comp.id.startsWith(n)) ? 1 : 1.5,
      6.5,
      11.5,
      comp.durationInFrames / 30 - 1.5,
    ]) {
      await renderStill({
        serveUrl,
        composition: comp,
        output: `../qa/${name}-${seconds}.jpg`,
        frame: Math.round(seconds * 30),
        imageFormat: "jpeg",
        jpegQuality: 90,
        scale: 0.5,
        puppeteerInstance: browser,
      });
    }
    console.log("PREVIEW " + comp.id);
  } else {
    let pct = -1;
    await renderMedia({
      serveUrl,
      composition: comp,
      codec: "h264",
      crf: 19,
      pixelFormat: "yuv420p",
      audioCodec: "aac",
      audioBitrate: "192k",
      outputLocation: `../finales/${name}.mp4`,
      overwrite: true,
      concurrency: 3,
      imageFormat: "jpeg",
      jpegQuality: 95,
      puppeteerInstance: browser,
      onProgress: (p) => {
        const n = Math.floor(p.progress * 4);
        if (n !== pct) {
          pct = n;
          console.log(comp.id + " " + n * 25 + "%");
        }
      },
    });
    await renderStill({
      serveUrl,
      composition: comp,
      output: `../portadas/${name}.jpg`,
      frame: ["05", "06", "07"].some((n) => comp.id.startsWith(n)) ? 36 : 60,
      imageFormat: "jpeg",
      jpegQuality: 95,
      puppeteerInstance: browser,
    });
    console.log("FINAL " + comp.id);
  }
}
await browser.close({ silent: true });
