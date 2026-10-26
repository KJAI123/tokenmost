/* TokenMost 羊毛助手 popup 逻辑：今日羊毛 + 托管账号 + 一键填充（chrome.scripting 注入 fill-core） */
const $ = (id) => document.getElementById(id);
let SITE = "https://tokenmost.com";

function tip(msg) {
  const t = $("tip");
  t.textContent = msg;
  t.style.display = "block";
  setTimeout(() => (t.style.display = "none"), 1600);
}
function esc(s) { return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function api(path) { return SITE.replace(/\/+$/, "") + path; }

chrome.storage.local.get(["cfg", "accs"], ({ cfg, accs }) => {
  if (cfg && cfg.site) SITE = cfg.site;
  $("p-site-url").value = SITE;
  renderAccs(accs || []);
  loadDeals();
  loadSites();
});

function save(accs) { chrome.storage.local.set({ accs, cfg: { site: SITE } }); }

/* ---- 今日羊毛 ---- */
async function loadDeals() {
  try {
    const r = await fetch(api("/deals.json"));
    const deals = await r.json();
    const top = deals
      .filter((d) => d.published !== false && d.verify_status === "verified")
      .sort((a, b) => new Date(b.verified_at) - new Date(a.verified_at))
      .slice(0, 3);
    $("dealsList").innerHTML = top.length
      ? top.map((d) => `<div class="deal" data-url="${esc(d.url)}"><b>${esc(d.provider)}</b><span>${esc(d.value.slice(0, 60))}</span></div>`).join("")
      : '<div class="empty">没有可显示的情报</div>';
  } catch (_) {
    $("dealsList").innerHTML = '<div class="empty">拉取失败——在下方把站点地址改成你的部署地址（如 https://xxx.github.io/tokenmost）</div>';
  }
}
$("dealsList").addEventListener("click", (e) => {
  const d = e.target.closest("[data-url]");
  if (d) chrome.tabs.create({ url: d.dataset.url });
});

/* ---- 平台下拉（来自站点 sites.json） ---- */
async function loadSites() {
  try {
    const r = await fetch(api("/sites.json"));
    const groups = await r.json();
    const names = groups.flatMap((g) => g.sites.map((s) => s.name));
    $("p-site").innerHTML = '<option value="">— 平台 —</option>' + names.map((n) => `<option>${esc(n)}</option>`).join("");
  } catch (_) { /* 站点未配好时手填平台名也行（input 语义由 select 提供常见项） */ }
}

/* ---- 托管账号 ---- */
function renderAccs(list) {
  if (!list.length) {
    $("accList").innerHTML = '<div class="empty">还没有托管。填左侧表单添加，或导入 tokenmost 网站账号库的备份 json。</div>';
    return;
  }
  $("accList").innerHTML = list.map((a, i) => `
    <div class="acc">
      <div class="t">${esc(a.site)}<small>${esc(a.account || "")}${a.pass ? " 🔑" : ""}</small></div>
      <div class="ops">
        <button class="fill" data-fill="${i}">✍️ 填充本页</button>
        <button data-copy="${i}">复制账号</button>
        <a class="go" data-open="${i}" href="#">直达登录</a>
        <button class="del" data-del="${i}">删</button>
      </div>
    </div>`).join("");
  window.__accs = list;
}

$("accList").addEventListener("click", async (e) => {
  const list = window.__accs || [];
  const open = e.target.closest("[data-open]");
  if (open) {
    const acc = list[+open.dataset.open];
    const { SITES } = await loadSitesData();
    const s = SITES.flatMap((g) => g.sites).find((x) => x.name === acc.site);
    chrome.tabs.create({ url: s ? s.url : "https://" + acc.site });
    return;
  }
  const copy = e.target.closest("[data-copy]");
  if (copy) {
    await navigator.clipboard.writeText(list[+copy.dataset.copy].account || "");
    tip("✅ 账号已复制");
    return;
  }
  const del = e.target.closest("[data-del]");
  if (del) {
    if (confirm("删除这条托管记录？")) {
      list.splice(+del.dataset.del, 1);
      save(list); renderAccs(list);
    }
    return;
  }
  const fill = e.target.closest("[data-fill]");
  if (fill) {
    const acc = list[+fill.dataset.fill];
    if (!acc.pass && !confirm("该条目没存密码，只填账号？")) return;
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.id) return tip("❌ 找不到当前标签页");
    try {
      await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["fill-core.js"] });
      const [res] = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: (a, p) => window.__fillCreds(a, p),
        args: [acc.account || "", acc.pass || ""],
      });
      tip(res && res.result && res.result.ok ? "✅ " + res.result.msg : "❌ " + ((res && res.result && res.result.msg) || "填充失败"));
    } catch (err) {
      tip("❌ 无法注入此页（浏览器内置页/商店页不允许）");
    }
  }
});

async function loadSitesData() {
  try {
    const r = await fetch(api("/sites.json"));
    return { SITES: await r.json() };
  } catch (_) { return { SITES: [] }; }
}

$("p-add").addEventListener("click", () => {
  const site = $("p-site").value;
  const account = $("p-account").value.trim();
  const pass = $("p-pass").value;
  if (!site) return tip("请选择平台");
  if (!account) return tip("请填手机号/邮箱");
  const list = window.__accs || [];
  list.push({ site, account, pass: pass || "" });
  save(list); renderAccs(list);
  $("p-account").value = ""; $("p-pass").value = "";
  tip("✅ 已托管（仅存本机）");
});

$("p-import").addEventListener("change", (e) => {
  const f = e.target.files[0];
  if (!f) return;
  const r = new FileReader();
  r.onload = () => {
    try {
      const data = JSON.parse(r.result);
      if (!Array.isArray(data)) throw 0;
      const list = window.__accs || [];
      for (const v of data) {
        if (v && v.site && !list.some((x) => x.site === v.site && x.account === v.account)) {
          list.push({ site: v.site, account: v.account || "", pass: "" });
        }
      }
      save(list); renderAccs(list);
      tip(`✅ 导入 ${data.length} 条（密码需逐个补）`);
    } catch (_) { tip("❌ 文件格式不对（要 tokenmost 账号库导出的 json）"); }
  };
  r.readAsText(f);
});

$("p-save").addEventListener("click", () => {
  SITE = $("p-site-url").value.trim() || SITE;
  save(window.__accs || []);
  tip("✅ 已保存，重新拉取…");
  loadDeals(); loadSites();
});
