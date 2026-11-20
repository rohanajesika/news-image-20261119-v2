// main.ts — entrypoint for the news-image-20261119 v2 entry.
//
// The front page (entry.png) was drawn during the build session by
// compose_v2.py from 50 news stories verified first reported on
// Thursday 19 November 2026 (UTC); see news-image-20261119-v2-research.md
// in the builder's notes for the sourcing. This program only copies that
// image to /output/entry.png, after checking it against the competition
// gate: a whole PNG, at most 1 MiB, at most 1024 by 1024 pixels.
// It runs with no network and writes the same bytes on every run.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = join(HERE, "entry.png");
const OUT_DIR = "/output";
const OUT = join(OUT_DIR, "entry.png");

function fail(msg: string): never {
  console.error("main.ts: " + msg);
  process.exit(1);
}

let buf: Buffer;
try {
  buf = readFileSync(SRC);
} catch {
  fail(`cannot read ${SRC} — is entry.png in the repository root?`);
}

// PNG signature: 89 50 4E 47 0D 0A 1A 0A
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < PNG_MAGIC.length; i++) {
  if (buf[i] !== PNG_MAGIC[i]) fail("entry.png is not a PNG file");
}

// IHDR must follow: width at bytes 16-19, height at bytes 20-23.
if (buf.length < 24 || buf.toString("ascii", 12, 16) !== "IHDR") {
  fail("entry.png has no IHDR chunk");
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  fail(`image is ${width}x${height}, over the 1024x1024 limit`);
}
if (buf.length > 1048576) {
  fail(`image is ${buf.length} bytes, over the 1 MiB limit`);
}

// Whole image: the file must end with the IEND chunk.
const IEND = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);
if (buf.length < 12 || !buf.subarray(buf.length - 12).equals(IEND)) {
  fail("entry.png does not end with a valid IEND chunk");
}

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, OUT);

const back = readFileSync(OUT);
if (!back.equals(buf)) fail("copied file differs from entry.png");

console.log(`wrote ${OUT}: ${width}x${height}, ${buf.length} bytes`);
