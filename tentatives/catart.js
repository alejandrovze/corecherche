console.log("loading catart ...");

// BIBLIOGRAPHY FILLER
const bibFillEvent = new CustomEvent("bibFill", {
    bubbles: true,
    detail: { yOffset: -60}// Offset for bibliography scroll
});
const bibliography = document.getElementById("bibliography");

async function loadSub(journalNumber) {
    const response = await fetch(`./tentatives/ateliers/atelier-v${journalNumber}.html`);
    const journal = await response.text();

    document.getElementById("journal-text").innerHTML = journal;

    bibliography.dispatchEvent(bibFillEvent);
}

const buttons = document.querySelectorAll('.subsection-button');

buttons.forEach(button => {
  button.addEventListener('click', function handleClick(event) {
    loadSub(button.getAttribute('journal-number'));
  });
});

loadSub("1");