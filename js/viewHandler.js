import { loadTentative } from "./tentativeLoader.js"
import { Tentative } from "./tentative.js"
import { Router } from "./router.js"

export class ViewHandler extends HTMLElement {

	constructor() {
		super();

		/* implement router */

		this._router = new Router();
        this._route = this._router.getRoute();

        this.loadView();

		this._router.eventSource.addEventListener("routechanged", () => {

		    if (this._route !== this._router.getRoute()) {
		        this._route = this._router.getRoute();
		        if (this._route) {
		            this.loadView();
		        }
		    }
		});
	}

	async loadView() {
		this._tentative = await loadTentative(this._route);
		this.innerHTML = '';
		this.appendChild(this._tentative.html);
		document.title = this._tentative.title;

		/* Run associated script once HTML is loaded */
        await this._tentative.runScript();
        /* Scroll to top */
        window.scrollTo({top: 0, behavior: 'smooth'});
	}


}

export const registerViewDeck = () => customElements.define('view-deck', ViewHandler);