'use strict';

var _myGallery = require('./myGallery');

require('./index/indexentry.js');
console.log("ddd");
require('./lib/particles.js');
require('../styles/common/common.css');
require('../styles/common/nav-container.css');
require('../styles/index/search-bar.css');
require('./DR/render');

console.log("This is index.js");
console.log(_myGallery.searchPath);
console.log(JSON.parse(localStorage.getItem("searchPath")));
console.log("This is index.js");
/* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
particlesJS.load('particles-js', "../../../assets/particles.json", function () {
    console.log('callback - particles.js config loaded');
});

var sendData = {};
/*
const allData = [
    {
        smallURL: "../static/img/banner.jpg",
        largeURL: "../static/img/banner.jpg",
        largePATH: "../static/img/banner.jpg",
    }
];
*/

var ajax = new XMLHttpRequest();

/*
ajax.open("POST","/search",true);
ajax.setRequestHeader("Content-type","application/json");
ajax.send(JSON.stringify(data));
*/
var searchBar = $("#search-input");
var searchInfo = searchBar.val();
//监听搜索的回车事件，并进一步执行程序。监听到有输入即跳转到搜索结果的页面

searchBar.bind("keydown", function (event) {
    //监听回车事件
    var searchInfo = searchBar.val();
    event = event || window.event;
    if (event.keyCode === 13) {
        if (searchInfo.length !== 0) {
            window.location.href = '../../../displayResult.html'; //跳转页面
            localStorage["searchInfo"] = searchInfo;
            ajax.open("POST", "/search", true);
            ajax.setRequestHeader("Content-type", "application/json");
            ajax.onreadystatechange = function () {
                console.log(this.readyState);
                if (this.readyState === 4) {
                    //Todo
                    console.log(this.responseText);
                    localStorage.setItem("ddd", this.responseText);

                    /*allData = [
                        {
                            smallURL: "../static/img/banner.jpg",
                            largeURL: "../static/img/banner.jpg",
                            largePATH: "../static/img/banner.jpg",
                        }
                    ];*/
                }
            };
            sendData.keyword = searchInfo;
            sendData.path = _myGallery.searchPath;
            //这里要向服务器发送请求。
            ajax.send(JSON.stringify(sendData));
        } else {}
    }
}, false);
//# sourceMappingURL=index.js.map