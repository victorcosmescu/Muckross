/*contact form validation*/
$(document).ready(function() {

	$("#contact-form").submit( function(event) {
		
		var is_error = false;
		var error_fullname = 0;
		var error_email = 0;
		var error_textarea= 0;

		var fullname = $("#fullname").val();
		if(fullname == ""){
			$("input#fullname").css("border-color", "#ff3333");
			is_error = true;
			error_fullname = 1;
		}

		var email = $("#email").val();
		if(email == ""){
			$("input#email").css("border-color", "#ff3333");
			is_error = true;
			error_email = 1;
		}

		var description = $("#description").val();
		if(description == ""){
			$("textarea#description").css("border-color", "#ff3333");
			is_error = true;
			error_textarea = 1;
		}

		if (is_error == true && error_fullname == 1 && error_email == 0 && error_textarea == 0){
			$("span#error-count").text("full name field");
			$("p#error-list").css("display", "block");
			event.preventDefault();
		}
		else if (is_error == true && error_fullname == 0 && error_email == 1 && error_textarea == 1){
			$("span#error-count").text("email and description fields");
			$("p#error-list").css("display", "block");
			event.preventDefault();
		}
		else if (is_error == true && error_email == 1 && error_fullname == 1 && error_textarea == 0){
			$("span#error-count").text("fullname and email fields");
			$("p#error-list").css("display", "block");
			event.preventDefault();
		}
		else if (is_error == true && error_email == 0 && error_fullname == 0 && error_textarea == 1) {
			$("span#error-count").text("description field");
			$("p#error-list").css("display", "block");
			event.preventDefault();
		}
		else if (is_error == true && error_email == 1 && error_fullname == 1 && error_textarea == 1) {
			$("span#error-count").text("fullname, email and description fields");
			$("p#error-list").css("display", "block");
			event.preventDefault();
		}
		
	});

	$("#fullname").focusout(function() {
		$("input#fullname").css("border-color", "#D8000C");
	});
	$("#email").focusout(function() {
		$("input#email").css("border-color", "#D8000C");
	});
	$("#description").focusout(function() {
		$("textarea#description").css("border-color", "#D8000C");
	});
	
	
});


