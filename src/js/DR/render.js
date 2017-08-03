"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

exports.default = function (element, index) {
    var targetNode = $("#render-picture");
    var div = document.createElement("div");
    div.className += " pic-container ";
    div.setAttribute("data-id", index);
    //language=HTML
    div.innerHTML = "\n        <div class=\"img-containers\">\n            <div class=\"img-container\">\n                <img src= " + element.smallURL + " alt=\"\">\n            </div>\n        </div>\n        <p class=\"pic-path\">" + element.largePATH + "</p>\n    ";
    targetNode.append(div);
};
//# sourceMappingURL=render.js.map