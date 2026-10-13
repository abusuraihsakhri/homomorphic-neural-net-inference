"use strict";

/** Mirrors the threshold rules in agents/workers.py, without claiming to run Python or HE. */
function evaluateRules(p) {
  const a = Number(p.primary_metric), b = Number(p.secondary_metric);
  if (!Number.isFinite(a) || !Number.isFinite(b)) {
    throw new Error("Metrics must be finite numbers.");
  }
  if (!p.task_id || !p.target_identifier || !p.status_descriptor) {
    throw new Error("Task ID, target identifier, and status descriptor are required.");
  }
  const alerts = [];
  const add = (origin_worker, urgency, summary) => alerts.push({ origin_worker, urgency, summary });
  if (a > 25) add("InvariantQCWorker", "ELEVATED_RISK", "Primary metric exceeds 25");
  if (p.is_critical_flag || b > 12) {
    add("SafetyEscalationWorker", p.is_critical_flag ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK",
      "Critical flag is set or secondary metric exceeds 12");
  }
  if (["DISCORDANT","ANOMALY","MUTANT","VIOLATION","FAIL","REJECT"]
    .some(term => String(p.status_descriptor).toUpperCase().includes(term))) {
    add("ProtocolConformanceWorker", "ELEVATED_RISK", "Status descriptor matches a flagged term");
  }
  const critical = alerts.filter(alert => alert.urgency === "CRITICAL_STAT_PANIC").length;
  const overall = critical ? "CRITICAL_STAT_PANIC" : alerts.length ? "ELEVATED_RISK" : "ROUTINE";
  return {
    mode: "local_rules_demo",
    task_id: String(p.task_id),
    target_identifier: String(p.target_identifier),
    overall_urgency: overall,
    integrity_status: critical ? "RECALIBRATION_REQUIRED" :
      alerts.length ? "DISCORDANT_ANOMALY" : "VALIDATED_OPTIMAL",
    total_alerts: alerts.length,
    critical_alerts_count: critical,
    alerts,
    disclaimer: "Threshold demonstration only. No encrypted inference or clinical validation."
  };
}
if (typeof module !== "undefined" && module.exports) module.exports = { evaluateRules };

if (typeof document !== "undefined") {
  let latest = null, runs = 0;
  const byId = id => document.getElementById(id);
  byId("audit-form").addEventListener("submit", event => {
    event.preventDefault();
    byId("error").textContent = "";
    try {
      const value = id => byId(id).value.trim();
      const record = {
        task_id: value("task_id"),
        target_identifier: value("target_identifier"),
        primary_metric: Number(value("primary_metric")),
        secondary_metric: Number(value("secondary_metric")),
        status_descriptor: value("status_descriptor"),
        is_critical_flag: byId("is_critical_flag").checked
      };
      // This page intentionally does not submit or store input outside memory.
      latest = evaluateRules(record);
      runs++;
      byId("empty-state").hidden = true;
      byId("results").hidden = false;
      byId("urgency").textContent = latest.overall_urgency;
      byId("alert-count").textContent = String(latest.total_alerts);
      byId("run-count").textContent = String(runs);
      const list = byId("alerts");
      list.replaceChildren();
      if (!latest.alerts.length) {
        const item = document.createElement("li");
        item.textContent = "No threshold rules triggered.";
        list.append(item);
      }
      latest.alerts.forEach(alert => {
        const item = document.createElement("li");
        item.textContent = alert.origin_worker + " (" + alert.urgency + "): " + alert.summary;
        list.append(item);
      });
      byId("json-result").textContent = JSON.stringify(latest, null, 2);
      byId("download").disabled = false;
    } catch (error) {
      byId("error").textContent = error.message;
    }
  });
  byId("download").addEventListener("click", () => {
    if (!latest) return;
    const blob = new Blob([JSON.stringify(latest, null, 2) + "\n"], {type:"application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "rule-evaluation.json";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
}
