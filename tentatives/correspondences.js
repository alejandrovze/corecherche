console.log("loading correspondences ...");

// BIBLIOGRAPHY FILLER
const bibFillEvent = new CustomEvent("bibFill", {
    bubbles: true,
    detail: { yOffset: -60}// Offset for bibliography scroll
});
const bibliography = document.getElementById("bibliography");


async function loadSub(correspondenceName) {
    const response = await fetch(`./tentatives/correspondences/${correspondenceName}.html`);
    const correspondence = await response.text();

    document.getElementById("correspondence-text").innerHTML = correspondence;
    
    bibliography.dispatchEvent(bibFillEvent);
}

const buttons = document.querySelectorAll('.subsection-button');

buttons.forEach(button => {
  button.addEventListener('click', function handleClick(event) {
    loadSub(button.getAttribute('id'));
  });
});

loadSub("2022-01-11-Robin");
// comment