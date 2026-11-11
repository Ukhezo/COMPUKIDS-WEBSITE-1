function showDateTime() {
  var el = document.getElementById("datetime");
  if (!el) return;
  el.textContent = new Date().toLocaleString();
}
showDateTime();
setInterval(showDateTime, 1000);
