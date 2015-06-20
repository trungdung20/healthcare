$(document).ready(function(){ 
	
	//handle thank and agree the answer 
	$('a').click(function() {
		var id = $(this).attr("id")
		if (id == "answer_agree"){
			var answer_agree_id = $(this).attr("data-answerid");
			$.get('/icare/agree_answer',{answer_agree_id: answer_agree_id} , function(data) { 
				$(this).hide();
				$("#answer_agree_count" + answer_agree_id).html(data);
			});
		}
		if (id == "answer_thanks"){ 
			var answer_thanks_id = $(this).attr("data_answerid")
			$.get('/icare/thanks_answer/', {answer_thanks_id: answer_thanks_id}, function(data) { 
				$(this).hide();
				$("#answer_thanks_count"+answer_thanks_id).html(data);
			});
		}
	});
	
	
});