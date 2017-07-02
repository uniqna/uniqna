(function(){

	var clip = new Clipboard(".link");
	clip.on('success', function(e){
		var ele = $(e.trigger);
		ele.addClass("animated tada");
		setTimeout(function(){
			ele.removeClass("tada");
		}, 1000);
	});

})();
