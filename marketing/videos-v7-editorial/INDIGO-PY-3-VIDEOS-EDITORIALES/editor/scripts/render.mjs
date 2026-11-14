import { bundle } from "@remotion/bundler";
import {
  getCompositions,
  renderMedia,
  renderStill,
  openBrowser,
} from "@remotion/renderer";
import path from "node:path";
const mode = process.argv[2] ?? "preview";
const wanted = process.argv.slice(3);
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const browser = await openBrowser("chrome");
const comps = (
  await getCompositions(serveUrl, { puppeteerInstance: browser })
).filter((c) => !wanted.length || wanted.some((n) => c.id.startsWith(n)));
for (const c of comps) {
  const name = c.id.toLowerCase();
  if (mode === "preview") {
    const secs = c.id.startsWith("11")
      ? [1.5, 6, 12, 17, 23, 28]
      : c.id.startsWith("12")
        ? [1.5, 6, 12, 18, 23, 28]
        : [1.5, 6, 12, 18, 24, 29];
    for (const t of secs)
      await renderStill({
        serveUrl,
        composition: c,
        output: `../qa/${name}-${t}.jpg`,
        frame: Math.round(t * 30),
        imageFormat: "jpeg",
        jpegQuality: 94,
        scale: 1,
        puppeteerInstance: browser,
      });
    console.log("PREVIEW " + c.id);
  } else {
    let prev = -1;
    await renderMedia({
      serveUrl,
      composition: c,
      outputLocation: `../work/${name}-mix.mp4`,
      codec: "h264",
      crf: 16,
      pixelFormat: "yuv420p",
      colorSpace: "bt709",
      audioCodec: "aac",
      audioBitrate: "320k",
      sampleRate: 48000,
      concurrency: 3,
      jpegQuality: 95,
      imageFormat: "jpeg",
      overwrite: true,
      puppeteerInstance: browser,
      onProgress: (p) => {
        let n = Math.floor(p.progress * 4);
        if (n !== prev) {
          prev = n;
          console.log(c.id + " " + n * 25 + "%");
        }
      },
    });
    await renderStill({
      serveUrl,
      composition: c,
      output: `../portadas/${name}.jpg`,
      frame: 45,
      imageFormat: "jpeg",
      jpegQuality: 95,
      puppeteerInstance: browser,
    });
    console.log("RENDER " + c.id);
  }
}
await browser.close({ silent: true });
