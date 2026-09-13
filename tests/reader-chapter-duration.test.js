"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const source = fs.readFileSync(path.join(__dirname, "../reader.js"), "utf8");
const helpers = source.slice(
  source.indexOf("  function showAudioError()"),
  source.indexOf("  function loadChapterTimelines()")
);
const context = vm.createContext({});
vm.runInContext(
  `${helpers}\nthis.formatChapterDuration = typeof formatChapterDuration === "function" ? formatChapterDuration : undefined;`,
  context
);

test("chapter duration is shown as rounded minutes and seconds", () => {
  assert.equal(typeof context.formatChapterDuration, "function");
  assert.equal(context.formatChapterDuration(452.592), "7:33");
  assert.equal(context.formatChapterDuration(339.864), "5:40");
});

test("missing chapter duration stays hidden", () => {
  assert.equal(context.formatChapterDuration(), "");
  assert.equal(context.formatChapterDuration(0), "");
});
