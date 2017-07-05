(function() {

	$("#id_username").on("blur", function() {

		value = $(this).val();

		if (value.trim() == "")
			return;

		purl = $(this).parent().data("url");
		var data = {
			username: value
		}
		input = $(this);

		$.post(purl, data, function(data){
			var available = data.available;
			if (available){
				input.removeClass("is-danger");
				input.addClass("is-success");
				$("#available").removeClass("is-hidden");
				$("#not_available").addClass("is-hidden");
			}
			else {
				input.removeClass("is-success");
				input.addClass("is-danger");
				$("#not_available").removeClass("is-hidden");
				$("#available").addClass("is-hidden");
			}
		});

	});

})();
