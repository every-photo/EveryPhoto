"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

exports.default = function (element, index) {
    var targetNode = $("#gallery-container");
    var div = document.createElement("div");
    div.setAttribute("data-id", index);
    div.className += ' ga-bar ';
    div.setAttribute("chooseornot", "");

    var searchPathArray = JSON.parse(localStorage.getItem("searchPathArray"));
    if (searchPathArray.indexOf(parseInt(index)) >= 0) {
        console.log("YESSSSSSS!!");
        div.setAttribute("chooseornot", "yes");
        div.innerHTML = "\n        <div class=\"choose-path choose\" >\n            <p></p>\n        </div>\n        <p class=\"lib-name\">" + element.name + "</p>\n        <p class=\"lib-path\">" + element.path + "</p>\n    ";
    } else {
        div.innerHTML = "\n        <div class=\"choose-path\" >\n            <p></p>\n        </div>\n        <p class=\"lib-name\">" + element.name + "</p>\n        <p class=\"lib-path\">" + element.path + "</p>\n    ";
    }
    targetNode.prepend(div);
};
//# sourceMappingURL=renderLIB.js.map