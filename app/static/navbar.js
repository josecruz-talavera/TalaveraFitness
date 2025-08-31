function toggleMenu() {
  var menu = document.getElementById("navMenu");
  if (menu.classList.contains("active")) {
      menu.classList.remove("active");
  } else {
      menu.classList.add("active");
  }
}
