export class Router {

	constructor() {
		this._eventSource = document.createElement("div");

        /**
         * Custom event raised when the route changes
         * @type {CustomEvent}
         */
		this._routeChanged = new CustomEvent("routechanged", {
            bubbles: true,
            cancelable: false
        });

        /**
         * The current route
         * @type {string}
         */
        this._route = null;
        window.addEventListener("popstate", () => {
            if (this.getRoute() !== this._route) {
                this._route = this.getRoute();
                this._eventSource.dispatchEvent(this._routeChanged);
            }
        });
	}

	get eventSource() {
		return this._eventSource;
	}

	setRoute(route) {
		window.location.hash = route;
		this._route = route;
	}

	getRoute() {
		var route = window.location.hash.substr(1).replace(/\//ig, "/");
		/* if no hash, go to ACCUEIL(HOME) */
		if (route === "") {
			route = "accueil";
		}
		return route;
	}
}