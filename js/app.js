import { registerNavigation } from "./navigation.js"
import { registerViewDeck } from "./viewHandler.js"
import { registerBibliography } from "./bibliography.js"

const app = async() => {
	console.log("loading main app");
	registerNavigation();
	registerViewDeck();
	registerBibliography();
}


document.addEventListener("DOMContentLoaded", app);