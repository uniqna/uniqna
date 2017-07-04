(function(){

	$("#toggle_email_form").on("change", function() {
		var purl = $(this).attr("action");

		var data = {
			toggle: $("input[name=emailpref]:checked").val()
		}

		$.post(purl, data).fail(function(data){
        console.error("Email toggle failed.");
    });
	});

})();
