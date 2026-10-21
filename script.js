function showDateTime() {
  var now = new Date();
  document.getElementById("datetime").textContent = now.toLocaleString();
}
showDateTime();
setInterval(showDateTime, 1000);
