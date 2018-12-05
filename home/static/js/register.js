(function() {

	$("#id_username").on("blur", function() {

		var value = $(this).val();

		if (value.trim() == "")
			return;

		purl = $(this).parent().data("url");
		var data = {
			username: value
		}
		var input = $(this);

		//Username validity
		var regex = new RegExp(/[_a-zA-Z0-9]{2,15}/);
		var rex = regex.exec(value);
		if (!rex || rex[0].length!==value.length){
			input.removeClass("is-success");
			input.addClass("is-danger");
			$(".validation").addClass("is-hidden");
			$("#not_valid").removeClass("is-hidden");
			return false;
		}

		// Username availability 
		$.post(purl, data, function(data){
			var available = data.available;
			if (available){
				input.removeClass("is-danger");
				input.addClass("is-success");
				$(".validation").addClass("is-hidden");
				$("#available").removeClass("is-hidden");
			}
			else {
				input.removeClass("is-success");
				input.addClass("is-danger");
				$(".validation").addClass("is-hidden");
				$("#not_available").removeClass("is-hidden");
			}
		});
	});

})();
