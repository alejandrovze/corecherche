import { Tentative } from "./tentative.js"

export async function loadTentative(tentativeName) {
    const response = await fetch(`./tentatives/${tentativeName}.html`);
    const tentative = await response.text();

   	var newTentative =  new Tentative(tentative);

   	const responseScript = await fetch(`./tentatives/${tentativeName}.js`);
   	const tentativeScript = await responseScript.text();

   	newTentative.script = tentativeScript;

    return newTentative;
}