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
const context = vm.createContext({ encodeURIComponent });
vm.runInContext(
  `${helpers}\nthis.addAudioVersion = typeof addAudioVersion === "function" ? addAudioVersion : undefined;`,
  context
);

test("regenerated audio gets a cache-busting timing version", () => {
  assert.equal(typeof context.addAudioVersion, "function");
  assert.equal(context.addAudioVersion("phrase.mp3", "abc-t2"), "phrase.mp3?v=abc-t2");
  assert.equal(context.addAudioVersion("phrase.mp3?x=1", "abc-t2"), "phrase.mp3?x=1&v=abc-t2");
});
