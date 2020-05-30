
function displayer(headline, div) {
	$.ajax({
			type: "POST",
			url: "/news/headlines",
			data: {
				"news_title": $("#news_title").val(),
				"keyword": $(headline).val(),
				"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
			},
			dataType: 'html',
			success: function(data) {
				$(div).html(data);
			}
		});
}

$(document).ready(function() {
	var typingTimer;                //timer identifier
	var doneTypingInterval = 3000;


	$("#headline").keyup(function() {
		clearTimeout(typingTimer);
		if($(this).val()) {
			typingTimer = setTimeout(displayer('#headline', '#headlines'), doneTypingInterval);
		}
	});


	$("#orig_headline").keyup(function() {
		clearTimeout(typingTimer);
		if($(this).val()) {
			typingTimer = setTimeout(displayer('#orig_headline', '#orig_headlines'), doneTypingInterval);
		}
	});

	$("#counterheadline").keyup(function() {
		clearTimeout(typingTimer);
		if($(this).val()) {
			typingTimer = setTimeout(displayer('#counterheadline', '#counterheadlines'), doneTypingInterval);
		}
	});

});
