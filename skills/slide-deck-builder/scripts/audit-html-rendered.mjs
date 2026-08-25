#!/usr/bin/env node
/** Audit computed typography and canvas use in a rendered HTML deck. */

import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const args = process.argv.slice(2);
const input = args[0];
if (!input) {
  console.error("Usage: node audit-html-rendered.mjs <deck.html> [--review review.md] [--against calibration.html]");
  process.exit(2);
}

function option(name) {
  const index = args.indexOf(name);
  return index >= 0 ? args[index + 1] : undefined;
}

const deckPath = resolve(input);
if (!existsSync(deckPath)) {
  console.error(`FAIL: file not found: ${deckPath}`);
  process.exit(2);
}

const chromeCandidates = [
  process.env.CHROME_PATH,
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/Applications/Chromium.app/Contents/MacOS/Chromium",
  "/usr/bin/google-chrome",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser",
].filter(Boolean);
const chrome = chromeCandidates.find(existsSync);
if (!chrome) {
  console.error("FAIL: Chrome or Chromium was not found. Set CHROME_PATH to its executable.");
  process.exit(2);
}

function auditPage() {
  const slides = [...document.querySelectorAll(".slide")];
  const stage = document.querySelector("#stage, .stage, .stage-frame");
  if (!slides.length || !stage) return { fatal: "Expected .slide elements and a stage container" };
  const visible = (el) => {
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0;
  };
  const ownText = (el) => [...el.childNodes].some((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim());
  const auxiliarySelector = ".foot,.footer,.counter,.slide-no,.pagenum,.page-number,.presenter-cue,.eyebrow,.kicker,.token";
  const chromeSelector = `${auxiliarySelector},.logo`;
  const parseColor = (value) => {
    const match = value?.match(/rgba?\(([^)]+)\)/);
    if (!match) return null;
    const parts = match[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    return { r: parts[0], g: parts[1], b: parts[2], a: parts[3] ?? 1 };
  };
  const blend = (front, back) => ({
    r: front.r * front.a + back.r * (1 - front.a),
    g: front.g * front.a + back.g * (1 - front.a),
    b: front.b * front.a + back.b * (1 - front.a),
    a: 1,
  });
  const luminance = ({ r, g, b }) => {
    const channel = (value) => {
      const normal = value / 255;
      return normal <= 0.03928 ? normal / 12.92 : ((normal + 0.055) / 1.055) ** 2.4;
    };
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b);
  };
  const contrast = (a, b) => {
    const values = [luminance(a), luminance(b)].sort((x, y) => y - x);
    return (values[0] + 0.05) / (values[1] + 0.05);
  };
  const backgroundFor = (el) => {
    for (let node = el; node; node = node.parentElement) {
      const colour = parseColor(getComputedStyle(node).backgroundColor);
      if (colour?.a > 0.01) return colour.a < 1 ? blend(colour, { r: 255, g: 255, b: 255, a: 1 }) : colour;
    }
    return { r: 255, g: 255, b: 255, a: 1 };
  };
  const results = [];
  for (const slide of slides) slide.style.transition = "none";
  for (let index = 0; index < slides.length; index += 1) {
    for (const [i, slide] of slides.entries()) {
      slide.classList.toggle("active", i === index);
      slide.style.display = i === index ? "" : "none";
    }
    const slide = slides[index];
    const stageRect = stage.getBoundingClientRect();
    const failures = [];
    const textElements = [...slide.querySelectorAll("*")].filter((el) => visible(el) && ownText(el));
    for (const el of textElements) {
      const text = el.innerText.trim().replace(/\s+/g, " ");
      if (!text) continue;
      const size = parseFloat(getComputedStyle(el).fontSize);
      const style = getComputedStyle(el);
      const auxiliary = Boolean(el.closest(auxiliarySelector));
      const role = el.matches("h1") ? "deck title" : el.matches("h2") ? "slide title" : auxiliary ? "auxiliary" : "body";
      const minimum = role === "deck title" ? 64 : role === "slide title" ? 50 : role === "auxiliary" ? 14 : 22;
      if (size + 0.01 < minimum) failures.push(`${role} “${text.slice(0, 48)}” is ${size}px; minimum ${minimum}px`);
      const foreground = parseColor(style.color);
      if (foreground) {
        const ratio = contrast(foreground.a < 1 ? blend(foreground, backgroundFor(el)) : foreground, backgroundFor(el));
        const large = size >= 24 || (size >= 18.66 && Number(style.fontWeight) >= 700);
        const required = large ? 3 : 4.5;
        if (ratio + 0.01 < required) failures.push(`${role} “${text.slice(0, 48)}” contrast is ${ratio.toFixed(2)}:1; minimum ${required}:1`);
      }
      const rect = el.getBoundingClientRect();
      const tolerance = 1;
      if (rect.left < stageRect.left - tolerance || rect.top < stageRect.top - tolerance || rect.right > stageRect.right + tolerance || rect.bottom > stageRect.bottom + tolerance) {
        failures.push(`text “${text.slice(0, 48)}” extends beyond the stage`);
      }
    }
    for (const image of slide.querySelectorAll("img")) {
      if (!image.complete || !image.naturalWidth) failures.push(`image “${image.getAttribute("src") || image.alt || "unnamed"}” did not load`);
      const rect = image.getBoundingClientRect();
      if (image.naturalWidth && image.naturalHeight && rect.height > 0) {
        const distortion = Math.abs(rect.width / rect.height / (image.naturalWidth / image.naturalHeight) - 1);
        if (distortion > 0.03) failures.push(`image “${image.getAttribute("src") || image.alt || "unnamed"}” is distorted`);
      }
    }
    for (const list of slide.querySelectorAll("ul,ol")) {
      if (list.querySelectorAll(":scope > li").length >= 3 && !list.closest('[data-list-ok="true"]')) failures.push("three-or-more-item list needs a purposeful composition or data-list-ok=\"true\"");
    }
    const content = [...slide.children].filter((el) => visible(el) && !el.matches(chromeSelector));
    if (content.length) {
      const rects = content.map((el) => el.getBoundingClientRect());
      const left = Math.min(...rects.map((r) => r.left));
      const top = Math.min(...rects.map((r) => r.top));
      const right = Math.max(...rects.map((r) => r.right));
      const bottom = Math.max(...rects.map((r) => r.bottom));
      const widthUse = (right - left) / stageRect.width;
      const heightUse = (bottom - top) / stageRect.height;
      if (widthUse < 0.45) failures.push(`main content spans only ${Math.round(widthUse * 100)}% of stage width`);
      if (heightUse < 0.18) failures.push(`main content spans only ${Math.round(heightUse * 100)}% of stage height`);
    }
    results.push({ slide: index + 1, failures });
  }
  return { results };
}

const scratch = mkdtempSync(join(tmpdir(), "slide-audit-"));
const instrumentedPath = join(scratch, "deck.html");
const base = `<base href="${pathToFileURL(`${dirname(deckPath)}/`).href}">`;
const runner = `<script>(()=>{const run=()=>setTimeout(()=>{const result=(${auditPage.toString()})();const marker=document.createElement('meta');marker.id='__slide-audit-results';marker.setAttribute('data-result',encodeURIComponent(JSON.stringify(result)));document.documentElement.appendChild(marker)},50);document.readyState==='complete'?run():addEventListener('load',run,{once:true})})()</script>`;
let source = readFileSync(deckPath, "utf8");
const preflightFailures = [];
const slideSignatures = (html) => [...html.matchAll(/<section\b[^>]*class\s*=\s*["']([^"']*\bslide\b[^"']*)["']/gi)]
  .map((match) => match[1].split(/\s+/).filter((name) => name && name !== "active" && name !== "slide").sort().join("."));

const reviewInput = option("--review");
if (reviewInput) {
  const reviewPath = resolve(reviewInput);
  if (!existsSync(reviewPath)) {
    preflightFailures.push(`review file not found: ${reviewPath}`);
  } else {
    const rows = readFileSync(reviewPath, "utf8").split(/\r?\n/).map((line) => line.trim())
      .filter((line) => /^\|?\s*\d+\s*\|/.test(line))
      .map((line) => line.replace(/^\|/, "").replace(/\|$/, "").split("|").map((cell) => cell.trim()));
    const expected = slideSignatures(source).length;
    for (let slide = 1; slide <= expected; slide += 1) {
      const row = rows.find((cells) => Number(cells[0]) === slide);
      if (!row || row.length < 4 || row.slice(1, 4).some((cell) => !cell)) preflightFailures.push(`review row ${slide} is missing finding, action or verified evidence`);
      else {
        const finding = row[1].toLowerCase();
        const missing = ["hierarchy", "legibility", "silhouette", "accuracy"].filter((term) => !finding.includes(term));
        if (!/canvas|whitespace/.test(finding)) missing.push("canvas/whitespace");
        if (missing.length) preflightFailures.push(`review row ${slide} does not cover ${missing.join(", ")}`);
        if (!/verified|pass|resolved|yes/i.test(row[3])) preflightFailures.push(`review row ${slide} is not verified`);
      }
    }
  }
}

const againstInput = option("--against");
if (againstInput) {
  const againstPath = resolve(againstInput);
  if (!existsSync(againstPath)) {
    preflightFailures.push(`comparison deck not found: ${againstPath}`);
  } else {
    const generated = slideSignatures(source);
    const reference = slideSignatures(readFileSync(againstPath, "utf8"));
    const remaining = [...reference];
    const overlap = generated.reduce((count, signature) => {
      const index = remaining.indexOf(signature);
      if (index < 0) return count;
      remaining.splice(index, 1);
      return count + 1;
    }, 0);
    const basis = Math.min(generated.length, reference.length);
    if (basis >= 4 && overlap / basis >= 0.75) preflightFailures.push(`layout sequence reuses ${overlap} of ${basis} calibration silhouettes`);
  }
}
source = source.includes("<head>") ? source.replace("<head>", `<head>${base}`) : `${base}${source}`;
source = source.includes("</body>") ? source.replace("</body>", `${runner}</body>`) : `${source}${runner}`;
writeFileSync(instrumentedPath, source);

try {
  const rendered = spawnSync(chrome, [
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--window-size=1280,720",
    "--virtual-time-budget=1000",
    "--dump-dom",
    pathToFileURL(instrumentedPath).href,
  ], { encoding: "utf8", maxBuffer: 20 * 1024 * 1024 });
  if (rendered.error || rendered.status !== 0) {
    console.error(`FAIL: Chrome could not render the deck${rendered.error ? `: ${rendered.error.message}` : ""}`);
    process.exitCode = 2;
  } else {
    const marker = rendered.stdout.match(/<meta[^>]*id="__slide-audit-results"[^>]*>/)?.[0];
    const encoded = marker?.match(/data-result="([^"]+)"/)?.[1];
    if (!encoded) {
      console.error("FAIL: rendered audit result was not produced");
      process.exitCode = 2;
    } else {
      const result = JSON.parse(decodeURIComponent(encoded.replaceAll("&amp;", "&")));
      if (result.fatal) {
        console.error(`FAIL: ${result.fatal}`);
        process.exitCode = 1;
      } else {
        const failures = [...preflightFailures, ...result.results.flatMap((slide) => slide.failures.map((failure) => `slide ${slide.slide}: ${failure}`))];
        if (failures.length) {
          for (const failure of failures) console.error(`FAIL: ${basename(deckPath)} ${failure}`);
          process.exitCode = 1;
        } else {
          console.log("PASS: rendered HTML quality audit");
        }
      }
    }
  }
} finally {
  rmSync(scratch, { recursive: true, force: true });
}
