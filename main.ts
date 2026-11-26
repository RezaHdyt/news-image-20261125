// news-image-20261125 entry point: validate the checked-in entry.png and
// copy it to $MAKEFUN_OUTPUT_DIR. Pure Node stdlib; no network, no
// external runtime. The grader runs this with node22 on a read-only /bot,
// so the program only reads the repo and writes to the output directory.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = join(HERE, "entry.png");
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "out";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

if (!existsSync(SRC)) {
  console.error("entry.png not found next to main.ts");
  process.exit(1);
}
const bytes = readFileSync(SRC);
if (bytes.length > 1048576) {
  console.error("entry.png is over the 1 MiB limit: " + bytes.length + " bytes");
  process.exit(1);
}
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  console.error("entry.png is not a PNG file");
  process.exit(1);
}
// The gate also caps dimensions at 1024x1024: read them from the IHDR
// chunk (width at bytes 16-19, height at bytes 20-23, big-endian).
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  console.error("entry.png is over the 1024x1024 limit: " + width + "x" + height);
  process.exit(1);
}
// A whole PNG must end with its IEND chunk (12 bytes: length 0, the
// "IEND" tag, and its CRC). Reject a truncated file instead of copying
// a partial image to the output directory.
const IEND = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);
if (!bytes.subarray(bytes.length - 12).equals(IEND)) {
  console.error("entry.png is truncated: missing IEND chunk");
  process.exit(1);
}
mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, join(OUT_DIR, "entry.png"));
console.log("copied entry.png (" + bytes.length + " bytes) to " + OUT_DIR);
