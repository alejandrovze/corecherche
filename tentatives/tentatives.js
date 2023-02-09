console.log("loading tentatives ...");

// BIBLIOGRAPHY FILLER
const bibFillEvent = new CustomEvent("bibFill", {
    bubbles: true,
    detail: { yOffset: -60}// Offset for bibliography scroll
});

// HOTGLUE
function resizeHotglue() {

	var width = document.getElementById("hotgluewrapper").offsetWidth;

	// document.getElementById("hotglue").style.zoom = width / 1540;
	document.getElementById("hotglue").style.webkitTransform = "scale(" + (width / 1540) + ")";
	document.getElementById("hotglue").style.mozTransform = "scale(" + (width / 1540) + ")";
	document.getElementById("hotglue").style.oTransform = "scale(" + (width / 1540) + ")";

}

window.addEventListener('resize', resizeHotglue);

resizeHotglue();

// CONTENANT
// If the website is being loaded in itself, 
// then replace the iframe in the embededded website with static image
function iniFrame() {
	console.log("Checking contenant");
    if(window.self !== window.top) {
    	const contenant = document.getElementById("contenant-website");
    	const parent = contenant.parentNode;
    	var contenant_img = document.createElement("img");
    	contenant_img.src = "./media/img/contenant-code.png";
		contenant_img.style["width"] = "100%";
		contenant_img.style["height"] = "auto";
		parent.appendChild(contenant_img);
    	parent.removeChild(contenant);
    }
    else {
    	console.log("Loading contenant");
    }
}
iniFrame();

document.getElementById("bibliography").dispatchEvent(bibFillEvent);

