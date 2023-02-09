import { DataBinding } from "./dataBinding.js"

export class Tentative {

	constructor (text) {
		this._text = text;

		this._context = { };

        this._script = null;

        this._dataBinding = new DataBinding();

		this._html = document.createElement('div');
		this._html.innerHTML = text;

		this._title = this._html.querySelectorAll("title")[0].innerText;

	}

    set script(text) {
        this._script = text;
    }

	async runScript(text) {
        this._dataBinding.executeInContext(this._script, this._context, true);
        this._dataBinding.bindAll(this._html, this._context);
	}

    get title() {
        return this._title;
    }

    get date() {
        return this._date;
    }

    /**
     * The HTML DOM node for the slide
     * @returns {HTMLDivElement} The HTML content
     */
    get html() {
        return this._html;
    }

}