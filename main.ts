// Saltwater Verdict — news-image-20261124 entry point (Node 22, stdlib only).
// Copies the bundled entry.png to /output/entry.png after validating it:
// whole PNG, at most 1 MiB, exactly 1024x1024. No network, no randomness.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const targetDir = "/output";
const target = join(targetDir, "entry.png");

const MAX_BYTES = 1024 * 1024;
const WANT_W = 1024;
const WANT_H = 1024;

const data = readFileSync(source);
const size = statSync(source).size;
if (size !== data.length) throw new Error("entry.png changed while reading");
if (size > MAX_BYTES) throw new Error(`entry.png is ${size} bytes, over 1 MiB`);

// PNG signature + IHDR dimensions (bytes 16..23, big-endian uint32).
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (data.length < 33 || !data.subarray(0, 8).equals(PNG_SIG)) {
  throw new Error("entry.png is not a PNG file");
}
if (data.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error("entry.png has no IHDR chunk");
}
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width !== WANT_W || height !== WANT_H) {
  throw new Error(`entry.png is ${width}x${height}, want 1024x1024`);
}

mkdirSync(targetDir, { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target} (${size} bytes, ${width}x${height})`);
