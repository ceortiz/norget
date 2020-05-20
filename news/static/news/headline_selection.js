$(document).ready(function() {
	var typingTimer;                //timer identifier
	var doneTypingInterval = 1000;

	$("#headline").keyup(function() {
		clearTimeout(typingTimer);
	    if ($(this).val()) {
	        typingTimer = setTimeout(doneTyping, doneTypingInterval);
	    }
	});

	function doneTyping() {
		alert($("#headline").val());
		$.ajax({
			type: "POST",
			url: "/news/headlines",
			data: {
				"news_title": $("#news_title").val(),
				"keyword": $("#headline").val(),
				"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
			},
			dataType: 'html',
			success: function(data) {
				$("#headlines").html(data);
			}
		});
	}
});