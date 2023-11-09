document.addEventListener("DOMContentLoaded", (event) => {
  var root = document.documentElement;
  var img = document.getElementById("theme-toggle-img");

  // Au chargement de la page, vérifier s'il y a un thème enregistré dans localStorage
  if (localStorage.getItem("theme") === "dark") {
    root.setAttribute("data-theme", "dark");
    img.src = "/static/images/soleil.png";
    img.alt = "Basculer vers le thème clair";
  } else {
    root.setAttribute("data-theme", "");
    img.src = "/static/images/lune.png";
    img.alt = "Basculer vers le thème sombre";
  }
});

document.getElementById("theme-toggle").addEventListener("click", function () {
  var root = document.documentElement;
  var img = document.getElementById("theme-toggle-img");
  var isDark = root.getAttribute("data-theme") === "dark";

  // Basculer le thème
  var newTheme = isDark ? "" : "dark";
  root.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme); // Enregistrer le thème dans localStorage

  // Basculer l'image
  img.src = isDark ? "/static/images/lune.png" : "/static/images/soleil.png";
  img.alt = isDark
    ? "Basculer vers le thème clair"
    : "Basculer vers le thème sombre";
});
