
function news_previewer(url, div) {
	$.ajax({
			type: "POST",
			url: "/news/get_data",
			data: {
				"news_url": $(url).val(),
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
	var doneTypingInterval = 1000;

	$('#news_url').keyup(function(){
		alert('hi');
	    clearTimeout(typingTimer);
	    if ($(this).val()) {
	        typingTimer = setTimeout(news_previewer('#news_url', '#news_preview'), doneTypingInterval);
	    }
	});

	$('#other_news').keyup(function(){
		alert('hey');
	    clearTimeout(typingTimer);
	    if ($(this).val()) {
	        typingTimer = setTimeout(news_previewer('#other_news', '#other_news_preview'), doneTypingInterval);
	    }
	});

});
