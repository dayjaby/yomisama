'use strict';
angular.element(document.body).append('<div ng-app="myApp" ng-controller="YomiController"></div>');
var app = angular.module('myApp', []);
app.controller('YomiController', ['$rootScope','$scope','$http','$document', 
function(
	$rootScope,
	$scope,
	$http,
	$document) 
{
    $scope.refreshPopup = function(content,resetScroll) {
        var html = content.body.replace(/qrc:\/\/\/img\/img/g,chrome.extension.getURL("images"))
        $scope.popup.innerHTML = "<div id='yomisama'>" + html + "</div>";
        $($scope.popup).find('#yomisama').on("mousewheel",function(e) {
            var d = e.wheelDelta;
            var jq = $($scope.popup);
            if((jq.scrollTop === (this.scrollHeight - jq.height()) && d < 0) || (jq.scrollTop === 0 && d > 0)) {
                e.preventDefault();
            }
        });
        var $head = $($scope.popup).contents().find("head");
        $head.append($("<link/>",
            { rel: "stylesheet", href: chrome.extension.getURL("styles/main.css"), type: "text/css" }));
        var a = $($scope.popup).contents().find("a")
        .click(function(e) {
            var href = $(e.currentTarget).attr('href');
            console.log("click: ",href);
            if(href == "javascript:void(0);") return;
            chrome.runtime.sendMessage({
                action: "link",
                params: {
                    profile: 'vocabulary',
                    href: href
                }
            },function(response) {
                $scope.refreshPopup(response["vocabulary"],false);
            });
            e.preventDefault();
        });
	    if(resetScroll)
		    $($scope.popup).scrollTop(0);
    };

    $scope.onLookup = function(rp,ro,mm) {
	console.log("onLookup",rp,ro,mm);
        var d = {
            samplePosStart: ro,
            content: rp,
            contentSampleFlat: rp.slice(ro),
            contentSample: rp.slice(ro)
        }
        chrome.runtime.sendMessage({
            action: "lookup",
            params: d
        },function(response) {
            $scope.popup.style.left = mm.clientX + 'px';
            $scope.popup.style.top = (mm.clientY+20) + 'px';
            $scope.popup.style.width = '600px';
            $scope.popup.style.height = '250px';
            $scope.popup.style.bottom = 'initial';
            $scope.popup.style.right = 'initial';
            $scope.popup.style.visibility = 'visible';
            $scope.refreshPopup(response["vocabulary"],true);
        });
    };

    $scope.overPopup = function(x,y) {
        const rect = $scope.popup.getBoundingClientRect();
        return x>=rect.left && x<=rect.right && y>=rect.top && y<=rect.bottom;
    };

    $scope.hidePopup = function() {
        $scope.popup.style.visibility = 'hidden';
    };

    $scope.back = function() {
        chrome.runtime.sendMessage({
            action: "link",
            params: {
                profile: "vocabulary",
                href: "vocabulary_back:0"
            }
        },function(response) {
            console.log(response);
            $scope.refreshPopup(response["vocabulary"],false);
        });
    };

    $scope.next = function() {
        chrome.runtime.sendMessage({
            action: "link",
            params: {
                profile: "vocabulary",
                href: "vocabulary_forward:0"
            }
        },function(response) {
            $scope.refreshPopup(response["vocabulary"],false);
        });
    };

    $scope.maximize = function() {
        $scope.popup.style.left = '15px';
        $scope.popup.style.top = '15px';
        $scope.popup.style.bottom = '50px';
        $scope.popup.style.right = '50px';
        $scope.popup.style.width = 'initial';
        $scope.popup.style.height = 'initial';
    };

    $scope.popup = document.createElement('span');
    $scope.popup.id = 'yomisama-popup';
    $scope.popup.addEventListener('mousedown', function(e) { e.stopPropagation(); });
    $scope.popup.addEventListener('scroll', function(e) { e.stopPropagation(); });

    document.body.appendChild($scope.popup);
    $(document).bind('scroll', function(e) {
        $scope.hidePopup();
    });
    $document.bind('resize', function(e) {
        $scope.hidePopup();
    });
    $document.bind('mousedown', function(e) {
        if(!$scope.overPopup(e.clientX,e.clientY)) {
	        $scope.hidePopup();
        }
    });
    $document.bind('mousemove', function(e) {
        //console.log("mousemove:",e);
        $rootScope.mouseMove = e;
    });
    $document.bind('keypress', function(e) {
	var x = $rootScope.mouseMove.clientX, y = $rootScope.mouseMove.clientY;
        if(e.which == 17 && e.ctrlKey) {
	    var d = document;
            var range = d.caretRangeFromPoint(x,y);
            var rp = range.startContainer;
 	    var ro = range.startOffset;
	    $scope.onLookup(rp.textContent,ro,$rootScope.mouseMove);
        } else if($scope.overPopup(x,y)) {
	    if(e.which == 98) { // b
            $scope.back();        
	    } else if(e.which == 110) { // n
            $scope.next();
	    } else if(e.which == 109) { // m
            $scope.maximize();
        }

	}

        $rootScope.$broadcast('keypress', e);
        $rootScope.$broadcast('keypress:' + e.which, e);
    });
}]);
