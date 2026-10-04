"use strict";
const el = (id) => document.getElementById(id);
let connection = null;
let busy = false;
const message = (text) => { el("message").textContent = text; };

async function request(path, options) {
  const response = await fetch(path, { ...options, cache: "no-store", credentials: "omit" });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || "Request failed. Please try again.");
  return result;
}

async function run(action) {
  if (busy) return;
  busy = true;
  document.querySelectorAll("button").forEach((button) => { button.disabled = true; });
  message("");
  try { await action(); } catch (error) { message(error.message || "Unable to connect. Please try again."); }
  finally {
    busy = false;
    document.querySelectorAll("button").forEach((button) => { button.disabled = false; });
  }
}

function showKey(result) {
  connection = { mcp_url: result.mcp_url, user_id: result.user_id, bearer_key: result.api_key };
  el("new-key").value = result.api_key;
  el("mcp-url").value = result.mcp_url;
  el("signup-panel").hidden = true;
  el("result-panel").hidden = false;
  el("existing-key").value = "";
}

el("signup-form").addEventListener("submit", (event) => {
  event.preventDefault();
  run(async () => showKey(await request("/api/signup", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ display_name: el("display-name").value.trim() }),
  })));
});

el("copy-key").addEventListener("click", () => run(async () => {
  await navigator.clipboard.writeText(connection.bearer_key);
  message("Key copied. Save it somewhere private.");
}));
el("download").addEventListener("click", () => {
  if (!connection) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(connection, null, 2) + "\n"], { type: "application/json" }));
  const link = document.createElement("a"); link.href = url; link.download = "deepagentlabs-mcp.json"; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

async function account(method) {
  const token = el("existing-key").value.trim();
  if (!token) throw new Error("Paste your current MCP key first.");
  return request("/api/account", { method, headers: { Authorization: "Bearer " + token } });
}
el("inspect").addEventListener("click", () => run(async () => {
  const result = await account("GET");
  el("account-info").textContent = result.display_name + " · User ID: " + result.user_id;
}));
el("rotate").addEventListener("click", () => {
  if (confirm("Replace your current key? The old key will stop working immediately. Save the new key and update your MCP clients.")) {
    run(async () => { showKey(await account("POST")); message("Key replaced. Your user identity and sessions are preserved."); });
  }
});
el("revoke").addEventListener("click", () => {
  if (confirm("Permanently revoke this key? You will lose access to this account and its sessions.")) {
    run(async () => {
      await account("DELETE"); el("existing-key").value = "";
      connection = null; el("new-key").value = ""; el("result-panel").hidden = true;
      el("signup-panel").hidden = false; el("account-info").textContent = "";
      message("Key revoked. This account can no longer access MCP.");
    });
  }
});
