"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { evaluateRules } = require("./app.js");
const base = { task_id: "T1", target_identifier: "SYNTHETIC", primary_metric: 25,
  secondary_metric: 12, status_descriptor: "NOMINAL", is_critical_flag: false };

test("boundary values are nominal", () => {
  const r = evaluateRules(base);
  assert.equal(r.overall_urgency, "ROUTINE");
  assert.equal(r.total_alerts, 0);
});
test("strictly greater boundaries trigger warnings", () => {
  const r = evaluateRules({...base, primary_metric:25.1, secondary_metric:12.1});
  assert.equal(r.total_alerts, 2);
  assert.equal(r.overall_urgency, "ELEVATED_RISK");
});
test("critical flag takes precedence", () => {
  const r = evaluateRules({...base, is_critical_flag:true, status_descriptor:"FAIL"});
  assert.equal(r.overall_urgency, "CRITICAL_STAT_PANIC");
  assert.equal(r.critical_alerts_count, 1);
});
test("nonfinite metric values are rejected", () => {
  assert.throws(() => evaluateRules({...base, primary_metric:Infinity}), /finite/);
  assert.throws(() => evaluateRules({...base, secondary_metric:NaN}), /finite/);
});
test("descriptor matching is case insensitive", () => {
  assert.equal(evaluateRules({...base,status_descriptor:"discordant"}).total_alerts,1);
});
