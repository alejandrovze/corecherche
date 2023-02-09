/* NAVIGATION BAR */

export class Navigation extends HTMLElement {

	constructor() {
		super();
	}

	async connectedCallback() {

		const response = await fetch("./templates/navigation.html")
		const template = await response.text();
		this.innerHTML = "";

		const host = document.createElement("div");
		host.innerHTML = template;
		this.appendChild(host);

		/* EVENT LISTENERS ETC. */

	}

}

export const registerNavigation = () => customElements.define('navigation-bar', Navigation);