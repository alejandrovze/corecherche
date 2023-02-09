console.log("loading a-to-z ...");

// BIBLIOGRAPHY FILLER
const bibFillEvent = new CustomEvent("bibFill", {
    bubbles: true,
    detail: { yOffset: -160}// Offset for bibliography scroll
});
const bibliography = document.getElementById("bibliography");

/** AUDIO PLAYER */
const playButton = document.getElementById('play-button');
const playIcon = document.getElementById('play-icon');
const audioPlayerContainer = document.getElementById('audio-player');
const seekSlider = document.getElementById('seek-slider');
let playState = 'play';

const playSVG = "M30,0C13.458,0,0,13.458,0,30s13.458,30,30,30s30-13.458,30-30S46.542,0,30,0z M45.563,30.826l-22,15 C23.394,45.941,23.197,46,23,46c-0.16,0-0.321-0.038-0.467-0.116C22.205,45.711,22,45.371,22,45V15c0-0.371,0.205-0.711,0.533-0.884 c0.328-0.174,0.724-0.15,1.031,0.058l22,15C45.836,29.36,46,29.669,46,30S45.836,30.64,45.563,30.826z";
const pauseSVG = "M30,0C13.458,0,0,13.458,0,30s13.458,30,30,30s30-13.458,30-30S46.542,0,30,0z M27,46h-8V14h8V46z M41,46h-8V14h8V46z";

const play = () => {
    audio.play();
    playIcon.setAttribute("d", pauseSVG);
    requestAnimationFrame(whilePlaying);
    playState = 'pause';
}

const pause = () => {
    audio.pause();
    playIcon.setAttribute("d", playSVG);
    cancelAnimationFrame(raf);play
    playState = 'play';
}

playButton.addEventListener('click', () => {
    if(playState === 'play') {
        play();
    } else {
        pause();
    }
});

const showRangeProgress = (rangeInput) => {
    if(rangeInput === seekSlider) audioPlayerContainer.style.setProperty('--seek-before-width', rangeInput.value / rangeInput.max * 100 + '%');
    else audioPlayerContainer.style.setProperty('--volume-before-width', rangeInput.value / rangeInput.max * 100 + '%');
}

seekSlider.addEventListener('input', (e) => {
    showRangeProgress(e.target);
});

const audioContainer = document.getElementById('audio-player');
const audio = document.querySelector('audio');
const durationContainer = document.getElementById('duration');
const currentTimeContainer = document.getElementById('current-time');
const slider_spa = document.getElementById("spa");
const mainApp = document.getElementById("app");
let raf = null;

const hideAudio = () => {
    $("#audio-player").hide();
    mainApp.style.setProperty('margin-top', '60px');
}

const showAudio = () => {
    $("#audio-player").show();
    mainApp.style.setProperty('margin-top', '160px');
}

const calculateTime = (secs) => {
    const minutes = Math.floor(secs / 60);
    const seconds = Math.floor(secs % 60);
    const returnedSeconds = seconds < 10 ? `0${seconds}` : `${seconds}`;
    return `${minutes}:${returnedSeconds}`;
}

const displayDuration = () => {
    durationContainer.textContent = calculateTime(audio.duration);
}

const setSliderMax = () => {
    seekSlider.max = Math.floor(audio.duration);
}

const whilePlaying = () => {
    seekSlider.value = Math.floor(audio.currentTime);
    currentTimeContainer.textContent = calculateTime(seekSlider.value);
    audioPlayerContainer.style.setProperty('--seek-before-width', `${seekSlider.value / seekSlider.max * 100}%`);
    raf = requestAnimationFrame(whilePlaying);
}

if (audio.readyState > 0) {
    displayDuration();
    setSliderMax();
    pause();
} 

// EVENT LISTENER TO RELOAD AUDIO
audio.addEventListener('loadedmetadata', () => {
    console.log("Loaded sound file, reset duration");
    displayDuration();
    setSliderMax();
    pause(); // Force reset to pause icon etc.
    whilePlaying(); // Force reset to slider
});


seekSlider.addEventListener('input', () => {
    currentTimeContainer.textContent = calculateTime(seekSlider.value);
    if(!audio.paused) {
        cancelAnimationFrame(raf);
    }
});

seekSlider.addEventListener('change', () => {
    audio.currentTime = seekSlider.value;
    if(!audio.paused) {
        requestAnimationFrame(whilePlaying);
    }
});


// SECTION LOADER

const atozQuoteFields = ["name", "reference", "original", "french"];

async function loadQuotes(sectionQuotes, destination) {
    destination.innerHTML = "";
    const quoteTemplate = await fetch(`./templates/atoz-section.html`);
    const quoteTemplateText = await quoteTemplate.text();

    for (let i = 0; i < sectionQuotes.length; i++) {
        var sectionQuoteText = quoteTemplateText;

        for (let j = 0; j < atozQuoteFields.length; j++) {
            const fieldContent = sectionQuotes[i].querySelector(`.${atozQuoteFields[j]}`).innerHTML;
            const field = new RegExp(`#${atozQuoteFields[j]}`);
            sectionQuoteText = sectionQuoteText.replace(field, fieldContent);   
        }

        destination.innerHTML += sectionQuoteText;
    }

    bibliography.dispatchEvent(bibFillEvent);
}

async function loadSub(atozSection) {
    console.log("loading " + atozSection);
    
    var atozSectionName;
    var atozSectionQuotes;
    const atozAudio = `./tentatives/atoz/atoz-${atozSection}.mp3`;;

    // "WHOLE" SECTION
    if (atozSection === "whole") {
        document.getElementById("atoz-section").style.visibility = "hidden";
        atozSectionName = "";
    }
    // ACTUAL SECTION
    else {
        document.getElementById("atoz-section").style.visibility = "visible";

        const response = await fetch(`./tentatives/atoz/atoz-${atozSection}.html`);
        const atoz = await response.text();
        var parser = new DOMParser();
        var atozHTML = parser.parseFromString(atoz, 'text/html');

        atozSectionName = atozHTML.getElementById('section-name').text;
        atozSectionQuotes = atozHTML.getElementsByClassName('atoz-quote');
        
        // Change title
        document.getElementById("atoz-section-title-text").innerHTML = atozSectionName;

        // Change sections
        loadQuotes(atozSectionQuotes, document.getElementById("atoz-content"));

    }

    // Load audio including name
    document.getElementById("atoz-section-title").innerHTML = atozSectionName;
    audio.setAttribute('src', atozAudio);
    audio.load();

    if (atozSection === "whole") {
        
    } else {
        const y = document.getElementById("atoz-section").getBoundingClientRect().top + window.pageYOffset -160;
        window.scrollTo({top: y, behavior: 'smooth'});
    }

}

const buttons = document.querySelectorAll('.subsection-button');

buttons.forEach(button => {
  button.addEventListener('click', function handleClick(event) {
    loadSub(button.getAttribute('atoz-section'));
  });
});

loadSub("whole");
