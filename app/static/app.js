/* Arena Climb front end. The server decides every round; this file only draws it. */
(function () {
  "use strict";

  // ---------- Small helpers ----------
  var $ = function (id) { return document.getElementById(id); };

  // Build DOM safely: text always goes in as text, never as HTML.
  function h(tag, props) {
    var el = document.createElement(tag), i, child;
    props = props || {};
    Object.keys(props).forEach(function (k) {
      if (k === "class") el.className = props[k];
      else if (k === "text") el.textContent = props[k];
      else if (k === "style") el.setAttribute("style", props[k]);
      else if (k.indexOf("on") === 0) el.addEventListener(k.slice(2), props[k]);
      else if (props[k] === true) el.setAttribute(k, "");
      else if (props[k] !== false && props[k] != null) el.setAttribute(k, props[k]);
    });
    for (i = 2; i < arguments.length; i++) {
      child = arguments[i];
      if (child == null) continue;
      el.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
    }
    return el;
  }
  function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); return el; }

  function errorText(res) {
    var d = res.data && res.data.detail;
    if (typeof d === "string") return d;
    if (Array.isArray(d) && d.length) {
      var first = d[0], field = first.loc ? first.loc[first.loc.length - 1] : "";
      return (field ? String(field).replace("_", " ") + ": " : "") + (first.msg || "invalid value");
    }
    if (res.status === 0) return "Could not reach the server.";
    return "Something went wrong (" + res.status + ").";
  }

  function api(method, path, body) {
    return fetch(path, {
      method: method,
      credentials: "same-origin",
      headers: body ? { "Content-Type": "application/json" } : {},
      body: body ? JSON.stringify(body) : undefined
    }).then(function (r) {
      return r.text().then(function (t) {
        var data = null;
        try { data = t ? JSON.parse(t) : null; } catch (e) { data = null; }
        return { ok: r.ok, status: r.status, data: data };
      });
    }, function () {
      return { ok: false, status: 0, data: null };
    });
  }

  // ---------- Game data that only affects wording and drawing ----------
  var FIGHTERS = ["knight", "archer", "wizard"];
  var INFO = {
    knight: { name: "Knight", icon: "🛡️", beats: "archer", how: "charges down" },
    archer: { name: "Archer", icon: "🏹", beats: "wizard", how: "shoots" },
    wizard: { name: "Wizard", icon: "🧙", beats: "knight", how: "'s magic blasts" }
  };
  var RANK_STYLE = [
    "picks at random",
    "reads win-stay / lose-shift habits",
    "learns your habits during each battle",
    "remembers all your battles"
  ];
  function counter(x) { return FIGHTERS.filter(function (f) { return INFO[f].beats === x; })[0]; }
  function upper(f) { return INFO[f].name.toUpperCase(); }
  function beatLine(a, b) {
    var how = INFO[a].how;
    return upper(a) + (how.charAt(0) === "'" ? "" : " ") + how + " " + upper(b) + "!";
  }

  // ---------- State ----------
  var user = null;          // from the server
  var gear = { items: [], loadout: { knight: null, archer: null, wizard: null } };
  var match = null;         // the current match, from the server
  var busy = false;
  var view = "auth";

  function gearItem(id) { return gear.items.filter(function (it) { return it.id === id; })[0] || null; }

  // ---------- Sprites: Blender renders, pixelated ----------
  var CROP = { x: 108, y: 26, w: 304, h: 466 };
  var PIX_W = 52, PIX_H = Math.round(PIX_W * CROP.h / CROP.w);
  var images = {};
  function renderSrc(f, gearId) { return "/art/renders/" + f + "-" + (gearId || "starter") + ".png"; }
  function loadImage(src) {
    if (!images[src]) {
      var img = new Image(), entry = { img: img, ok: null, waiting: [] };
      images[src] = entry;
      img.onload = function () { entry.ok = true; entry.waiting.forEach(function (cb) { cb(); }); };
      img.onerror = function () { entry.ok = false; entry.waiting.forEach(function (cb) { cb(); }); };
      img.src = src;
    }
    return images[src];
  }
  function drawSprite(host, f, gearId) {
    clear(host);
    var entry = loadImage(renderSrc(f, gearId));
    function paint() {
      clear(host);
      if (entry.ok) {
        var c = document.createElement("canvas");
        c.width = PIX_W; c.height = PIX_H;
        var ctx = c.getContext("2d");
        ctx.imageSmoothingEnabled = true;
        ctx.drawImage(entry.img, CROP.x, CROP.y, CROP.w, CROP.h, 0, 0, PIX_W, PIX_H);
        host.appendChild(c);
      } else {
        host.appendChild(h("div", { class: "emoji", text: INFO[f].icon }));
      }
    }
    if (entry.ok === null) entry.waiting.push(paint); else paint();
  }

  // ---------- Views ----------
  function show(name) {
    view = name;
    ["auth", "battle", "dashboard", "armory", "account"].forEach(function (v) {
      $("view-" + v).classList.toggle("show", v === name);
    });
    $("hud").hidden = name === "auth";
    Array.prototype.forEach.call(document.querySelectorAll(".nav [data-view]"), function (b) {
      b.classList.toggle("on", b.getAttribute("data-view") === name);
    });
    if (name === "dashboard") loadDashboard();
    if (name === "armory") loadArmory();
    if (name === "account") fillAccount();
    if (name === "battle") enterBattle();
  }

  function signedOut() {
    user = null; match = null; busy = false; seq = null;
    closeModal();
    setTab(false);
    $("loginMsg").textContent = ""; $("registerMsg").textContent = "";
    show("auth");
  }

  // Any 401 outside the login form means the session ended.
  function guard(res) {
    if (res.status === 401) { signedOut(); return false; }
    return true;
  }

  function renderHud() {
    if (!user) return;
    $("rankName").textContent = user.rank_name;
    $("coins").textContent = user.coins;
    var box = clear($("stars"));
    if (user.stars_needed == null) {
      $("rankHint").textContent = "top rank · " + user.stars + " victory pts";
    } else {
      $("rankHint").textContent = (user.stars_needed - user.stars) + " to next rank";
      for (var i = 0; i < user.stars_needed; i++) box.appendChild(h("div", { class: "star" + (i < user.stars ? " on" : "") }));
    }
    $("playerSub").textContent = user.rank_name;
    $("playerName").textContent = user.display_name.toUpperCase().slice(0, 14);
  }

  // ---------- Auth ----------
  function setTab(register) {
    $("loginForm").hidden = register;
    $("registerForm").hidden = !register;
    $("tabLogin").className = "btn" + (register ? "" : " primary");
    $("tabRegister").className = "btn" + (register ? " primary" : "");
  }
  $("tabLogin").addEventListener("click", function () { setTab(false); });
  $("tabRegister").addEventListener("click", function () { setTab(true); });

  function formData(form) {
    var out = {};
    Array.prototype.forEach.call(form.querySelectorAll("input[name]"), function (i) { out[i.name] = i.value; });
    return out;
  }

  function afterSignIn(res) {
    user = res.data.user;
    $("loginForm").reset(); $("registerForm").reset();
    return refreshGear().then(function () { renderHud(); show("battle"); });
  }

  $("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
    $("loginMsg").textContent = "";
    api("POST", "/api/auth/login", formData(e.target)).then(function (res) {
      if (!res.ok) { $("loginMsg").textContent = errorText(res); return; }
      afterSignIn(res);
    });
  });

  $("registerForm").addEventListener("submit", function (e) {
    e.preventDefault();
    $("registerMsg").textContent = "";
    api("POST", "/api/auth/register", formData(e.target)).then(function (res) {
      if (!res.ok) { $("registerMsg").textContent = errorText(res); return; }
      afterSignIn(res);
    });
  });

  $("logoutBtn").addEventListener("click", function () {
    if (busy) return;
    api("POST", "/api/auth/logout").then(signedOut);
  });

  Array.prototype.forEach.call(document.querySelectorAll(".nav [data-view]"), function (b) {
    b.addEventListener("click", function () { if (!busy) show(b.getAttribute("data-view")); });
  });

  function refreshGear() {
    return api("GET", "/api/armory").then(function (res) {
      if (res.ok) { gear = res.data.gear; user = res.data.user; }
      return res;
    });
  }

  // ---------- Text box ----------
  var seq = null;
  function say(lines, done) {
    var token = {}, i = 0, timer = null, typing = false, full = "", pos = 0;
    seq = token;
    function nextLine() {
      if (seq !== token) return;
      if (i >= lines.length) { seq = null; $("nextArrow").style.visibility = "hidden"; if (done) done(); return; }
      var line = lines[i++];
      if (typeof line === "function") { line(); nextLine(); return; }
      full = line; pos = 0; typing = true;
      $("text").textContent = ""; $("nextArrow").style.visibility = "hidden";
      tick();
    }
    function tick() {
      if (seq !== token) return;
      pos++;
      $("text").textContent = full.slice(0, pos);
      if (pos < full.length) timer = setTimeout(tick, 16);
      else { typing = false; $("nextArrow").style.visibility = "visible"; timer = setTimeout(nextLine, 650); }
    }
    token.skip = function () {
      clearTimeout(timer);
      if (typing) { pos = full.length - 1; tick(); } else nextLine();
    };
    nextLine();
  }
  function prompt() { seq = null; $("text").textContent = "What will you do?"; $("nextArrow").style.visibility = "hidden"; }

  // ---------- Battle screen ----------
  function animate(el, cls) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }
  function showPlayer(f) {
    var el = $("playerSprite"); el.className = "sprite player";
    drawSprite(el, f, gear.loadout[f]); animate(el, "anim-enter-left");
  }
  function showEnemy(f) {
    var el = $("enemySprite"); el.className = "sprite enemy";
    drawSprite(el, f, null); animate(el, "anim-enter-drop");
  }
  function showMystery() {
    var el = clear($("enemySprite")); el.className = "sprite enemy";
    el.appendChild(h("div", { class: "mystery", text: "?" }));
  }
  function clearPlayer() { $("playerSprite").className = "sprite player"; clear($("playerSprite")); }

  function setBar(el, left) {
    var pct = Math.max(0, left) / 3 * 100;
    el.style.width = pct + "%";
    el.style.background = pct > 50 ? "var(--hp-high)" : pct > 34 ? "var(--hp-mid)" : "var(--hp-low)";
  }
  function renderBars() {
    var you = match ? match.you : 0, cpu = match ? match.cpu : 0;
    setBar($("playerBar"), 3 - cpu);
    setBar($("enemyBar"), 3 - you);
    $("score").textContent = "Rounds " + you + " – " + cpu + " · first to 3";
  }
  function renderMenu() {
    Array.prototype.forEach.call(document.querySelectorAll(".cmd[data-fighter]"), function (b) {
      var f = b.getAttribute("data-fighter"), g = gear.loadout[f], it = g ? gearItem(g) : null;
      clear(b);
      b.appendChild(document.createTextNode(upper(f)));
      b.appendChild(it ? h("small", {}, h("span", { class: "gear", text: "✦ " + it.name }))
                       : h("small", { text: "beats " + INFO[INFO[f].beats].name }));
    });
  }
  function setMenu(on) {
    Array.prototype.forEach.call(document.querySelectorAll(".cmd"), function (b) { b.disabled = !on; });
  }

  function enterBattle() {
    if (!user) return;
    renderHud(); renderMenu();
    $("enemySub").textContent = user.rank_name + " AI";
    if (!match || match.status !== "active") { match = null; clearPlayer(); showMystery(); }
    renderBars();
    if (!busy) { prompt(); setMenu(true); }
  }

  function fail(res) {
    busy = false;
    if (!guard(res)) return;
    $("text").textContent = errorText(res) + " Try again.";
    setMenu(true);
  }

  function play(pick) {
    if (busy || view !== "battle" || $("overlay").classList.contains("show")) return;
    busy = true; setMenu(false);
    $("text").textContent = "…";
    var start = (match && match.status === "active")
      ? Promise.resolve({ ok: true, data: { match: match } })
      : api("POST", "/api/matches");
    start.then(function (res) {
      if (!res.ok) { fail(res); return; }
      match = res.data.match;
      return api("POST", "/api/matches/" + match.id + "/rounds", { pick: pick }).then(function (res2) {
        if (!res2.ok) {
          if (res2.status === 409 || res2.status === 404) match = null;   // stale match: start fresh next time
          fail(res2); return;
        }
        playOut(res2.data);
      });
    });
  }

  // Tell one round on screen from the server's answer.
  function playOut(data) {
    var r = data.round, after = data.match, over = after.status !== "active";
    var playerEl = $("playerSprite"), enemyEl = $("enemySprite");
    function applyScore() { match = after; renderBars(); }
    var lines = [
      function () { showPlayer(r.pick); showMystery(); },
      "You send out " + upper(r.pick) + "!",
      function () { showEnemy(r.cpu); },
      "The rival sends out " + upper(r.cpu) + "!"
    ];
    if (r.predicted) lines.push(r.predicted === r.pick ? "The rival saw your move coming!" : "You caught the rival off guard!");
    if (r.result === "tie") {
      lines.push(function () { applyScore(); });
      lines.push("Both sent out " + upper(r.pick) + "! It's a standoff.");
    } else if (r.result === "win") {
      lines.push(function () { animate(playerEl, "anim-lunge-right"); setTimeout(function () { animate(enemyEl, "anim-hit"); applyScore(); }, 220); });
      lines.push(beatLine(r.pick, r.cpu));
      lines.push("You win the round!");
    } else {
      lines.push(function () { animate(enemyEl, "anim-lunge-left"); setTimeout(function () { animate(playerEl, "anim-hit"); applyScore(); }, 220); });
      lines.push(beatLine(r.cpu, r.pick));
      lines.push("The rival wins the round.");
    }
    if (over) {
      var won = after.status === "won";
      lines.push(function () { animate(won ? enemyEl : playerEl, "anim-faint"); if (won) animate(playerEl, "anim-win"); });
      lines.push(won ? "The rival is knocked out of the arena!" : "You were knocked out of the arena…");
    }
    say(lines, function () {
      match = after;
      renderBars();
      if (!over) { busy = false; prompt(); setMenu(true); return; }
      user = data.user;
      renderHud();
      var finish = function () { busy = false; showMatchResult(data); };
      if (data.outcome && data.outcome.unlocked_items.length) refreshGear().then(finish); else finish();
    });
  }

  function nextMatch() {
    match = null;
    closeModal();
    clearPlayer(); showMystery();
    renderHud(); renderMenu(); renderBars();
    $("enemySub").textContent = user.rank_name + " AI";
    setMenu(false);
    say(["A new rival steps into the arena!"], function () { prompt(); setMenu(true); });
  }

  // ---------- Modal ----------
  function openModal() {
    var m = clear($("modal"));
    for (var i = 0; i < arguments.length; i++) if (arguments[i]) m.appendChild(arguments[i]);
    $("overlay").classList.add("show");
  }
  function closeModal() { $("overlay").classList.remove("show"); }

  function progressLine() {
    if (user.stars_needed == null) return "You're a Champion. Keep winning for victory points.";
    var left = user.stars_needed - user.stars;
    var next = gear.items.filter(function (it) { return it.unlock_rank === user.rank + 1; })[0];
    return left + " more win" + (left === 1 ? "" : "s") + " to rank up" + (next ? " and unlock " + next.name + "!" : "!");
  }

  function showMatchResult(data) {
    var o = data.outcome, m = data.match, champ = user.stars_needed == null && !o.ranked_up;
    var unit = champ ? "victory point" : "star";
    var change;
    if (o.won) change = "+" + o.stars_change + " " + unit + (o.stars_change === 1 ? "" : "s") + " · +" + o.coins_earned + " coins" + (o.streak_bonus ? " · 🔥 3-win streak bonus!" : "");
    else change = o.stars_change < 0 ? "−1 " + unit : "Nothing lost: you're at the bottom of this rank";

    var again = h("button", { class: "btn", text: "Battle again", id: "againBtn", onclick: nextMatch });
    var stop = h("button", { class: "btn", text: "Dashboard", id: "stopBtn", onclick: function () { match = null; closeModal(); show("dashboard"); } });

    if (o.ranked_up) {
      var it = o.unlocked_items[0];
      var actions = h("div", { class: "actions" });
      if (it) {
        actions.appendChild(h("button", {
          class: "btn primary", text: "Equip & battle", id: "equipNow",
          onclick: function () {
            api("PUT", "/api/armory/loadout", { fighter: it.fighter, item_id: it.id }).then(function (res) {
              if (!guard(res)) return;
              if (res.ok) { gear = res.data.gear; user = res.data.user; }
              nextMatch();
            });
          }
        }));
      } else {
        again.className = "btn primary";
      }
      actions.appendChild(again); actions.appendChild(stop);
      var art = h("div", { class: "art-box" });
      openModal(
        h("h2", { style: "color:#b07a10", text: "RANKED UP: " + o.new_rank_name.toUpperCase() + "!" }),
        h("p", { text: "+" + o.coins_earned + " coins." + (it ? " New gear for your " + INFO[it.fighter].name + ":" : "") }),
        it ? art : null,
        it ? h("h3", { style: "color:" + it.color + ";margin:4px 0", text: it.name }) : null,
        h("p", { text: "From now on the rival " + (RANK_STYLE[user.rank] || RANK_STYLE[RANK_STYLE.length - 1]) + "." }),
        actions
      );
      if (it) drawSprite(art, it.fighter, it.id);
    } else {
      again.className = "btn primary";
      openModal(
        h("h2", { style: "color:" + (o.won ? "#2f9a3d" : "#c0392b"), text: o.won ? "VICTORY!" : "DEFEAT" }),
        h("p", {}, "Final score " + m.you + " – " + m.cpu + ".", h("br"), change),
        h("div", { class: "progress-line", text: progressLine() }),
        h("div", { class: "actions" }, again, stop)
      );
    }
  }

  // ---------- Dashboard ----------
  function starsRow(u) {
    var row = h("div", { class: "big-stars" });
    if (u.stars_needed == null) return h("p", { text: u.stars + " victory points" });
    for (var i = 0; i < u.stars_needed; i++) row.appendChild(h("div", { class: "star" + (i < u.stars ? " on" : "") }));
    return row;
  }
  function stat(value, label) { return h("div", { class: "stat" }, h("b", { text: String(value) }), h("span", { text: label })); }

  function gearCard(it, withActions) {
    var thumb = h("div", { class: "thumb" });
    var status = it.equipped ? "Equipped" : it.owned ? "Owned"
      : it.price != null ? it.price + " coins" : "Unlocks at " + it.unlock_rank_name;
    var card = h("div", { class: "gear-card" + (it.equipped ? " equipped" : "") + (it.owned ? "" : " locked"), "data-item": it.id },
      thumb, h("div", {}, h("span", { class: "dot", style: "background:" + it.color }), h("b", { text: it.name })), h("small", { text: INFO[it.fighter].name + " · " + status }));
    drawSprite(thumb, it.fighter, it.id);
    if (withActions) {
      if (it.equipped) card.appendChild(h("button", { class: "btn", text: "Unequip", onclick: function () { equip(it.fighter, null); } }));
      else if (it.owned) card.appendChild(h("button", { class: "btn primary", text: "Equip", onclick: function () { equip(it.fighter, it.id); } }));
      else if (it.price != null) card.appendChild(h("button", { class: "btn", text: "Buy · " + it.price, disabled: user.coins < it.price, onclick: function () { buy(it.id); } }));
      else card.appendChild(h("small", { text: "🔒 Locked" }));
    }
    return card;
  }

  function loadDashboard() {
    var root = $("view-dashboard");
    api("GET", "/api/dashboard").then(function (res) {
      if (!guard(res)) return;
      if (!res.ok) { clear(root).appendChild(h("div", { class: "panel" }, h("p", { text: errorText(res) }))); return; }
      var d = res.data; user = d.user; gear = d.gear; renderHud();
      var s = d.stats;
      var progress = h("div", { class: "panel" },
        h("h2", { text: d.user.display_name.toUpperCase() + " · " + d.user.rank_name.toUpperCase() }),
        starsRow(d.user),
        h("p", { text: d.user.stars_needed == null ? "Top rank reached." : (d.user.stars_needed - d.user.stars) + " more star(s) to rank up." }),
        h("div", { class: "stat-row" },
          stat(s.matches_played, "battles"), stat(s.wins, "wins"), stat(s.losses, "losses"),
          stat(s.win_rate == null ? "–" : Math.round(s.win_rate * 100) + "%", "win rate"),
          stat(s.streak, "win streak"), stat(d.user.coins, "coins")));

      var history = h("div", { class: "panel" }, h("h2", { text: "RECENT BATTLES" }));
      if (!d.recent_matches.length) {
        history.appendChild(h("p", { text: "No battles yet." }));
        history.appendChild(h("button", { class: "btn primary", text: "Enter the arena", onclick: function () { show("battle"); } }));
      } else {
        var body = h("tbody");
        d.recent_matches.forEach(function (m) {
          var when = m.finished_at ? new Date(m.finished_at).toLocaleString([], { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) : "";
          body.appendChild(h("tr", {},
            h("td", { class: m.won ? "won" : "lost", text: m.won ? "Won" : "Lost" }),
            h("td", { text: m.you + " – " + m.cpu }),
            h("td", { text: m.rank_name }),
            h("td", { text: (m.stars_change > 0 ? "+" : "") + m.stars_change + " ★" }),
            h("td", { text: "+" + m.coins_earned }),
            h("td", { text: when })));
        });
        history.appendChild(h("table", { class: "history" },
          h("thead", {}, h("tr", {}, h("th", { text: "Result" }), h("th", { text: "Rounds" }), h("th", { text: "Rank" }), h("th", { text: "Stars" }), h("th", { text: "Coins" }), h("th", { text: "When" }))),
          body));
      }

      var owned = d.gear.items.filter(function (it) { return it.owned; });
      var collection = h("div", { class: "panel" }, h("h2", { text: "GEAR · " + owned.length + " OF " + d.gear.items.length }));
      var grid = h("div", { class: "gear-grid" });
      d.gear.items.forEach(function (it) { grid.appendChild(gearCard(it, false)); });
      collection.appendChild(grid);
      collection.appendChild(h("p", {}, h("button", { class: "btn", text: "Open the armory", onclick: function () { show("armory"); } })));

      clear(root); root.appendChild(progress); root.appendChild(history); root.appendChild(collection);
    });
  }

  // ---------- Armory ----------
  function renderArmory(message, isError) {
    var root = clear($("view-armory"));
    var panel = h("div", { class: "panel" },
      h("h2", { text: "ARMORY" }),
      h("p", { text: "Gear changes how your fighters look, never whether they win. You have 🪙 " + user.coins + "." }),
      h("div", { class: "msg " + (isError ? "err" : "ok"), id: "armoryMsg", text: message || "" }));
    var grid = h("div", { class: "gear-grid" });
    gear.items.forEach(function (it) { grid.appendChild(gearCard(it, true)); });
    panel.appendChild(grid);
    root.appendChild(panel);
  }
  function loadArmory() {
    refreshGear().then(function (res) { if (!guard(res)) return; renderHud(); renderArmory(); });
  }
  function armoryAction(promise, okMessage) {
    promise.then(function (res) {
      if (!guard(res)) return;
      if (res.ok) { gear = res.data.gear; user = res.data.user; renderHud(); renderArmory(okMessage, false); }
      else renderArmory(errorText(res), true);
    });
  }
  function buy(id) { armoryAction(api("POST", "/api/armory/buy", { item_id: id }), "Bought " + gearItem(id).name + "."); }
  function equip(fighter, id) {
    armoryAction(api("PUT", "/api/armory/loadout", { fighter: fighter, item_id: id }), id ? "Equipped " + gearItem(id).name + "." : "Gear removed.");
  }

  // ---------- Account ----------
  function fillAccount() {
    $("profileForm").elements.display_name.value = user.display_name;
    $("accountEmail").textContent = "Signed in as " + user.email;
    $("profileMsg").textContent = ""; $("passwordMsg").textContent = "";
  }
  function setMsg(id, text, ok) { var el = $(id); el.textContent = text; el.className = "msg " + (ok ? "ok" : "err"); }

  $("profileForm").addEventListener("submit", function (e) {
    e.preventDefault();
    api("PATCH", "/api/me", formData(e.target)).then(function (res) {
      if (!guard(res)) return;
      if (!res.ok) { setMsg("profileMsg", errorText(res), false); return; }
      user = res.data.user; renderHud(); fillAccount(); setMsg("profileMsg", "Saved.", true);
    });
  });
  $("passwordForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var form = e.target;
    api("POST", "/api/me/password", formData(form)).then(function (res) {
      if (res.status === 401) { signedOut(); return; }
      if (!res.ok) { setMsg("passwordMsg", errorText(res), false); return; }
      form.reset(); setMsg("passwordMsg", "Password changed.", true);
    });
  });

  // ---------- Wiring ----------
  Array.prototype.forEach.call(document.querySelectorAll(".cmd[data-fighter]"), function (b) {
    var f = b.getAttribute("data-fighter");
    b.addEventListener("click", function () { play(f); });
    b.addEventListener("mouseenter", function () {
      if (!busy && !seq) $("text").textContent = beatLine(f, INFO[f].beats).replace("!", "") + ", but loses to " + upper(counter(f)) + ".";
    });
    b.addEventListener("mouseleave", function () { if (!busy && !seq) prompt(); });
  });
  $("armoryCmd").addEventListener("click", function () { if (!busy) show("armory"); });
  $("dialog").addEventListener("click", function () { if (seq && seq.skip) seq.skip(); });
  document.addEventListener("keydown", function (e) {
    if (view !== "battle" || $("overlay").classList.contains("show")) return;
    if (e.key === " " || e.key === "Enter") { if (seq && seq.skip) { seq.skip(); e.preventDefault(); } return; }
    var i = ["1", "2", "3"].indexOf(e.key);
    if (i >= 0) play(FIGHTERS[i]);
  });

  // ---------- Start ----------
  FIGHTERS.forEach(function (f) { loadImage(renderSrc(f, null)); });
  api("GET", "/api/me").then(function (res) {
    if (!res.ok) { show("auth"); return; }
    user = res.data.user;
    refreshGear().then(function () { renderHud(); show("battle"); });
  });

  // For automated checks only.
  window.__arena = {
    busy: function () { return busy; },
    view: function () { return view; },
    user: function () { return user; },
    skip: function () { if (seq && seq.skip) seq.skip(); }
  };
})();
