/* TokenMost 填充引擎：注入到目标登录页，启发式定位账号/密码框并填入。
   同时被 popup（本地引用）与 chrome.scripting（注入）复用；test-login.html 用于回归。 */
(function () {
  function vis(el) { return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length); }
  function textish(el) {
    const t = (el.type || "text").toLowerCase();
    return ["text", "tel", "email", ""].includes(t);
  }
  function setVal(el, v) {
    // 走原生 setter，绕开 React 受控组件的值拦截
    const d = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value");
    if (d && d.set) d.set.call(el, v); else el.value = v;
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  }
  window.__fillCreds = function (account, password) {
    const pws = Array.from(document.querySelectorAll('input[type="password"]')).filter(vis);
    if (!pws.length) {
      return { ok: false, msg: "本页没找到密码框（可能需要先点「密码登录」切换登录模式）" };
    }
    const pwEl = pws[0];
    const all = Array.from(document.querySelectorAll("input"));
    const kw = /(phone|mobile|tel|account|email|user|name|mail|login)/i;
    let uEl = null;
    for (const el of all) {                 // 1) 关键词优先（name/id/placeholder/autocomplete）
      if (el === pwEl) break;
      if (!vis(el) || !textish(el) || el.disabled || el.readOnly) continue;
      const sig = ((el.name || "") + " " + (el.id || "") + " " + (el.placeholder || "") + " " + (el.autocomplete || ""));
      if (kw.test(sig)) { uEl = el; break; }
    }
    if (!uEl) for (const el of all) {       // 2) 兜底：密码框之前最后一个可见文本框
      if (el === pwEl) break;
      if (vis(el) && textish(el) && !el.disabled && !el.readOnly) uEl = el;
    }
    let did = 0;
    if (uEl && account) { setVal(uEl, account); did++; }
    if (password) { setVal(pwEl, password); did++; }
    pwEl.focus();
    if (!did) return { ok: false, msg: "没有可填的字段" };
    return { ok: true, msg: "账号" + (uEl ? "✓ " : "未识别（已填密码）") + " 密码✓，检查后点登录" };
  };
})();
