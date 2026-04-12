(function () {
  let panel = null;

  function close() {
    if (panel) { panel.remove(); panel = null; }
  }

  window.showUserPanel = function (event, userId, username) {
    event.stopPropagation();
    if (panel) { close(); return; }

    panel = document.createElement("div");
    panel.innerHTML = `
      <div style="padding:8px 12px; font-size:0.8rem; font-weight:700; color:rgba(55,165,199,0.81); border-bottom:1px solid rgba(255,255,255,0.1)">@${username}</div>
      <div style="padding:6px">
        <button class="fp-btn" onclick="sendFriendRequest('${userId}')">Add Friend</button>
        <button class="fp-btn" onclick="viewProfile('${userId}')">View Profile</button>
        <button class="fp-btn" onclick="openDM('${userId}')">Message</button>
      </div>`;

    Object.assign(panel.style, {
      position: "fixed", zIndex: 9999, width: "170px",
      background: "#1e2124", border: "1px solid rgba(255,255,255,0.1)",
      borderRadius: "8px", boxShadow: "0 8px 24px rgb(0,0,0)",
      fontFamily: "inherit",
    });

    document.body.appendChild(panel);

    let x = event.clientX + 8, y = event.clientY + 8;
    const r = panel.getBoundingClientRect();
    if (x + r.width  > window.innerWidth)  x = window.innerWidth  - r.width  - 8;
    if (y + r.height > window.innerHeight) y = window.innerHeight - r.height - 8;
    panel.style.left = x + "px";
    panel.style.top  = y + "px";
  };

  window.sendFriendRequest = (userId) => { close(); location.href = `/friends/request/${userId}/`; };
  window.viewProfile        = (userId) => { close(); location.href = `/profile/${userId}/`; };
  window.openDM             = (userId) => { close(); location.href = `/dm/${userId}/`; };

  document.addEventListener("click",  (e) => { if (panel && !panel.contains(e.target)) close(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });
})();