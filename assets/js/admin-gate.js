/* 硬见 · 后台隐蔽入口（纯新增文件，不改任何既有逻辑）
 *
 * 作用：在博客页面用「不显眼的方式」跳转到受 Basic Auth 保护的后台看板。
 * 注意：这里只负责"带你到门口"，真正的访问控制由 nginx Basic Auth 完成，
 *       本文件泄露不会导致任何权限提升。
 *
 * 两种触发方式，任意一个生效即可：
 *   1) 口令：在页面任意位置依次键入 zibange
 *   2) Konami 码：↑ ↑ ↓ ↓ ← → ← → B A
 *
 * 接入：在 index.html / article.html 末尾加一行
 *   <script src="assets/js/admin-gate.js"></script>
 */
(function () {
  'use strict';

  // 目标地址做轻度拆分，避免被整串关键字直接搜到
  var TARGET = ['h', 't', 't', 'p', 's', ':', '/', '/',
    'h', 'a', 'd', 'r', 'w', 'a', 'r', 'e', 'w', 'a', 't', 'c', 'h',
    '.', 'i', 'c', 'u', ':', '8', '4', '4', '3', '/', 'a', 'd', 'm', 'i', 'n', '/'
  ].join('');

  var PASSWORD = 'zibange';                 // 口令触发
  var KONAMI = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
    'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

  var buf = '';
  var kbuf = [];
  var fired = false;
  var timer = null;

  function isTyping(el) {
    if (!el) return false;
    var t = (el.tagName || '').toLowerCase();
    return t === 'input' || t === 'textarea' || t === 'select' || el.isContentEditable;
  }

  function go() {
    if (fired) return;
    fired = true;
    // 清空缓冲，避免在地址栏可见的历史里留下痕迹
    buf = '';
    kbuf = [];
    try { sessionStorage.setItem('hw_gate', '1'); } catch (e) { /* 忽略隐私模式 */ }
    window.location.href = TARGET;
  }

  function reset() {
    buf = '';
    kbuf = [];
  }

  document.addEventListener('keydown', function (e) {
    if (fired || isTyping(e.target)) return;

    // 忽略带修饰键的组合（Ctrl/Cmd/Alt 多为浏览器快捷键）
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    // ---- 触发 1：口令 ----
    var ch = (e.key || '').toLowerCase();
    if (ch && ch.length === 1) {
      buf += ch;
      if (buf.length > PASSWORD.length) buf = buf.slice(-PASSWORD.length);
      if (buf === PASSWORD) { go(); return; }
      clearTimeout(timer);
      timer = setTimeout(reset, 2000);   // 2 秒无输入则重置，避免误触发
    }

    // ---- 触发 2：Konami 码 ----
    kbuf.push(e.key);
    if (kbuf.length > KONAMI.length) kbuf.shift();
    if (kbuf.length === KONAMI.length) {
      for (var i = 0; i < KONAMI.length; i++) {
        var a = String(kbuf[i]).toLowerCase();
        var b = String(KONAMI[i]).toLowerCase();
        if (a !== b) return;
      }
      go();
    }
  }, false);
})();
