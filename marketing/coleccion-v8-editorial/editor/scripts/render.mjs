import { bundle } from "@remotion/bundler";
import {
  getCompositions,
  renderMedia,
  renderStill,
  openBrowser,
} from "@remotion/renderer";
import path from "node:path";
const mode = process.argv[2] ?? "stills";
const wanted = process.argv.slice(3);
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const browser = await openBrowser("chrome");
try {
  for (const c of await getCompositions(serveUrl, {
    puppeteerInstance: browser,
  })) {
    if (wanted.length && !wanted.some((x) => c.id.startsWith(x))) continue;
    if (mode === "stills" && /^(Neutros|Pantalones)-0/.test(c.id)) {
      const name = c.id.toLowerCase();
      await renderStill({
        serveUrl,
        composition: c,
        frame: 0,
        output: `../carruseles/${name.split("-")[0]}/${name}.png`,
        puppeteerInstance: browser,
      });
      console.log("PLACA " + name);
    }
    if (mode === "preview" && /^(14|15)-/.test(c.id)) {
      for (const t of [1.5, 5, 9.5, 14.5, 19.5])
        await renderStill({
          serveUrl,
          composition: c,
          frame: Math.round(t * 30),
          output: `../qa/${c.id}-${t}.png`,
          puppeteerInstance: browser,
        });
      console.log("PREVIEW " + c.id);
    }
    if (mode === "render" && /^(14|15)-/.test(c.id)) {
      let last = -1;
      await renderMedia({
        serveUrl,
        composition: c,
        outputLocation: `../work/${c.id}-mix.mp4`,
        codec: "h264",
        crf: 16,
        pixelFormat: "yuv420p",
        colorSpace: "bt709",
        audioCodec: "aac",
        audioBitrate: "320k",
        sampleRate: 48000,
        concurrency: 3,
        imageFormat: "jpeg",
        jpegQuality: 96,
        overwrite: true,
        puppeteerInstance: browser,
        onProgress: (p) => {
          let n = Math.floor(p.progress * 4);
          if (n !== last) {
            last = n;
            console.log(c.id + " " + n * 25 + "%");
          }
        },
      });
      await renderStill({
        serveUrl,
        composition: c,
        frame: 45,
        output: `../portadas/${c.id}.png`,
        puppeteerInstance: browser,
      });
    }
  }
} finally {
  await browser.close({ silent: true });
}
