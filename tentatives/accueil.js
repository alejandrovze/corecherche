console.log("loading home ...");

// BIBLIOGRAPHY FILLER
const bibFillEvent = new CustomEvent("bibFill", {
    bubbles: true,
    detail: { yOffset: -160}// Offset for bibliography scroll
});
const bibliography = document.getElementById("bibliography");