(function(){

var routes = ["posts", "replies"];

function pathHandler() {
	var paths = location.pathname.split("/");
	var n = 1
	if (paths.length == 4)
		n = 2
	path = paths[paths.length - n]
    var index = routes.indexOf(path);
    if (path === "")
    	return "posts";
    else if (index === -1)
        return false;
    else
        return path;
}

function routeHandler(to) {

    if (routes.indexOf(to) === -1 && to !== "home"){
        console.error(to, " route not declared.");
        return;
    }

    var curr_path = pathHandler();
    if (to === curr_path)
    	return;

    var href = location.pathname.split("/");
    var n = 1;
	if (href.length == 4){
		href.pop();
	}
	if (to === "posts")
        to = "";
	href[href.length - n] = to
	var go_to = href.join("/");
	console.log(go_to);
    history.pushState(null, null, go_to);
    tabHandler();
}

function linkHandler() {
	// all the tabs
	var links = $(".route-link");
    if (!links.length)
        return;
	links.on("click", function(e) {
        e.preventDefault();
        var to = $(this).parent().data("to");
        routeHandler(to);
    });
}

function activeTabHandler(path) {
	$(".tabs ul li").removeClass("is-active");
	selector = ".tabs ul li[data-to=" + path + "]";
	$(selector).addClass("is-active")
}

function tabHandler() {
	path = pathHandler();

	if (!path)
		return;

	selector = ".route#" + path;
	$(".loading").hide();
	$(".route").hide();
	$(selector).show();

	activeTabHandler(path);
}

function init() {
    // Sets up routing
    tabHandler();
    linkHandler();

    window.onpopstate = function() {
    	tabHandler();
    };
}

init();
})();

$('.content p').contents().unwrap().siblings('p').remove();
$('.reply-author-vue').addClass('is-pulled-down');
$('.content p').contents().unwrap().siblings('p').remove();
$('.reply').hide();
