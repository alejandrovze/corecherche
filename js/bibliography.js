// MANAGE BIBLIOGRAPHY

const bibliography = document.getElementById('bibliography');

export async function registerBibliography() {
    console.log("Loading bibliography");
    const bibFile = await fetch(`./templates/bibliography.html`);
    const bibContents = await bibFile.text();
    bibliography.innerHTML = bibContents;
}

const getBibIndex = (bibId) => {
    return Array.from(bibliography.children).indexOf(document.getElementById(bibId)) + 1;
}

const fillBibliography = (offset) => {
    const bibItems = document.getElementsByClassName("bib");
    for (let i = 0; i < bibItems.length; i++) {
        const index = bibItems[i].getAttribute("ref");
        bibItems[i].innerText = getBibIndex(index);
        bibItems[i].addEventListener('click', async function handleClick(event) {
            // Scroll bibliography item into view with offset
            const y = document.getElementById(index).getBoundingClientRect().top + window.pageYOffset + offset;
            window.scrollTo({top: y, behavior: 'smooth'});

            // Highlight bib element
            document.getElementById(index).classList.add('active');
            setTimeout(function(){
                document.getElementById(index).classList.remove('active')
            },5000)
        });
    }
}

bibliography.addEventListener("bibFill", e => fillBibliography(e.detail.yOffset));