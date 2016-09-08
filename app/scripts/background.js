'use strict';

chrome.runtime.onMessage.addListener(function (request, sender, callback) {
    const xhr = new XMLHttpRequest();
    xhr.addEventListener('loadend', function() {
        const resp = xhr.responseText;
        callback(resp ? JSON.parse(resp) : null);
    });
    xhr.open('POST', 'http://127.0.0.1:8766');
    xhr.send(JSON.stringify({action:request.action, params:request.params}));
    return true;
});
