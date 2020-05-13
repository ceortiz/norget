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
	    //do something
	   // alert('done typ');
	    $.ajax({
	    	type: "POST",
	    	url: "/news/get_data",
	    	data: {
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



