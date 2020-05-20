$(document).ready(function(){
	//setup before functions
	var typingTimer;                //timer identifier
	var doneTypingInterval = 1000;  //time in ms (5 seconds)

	//on keyup, start the countdown
	$('#news_url').keyup(function(){
	    clearTimeout(typingTimer);
	    if ($(this).val()) {
	        typingTimer = setTimeout(doneTyping, doneTypingInterval);
	    }
	});

	//user is "finished typing," do something
	function doneTyping () {
	    //get the chosen category
	    //query by looking for news_url or title under the same category
	    //query for heading
	    $.ajax({
	    	type: "POST",
	    	url: "/news/get_data",
	    	data: {
	    		//"category": $("#categories").val(),
	    		"news_url": $('#news_url').val(),
	    		"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
	    	},
	    	dataType: 'html',
	    	success: function(data) {
	    		//show news preview
	    		$('#news_preview').html(data);
	    	}
	    });
	}
});



