function showDateTime() {
  var el = document.getElementById("datetime");
  if (!el) return;
  el.textContent = new Date().toLocaleString();
}
showDateTime();
setInterval(showDateTime, 1000);

// Languages page: filter the cards by category
(function () {
  var buttons = document.querySelectorAll(".filter");
  var cards = document.querySelectorAll(".lang-card");
  var count = document.getElementById("lang-count");
  if (!buttons.length || !cards.length) return;

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      var filter = button.getAttribute("data-filter");
      var shown = 0;

      buttons.forEach(function (b) {
        var active = b === button;
        b.classList.toggle("active", active);
        b.setAttribute("aria-pressed", active ? "true" : "false");
      });

      cards.forEach(function (card) {
        var match = filter === "all" || card.getAttribute("data-category") === filter;
        card.hidden = !match;
        if (match) shown++;
      });

      count.textContent = "Showing " + shown + (shown === 1 ? " language" : " languages") +
        (filter === "all" ? "" : " for " + filter);
    });
  });
})();
