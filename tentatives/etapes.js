console.log("loading etapes ...");

// BIBLIOGRAPHY FILLER
const bibFillEvent = new CustomEvent("bibFill", {
    bubbles: true,
    detail: { yOffset: -60}// Offset for bibliography scroll
});


document.getElementById("bibliography").dispatchEvent(bibFillEvent);
