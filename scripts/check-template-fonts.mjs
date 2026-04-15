#!/usr/bin/env node
// Verifies whether the DILS pitch template has fonts properly embedded.
// Reads the embeddedFontLst section to map typefaces to embedded files.
//
// Usage:
//   node scripts/check-template-fonts.mjs
//   node scripts/check-template-fonts.mjs "path/to/other.pptx"

import fs from "fs";
import path from "path";
import { execSync } from "child_process";

const DEFAULT_TEMPLATE = "C:/Users/NoahMaatoke_exjgg4d/OneDrive - Dils SpA/Empty Page - Dils Style.pptx";
const target = process.argv[2] ?? DEFAULT_TEMPLATE;

if (!fs.existsSync(target)) {
  console.error(`❌ File not found: ${target}`);
  process.exit(1);
}

console.log(`\n🔍 Checking: ${path.basename(target)}\n`);

let entries;
try {
  entries = execSync(`unzip -l "${target}"`, { encoding: "utf8" });
} catch {
  console.error("❌ unzip not found. Use Git Bash or install it.");
  process.exit(1);
}

// 1. Embedded font files in the ZIP
const fontFiles = entries.split("\n")
  .filter((l) => /ppt\/fonts\/[^\/]+\.(fntdata|ttf|otf)/i.test(l))
  .map((l) => l.trim().split(/\s+/).pop());

// 2. Read presentation.xml to get the official typeface → file mapping
const presentationXml = execSync(`unzip -p "${target}" ppt/presentation.xml`, { encoding: "utf8" });
const embedFlag = /embedTrueTypeFonts\s*=\s*"1"/i.test(presentationXml);

// Parse <p:embeddedFontLst>...<p:embeddedFont><p:font typeface="X"/><p:regular r:id="rId1"/>...
const embedded = []; // {typeface, variants:["regular","bold","italic","boldItalic"]}
const fontBlocks = presentationXml.match(/<p:embeddedFont>[\s\S]*?<\/p:embeddedFont>/g) ?? [];
for (const block of fontBlocks) {
  const t = block.match(/typeface="([^"]+)"/);
  if (!t) continue;
  const variants = [];
  if (/<p:regular[\s/]/.test(block)) variants.push("regular");
  if (/<p:bold[\s/]/.test(block)) variants.push("bold");
  if (/<p:italic[\s/]/.test(block)) variants.push("italic");
  if (/<p:boldItalic[\s/]/.test(block)) variants.push("boldItalic");
  embedded.push({ typeface: t[1], variants });
}

// 3. Collect all unique fonts referenced in slide XML
const slideXmls = entries.split("\n")
  .filter((l) => /ppt\/slides\/slide\d+\.xml$/i.test(l))
  .map((l) => l.trim().split(/\s+/).pop())
  .filter(Boolean);

const referenced = new Set();
for (const xmlPath of slideXmls) {
  try {
    const xml = execSync(`unzip -p "${target}" "${xmlPath}"`, { encoding: "utf8" });
    for (const m of xml.matchAll(/typeface="([^"]+)"/g)) {
      const f = m[1].trim();
      if (f && !f.startsWith("+")) referenced.add(f);
    }
  } catch {}
}

// 4. For each referenced typeface, decide if it's covered by the embedded list
const norm = (s) => s.toLowerCase().replace(/[\s\-_]+/g, "");
const isCovered = (typeface) => {
  const t = norm(typeface);
  return embedded.some((e) => {
    const en = norm(e.typeface);
    return en === t || en.includes(t) || t.includes(en);
  });
};

// 5. Report
console.log("─".repeat(70));
console.log("EMBEDDED FONT BLOCKS (from presentation.xml)");
console.log("─".repeat(70));
if (embedded.length === 0) {
  console.log("  (none declared)");
} else {
  for (const e of embedded) {
    console.log(`  ✅ ${e.typeface.padEnd(35)} variants: ${e.variants.join(", ") || "—"}`);
  }
}

console.log("\n" + "─".repeat(70));
console.log("FONT FILES IN ARCHIVE");
console.log("─".repeat(70));
console.log(`  ${fontFiles.length} file(s) under ppt/fonts/`);
for (const f of fontFiles) console.log(`    • ${f}`);

console.log("\n" + "─".repeat(70));
console.log("FLAG");
console.log("─".repeat(70));
console.log(`  embedTrueTypeFonts = "${embedFlag ? "1" : "0"}"  ${embedFlag ? "✅" : "❌"}`);

console.log("\n" + "─".repeat(70));
console.log("FONTS USED IN SLIDES (and coverage)");
console.log("─".repeat(70));
const sorted = [...referenced].sort();
let uncovered = 0;
for (const f of sorted) {
  const ok = isCovered(f);
  if (!ok) uncovered++;
  console.log(`  ${ok ? "✅ embedded   " : "⚠️  fallback  "} ${f}`);
}

console.log("\n" + "─".repeat(70));
console.log("VERDICT");
console.log("─".repeat(70));
if (embedFlag && fontFiles.length > 0 && uncovered === 0) {
  console.log("  🟢 ALL GOOD — every font on every slide is embedded.");
  console.log("     Decks render correctly on any PC, Mac, or web viewer.\n");
} else if (embedFlag && fontFiles.length > 0 && uncovered > 0) {
  console.log(`  🟡 MOSTLY EMBEDDED — but ${uncovered} typeface(s) will substitute on machines without them:`);
  for (const f of sorted) if (!isCovered(f)) console.log(`     • ${f}`);
  console.log("     (Likely commercial-license restriction OR an unembedded fallback like Calibri / System Font)\n");
} else if (embedFlag && fontFiles.length === 0) {
  console.log("  🟠 FLAG ON BUT NOTHING EMBEDDED — re-save in PowerPoint to actually pack them in.\n");
} else {
  console.log("  🔴 NOT EMBEDDED — fonts will substitute on every machine without them.");
  console.log("     Fix in PowerPoint: File → Options → Save → tick 'Embed fonts in the file'.\n");
}
