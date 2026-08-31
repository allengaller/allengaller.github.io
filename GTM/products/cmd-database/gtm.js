/* 语料星座图谱 — 全部数据来自 CORPUS（INDEX.md 与真实语料目录生成） */
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var svg = document.getElementById("constellation");
  var qInput = document.getElementById("q");
  var skyHint = document.getElementById("skyHint");
  var HINT_DEFAULT = skyHint.textContent;

  /* ---------- 确定性随机（mulberry32） ---------- */
  function hash(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  function rng(seed) {
    var a = hash(seed);
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* ---------- 九大星座锚点（手工排布的星图制图位） ---------- */
  var CATS = [
    { id: "ai",          label: "AI 基础设施", x: 330, y: 500 },
    { id: "cloudnative", label: "云原生",      x: 735, y: 330 },
    { id: "toolchain",   label: "开发工具链",  x: 905, y: 160 },
    { id: "system",      label: "操作系统",    x: 200, y: 680 },
    { id: "data",        label: "数据库",      x: 560, y: 720 },
    { id: "bigdata",     label: "大数据",      x: 895, y: 600 },
    { id: "network",     label: "网络",        x: 130, y: 330 },
    { id: "ops",         label: "运维",        x: 330, y: 810 },
    { id: "misc",        label: "综合",        x: 560, y: 210 }
  ];
  var CAT_XLINKS = [["ai", "cloudnative"], ["ai", "data"], ["cloudnative", "toolchain"],
                    ["system", "network"], ["data", "bigdata"], ["ops", "misc"]];

  var GOLDEN = Math.PI * (3 - Math.sqrt(5));

  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }

  /* ---------- 渲染 ---------- */
  var root = el("g", { class: "drift" });
  svg.appendChild(root);

  /* 背景细星（确定性撒点，不参与交互） */
  (function () {
    var r = rng("starfield");
    for (var i = 0; i < 110; i++) {
      el("circle", {
        class: "bg-star",
        cx: (r() * 1000).toFixed(1), cy: (r() * 880).toFixed(1),
        r: (0.5 + r() * 1.1).toFixed(2),
        opacity: (0.08 + r() * 0.3).toFixed(2)
      }, root);
    }
  })();

  /* 星座间发丝长线 */
  CAT_XLINKS.forEach(function (p) {
    var a = CATS.find(function (c) { return c.id === p[0]; });
    var b = CATS.find(function (c) { return c.id === p[1]; });
    el("line", { class: "edge-x", x1: a.x, y1: a.y, x2: b.x, y2: b.y }, root);
  });

  /* 领域节点：绕锚点按黄金角散布 */
  var domainsByCat = {};
  CORPUS.domains.forEach(function (d) { (domainsByCat[d.cat] = domainsByCat[d.cat] || []).push(d); });

  var byName = {};
  var cmdPos = {};

  CATS.forEach(function (cat) {
    var list = (domainsByCat[cat.id] || []).slice().sort(function (a, b) { return b.cmds - a.cmds; });
    var r = rng("cat:" + cat.id);
    list.forEach(function (d, i) {
      var ang = i * GOLDEN + r() * 0.9;
      var dist = (cat.id === "ai" ? 92 : 44) + Math.sqrt(d.cmds) * 4.2 + r() * 34;
      var x = cat.x + Math.cos(ang) * dist;
      var y = cat.y + Math.sin(ang) * dist * 0.82;
      if (d.name === "大模型训练") { x = 430; y = 420; }
      x = Math.max(46, Math.min(954, x));
      y = Math.max(52, Math.min(838, y));
      d._x = x; d._y = y;

      var g = el("g", { class: "node" }, root);
      var a = el("a", { href: "../" + d.name + "/" + d.name + "-MOC.md" }, g);
      el("circle", { class: "dom", cx: x, cy: y, r: 2.2 + Math.sqrt(d.cmds) * 0.75 }, a);
      var t = el("title", {}, a);
      t.textContent = d.name + " · " + d.cmds + " 命令页 · " + d.bp + " 最佳实践页";
      g.dataset.keys = d.name.toLowerCase();
      g.dataset.kind = "domain";
      byName[d.name] = d; d._g = g;

      if (d.name === "大模型训练") {
        el("circle", { class: "hub-ring", cx: x, cy: y, r: 30, opacity: 0.18 }, a);
        el("circle", { class: "hub-ring", cx: x, cy: y, r: 46, opacity: 0.09 }, a);
        el("text", { class: "hub-label", x: x, y: y - 3 }, a).textContent = "大模型";
        el("text", { class: "hub-label", x: x, y: y + 15 }, a).textContent = "训练";
      } else if (d.cmds >= 30) {
        el("text", { class: "node-label", x: x, y: y + 18, "text-anchor": "middle" }, g)
          .textContent = d.name;
      }
    });

    el("circle", { class: "cat", cx: cat.x, cy: cat.y, r: 3.4 }, root);
    el("text", { class: "cat-label", x: cat.x + 10, y: cat.y - 10 }, root).textContent = cat.label;
  });

  /* ---------- 聚焦簇：大模型训练（构图三的手工星位，标签不叠压） ---------- */
  var HUB = { x: 430, y: 420 };

  var THEMES = [
    ["cerebras",      232, 246], ["colossal-ai",  650, 262],
    ["composer",      810, 322], ["flash-attn",   128, 356],
    ["distilabel",    930, 412], ["alpaca-eval",   92, 500],
    ["dpo",           880, 528], ["axolotl",      150, 636],
    ["grpo",          935, 646], ["lightning",    262, 764],
    ["llama-factory", 492, 788], ["bitsandbytes", 700, 716]
  ];

  function spoke(x2, y2, key) {
    var ln = el("line", { class: "edge", x1: HUB.x, y1: HUB.y, x2: x2, y2: y2 }, root);
    ln.dataset.a = "大模型训练"; ln.dataset.b = key;
  }
  function cmdNode(name, x, y, href) {
    var g = el("g", { class: "node" }, root);
    var a = el("a", { href: href }, g);
    el("circle", { class: "cmd", cx: x, cy: y, r: 2.6 }, a);
    var t = el("title", {}, a);
    t.textContent = name + " · 大模型训练";
    var anchor = x >= HUB.x ? "start" : "end";
    el("text", {
      class: "cmd-label", x: x + (anchor === "start" ? 7 : -7), y: y + 3.5, "text-anchor": anchor
    }, g).textContent = name;
    g.dataset.keys = name.toLowerCase();
    g.dataset.kind = "cmd";
    g.dataset.dom = "大模型训练";
    cmdPos[name] = { x: x, y: y };
  }
  function cmdBox(name, cx, cy, opts) {
    opts = opts || {};
    var w = name.length * 7 + 24, h = 26;
    var g = el("g", { class: "node " + (opts.dashed ? "bp-box" : "cmd-box") }, root);
    var a = el("a", { href: opts.href }, g);
    el("rect", { x: cx - w / 2, y: cy - h / 2, width: w, height: h, rx: 3 }, a);
    el("text", { x: cx, y: cy + 4, "text-anchor": "middle" }, a).textContent = name;
    var t = el("title", {}, a);
    t.textContent = name + " · 大模型训练";
    g.dataset.keys = name.toLowerCase();
    g.dataset.kind = "cmd";
    g.dataset.dom = "大模型训练";
    cmdPos[name] = { x: cx, y: cy };
  }

  THEMES.forEach(function (th) { spoke(th[1], th[2], th[0].toLowerCase()); });
  spoke(438, 516, "deepspeed");
  spoke(318, 580, "accelerate");

  THEMES.forEach(function (th) {
    cmdNode(th[0], th[1], th[2], "../大模型训练/" + th[0] + ".md");
  });
  cmdBox("deepspeed", 438, 516, { href: "../大模型训练/deepspeed.md" });
  cmdBox("accelerate", 318, 580, { href: "../大模型训练/accelerate.md" });
  cmdBox("bp-deepspeed", 438, 562, { dashed: true, href: "../大模型训练/bp-deepspeed.md" });
  (function () {
    var ln = el("line", { class: "edge", x1: 438, y1: 529, x2: 438, y2: 551 }, root);
    ln.dataset.a = "deepspeed"; ln.dataset.b = "bp-deepspeed";
  })();

  /* 簇内 related_commands 连线（与 llm-training.yaml 一致的子集） */
  [["deepspeed", "accelerate"], ["dpo", "grpo"], ["distilabel", "dpo"]].forEach(function (p) {
    var a = cmdPos[p[0]], b = cmdPos[p[1]];
    if (!a || !b) return;
    var ln = el("line", { class: "edge", x1: a.x, y1: a.y, x2: b.x, y2: b.y }, root);
    ln.dataset.a = p[0]; ln.dataset.b = p[1];
  });

  /* 其余聚焦领域的命令深度：不标注的小星点 */
  Object.keys(CORPUS.focus).forEach(function (domName) {
    if (domName === "大模型训练") return;
    var d = byName[domName];
    if (!d) return;
    var cmds = CORPUS.focus[domName].filter(function (c) { return !/-MOC$/.test(c); }).slice(0, 5);
    var r = rng("focus:" + domName);
    cmds.forEach(function (name, i) {
      var ang = i * GOLDEN + r() * 0.8;
      var dist = 24 + r() * 26;
      var x = Math.max(30, Math.min(970, d._x + Math.cos(ang) * dist));
      var y = Math.max(36, Math.min(852, d._y + Math.sin(ang) * dist * 0.9));
      var g = el("g", { class: "node" }, root);
      var a = el("a", { href: "../" + domName + "/" + name + ".md" }, g);
      el("circle", { class: "cmd", cx: x, cy: y, r: 2.1 }, a);
      var t = el("title", {}, a);
      t.textContent = name + " · " + domName;
      g.dataset.keys = name.toLowerCase();
      g.dataset.kind = "cmd";
      g.dataset.dom = domName.toLowerCase();
      var ln = el("line", { class: "edge", x1: d._x, y1: d._y, x2: x, y2: y }, root);
      ln.dataset.a = domName.toLowerCase(); ln.dataset.b = name.toLowerCase();
    });
  });

  /* nodeIn 动画结束后摘掉 .node（fill:both 会锁死 opacity，干扰搜索调光） */
  svg.addEventListener("animationend", function (e) {
    if (e.target.classList && e.target.classList.contains("node") && e.animationName === "nodeIn") {
      e.target.classList.remove("node");
    }
  });

  /* ---------- 搜索即点亮 ---------- */
  var groups = Array.prototype.slice.call(svg.querySelectorAll("g[data-keys]"));
  var edges = Array.prototype.slice.call(svg.querySelectorAll("line.edge[data-a]"));
  qInput.addEventListener("input", function () {
    var q = qInput.value.trim().toLowerCase();
    if (!q) {
      svg.classList.remove("searching");
      groups.forEach(function (g) { g.classList.remove("lit"); });
      edges.forEach(function (ln) { ln.classList.remove("lit"); });
      skyHint.textContent = HINT_DEFAULT;
      return;
    }
    var hits = 0;
    var litKeys = {};
    groups.forEach(function (g) {
      var match = g.dataset.keys.indexOf(q) !== -1;
      g.classList.toggle("lit", match);
      if (match) {
        hits++;
        litKeys[g.dataset.keys] = true;
        if (g.dataset.dom) litKeys[g.dataset.dom] = true;
      }
    });
    edges.forEach(function (ln) {
      ln.classList.toggle("lit", !!(litKeys[ln.dataset.a] && litKeys[ln.dataset.b]));
    });
    svg.classList.add("searching");
    skyHint.textContent = hits
      ? hits + " 处命中 · 星图已聚焦"
      : "无命中 · 试试 deepspeed / kubectl / git";
  });

  /* 深链：?q=xxx 直接进入点亮态，可分享搜索结果 */
  var qs = new URLSearchParams(location.search).get("q");
  if (qs) {
    qInput.value = qs;
    qInput.dispatchEvent(new Event("input"));
  }

  /* ---------- 领域星图索引（#domGrid） ---------- */
  var grid = document.getElementById("domGrid");
  var frag = document.createDocumentFragment();

  CATS
    .map(function (c) {
      var list = (domainsByCat[c.id] || []).slice()
        .sort(function (a, b) { return b.cmds - a.cmds; });
      return { cat: c, list: list };
    })
    .sort(function (a, b) {
      return sum(b.list) - sum(a.list);
    })
    .forEach(function (entry) {
      var div = document.createElement("div");
      div.className = "dom-cat";
      var h = document.createElement("h3");
      h.textContent = entry.cat.label + " · " + entry.list.length;
      div.appendChild(h);
      var ul = document.createElement("ul");
      entry.list.forEach(function (d) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = "../" + d.name + "/" + d.name + "-MOC.md";
        a.textContent = d.name;
        var n = document.createElement("span");
        n.className = "n";
        var b = document.createElement("b");
        b.textContent = d.cmds;
        var it = document.createElement("i");
        it.textContent = "页";
        n.appendChild(b); n.appendChild(it);
        if (d.bp) n.appendChild(document.createTextNode(" · " + d.bp + " BP"));
        li.appendChild(a); li.appendChild(n);
        ul.appendChild(li);
      });
      div.appendChild(ul);
      frag.appendChild(div);
    });
  grid.appendChild(frag);

  function sum(list) { return list.reduce(function (s, d) { return s + d.cmds; }, 0); }
})();
