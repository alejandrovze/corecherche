console.log("loading memoire ...");

// BIBLIOGRAPHY FILLER
const bibFillEvent = new CustomEvent("bibFill", {
    bubbles: true,
    detail: { yOffset: -60}// Offset for bibliography scroll
});
const bibliography = document.getElementById("bibliography");

// PDF MEMOIRE
function resizeMemoire() {

  var width = document.getElementById("memoire-pdf").offsetWidth;

  document.getElementById("memoire-pdf").height = width / 1.41;

}

window.addEventListener('resize', resizeMemoire);;

resizeMemoire();

//