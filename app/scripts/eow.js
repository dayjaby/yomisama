var results = $("#resultsList").find("li");
var index = 0;
var definitions = $.map(results,function(el){
    if(el.children.length<3) return undefined;
    var definition = {
        'filename': window.location.href,
        'text': el.children[0].innerText,
        'translation': el.children[1].innerText.replace(/(?:\r\n|\r|\n)/g, '<br />')
    };
    var i = index;
    $(el).find(".fukidashi").remove();
    $(el).find(".tango_btn").unbind("click").bind("click",function(e) {
        console.log(i);
        chrome.runtime.sendMessage({
	        action: "link",
	        params: {
                profile: 'sentence',
                href: 'sentence_add:' + i
            }
        },function(response) {
            $(el).find(".tango_btn").remove();
        });    
    });
    index += 1;
    return definition;
});
chrome.runtime.sendMessage({
	action: "set",
	params: {
        profile: 'sentence',
        definitions: definitions
    }
},function(response) {
    console.log(response);
});
