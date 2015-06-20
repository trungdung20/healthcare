$(document).ready(function(){ 
	 alert('Hello world!');
	//handle thank and agree the answer 
	$('.button tiny').click(function() {
		var id = $(this).attr("id")
		if (id == "answer_agree"){
			var answer_agree_id = $(this).attr("data-answerid");
			$.get('/icare/agree_answer',{answer_agree_id: answer_agree_id} , function(data) { 
				$(this).hide;
				$("#answer_agree_count" + answer_agree_id).html(data);
			});
		}
		if (id == "answer_thanks"){ 
			var answer_thanks_id = $(this).attr("data_answerid")
			$.get('/icare/thanks_answer/', {answer_thanks_id: answer_thanks_id}, function(data) { 
				$(this).hide;
				$("#answer_thanks_count"+answer_thanks_id).html(data);
			});
		}
	});
	//handle checklist and checklist item 
	$('.button tiny').click(function(){
		var id = $(this).attr('id');
		if(id == "item_complete"){
			var item_id = $(this).attr("data-itemid");
			$.get('/icare/user_checklist_item/complete/',{item_id:item_id},function(data) {
				$(this).hide;
				
			});
		}
		if(id="checklist_delete"){
			var checklist_id = $(this).attr("data-listid");
			$.get('/icare/checklist/delete/',{checlist_id:checklist_id},function(data){ 
				$.(this).hide;
			})
		}
	});
	
	//handle checklist thank, agree 
	$('.button tiny').click(function() {
		var id = $(this).attr("id");
		if (id == "agree_checklist"){ 
			var checklist_agree_id = $(this).attr("data-listid");
			$.get('/icare/agree_checklist/', {checklist_agree_id: checklist_agree_id}, function(data) {
				$(this).hide;
				$('#checklist_agree_count'+checklist_agree_id).html(data);
			});
		}
		if (id == "thanks_checklist"){ 
			var checklist_thanks_id = $(this).attr("data-listid");
			$.get('/icare/thanks_checklist/',{checklist_thanks_id: checklist_thanks_id} , function(data) {
				$(this).hide;
				$('#checklist_thanks_count'+ checklist_thanks_id).html(data);
			});
		}
		if (id == "add_checklist"){
			var checklist_add_id = $(this).attr("data-listid");
			$.get('/icare/add_checklist/',{checklist_add_id: checklist_add_id}, function(data){ 
				$.(this).hide;
				$.('#checklist_add_id'+ checklist_add_id).html(data);
			});
		}
	});
	// handle patient doctor relationship
	$('#add_friend_patient').click(function() { 
		var patientid;
		patientid = $(this).attr("data-id");
		$.get('/icare/patient_care_list_request/',{patientid: patientid} , function(data) {
			$('#add_friend_patient').hide;
		});
	});
	$('#add_friend_doctor').click(function() { 
		var doctorid;
		doctorid = $(this).attr("data-id");
		$.get('/icare/doctor_care_list_request', {doctorid: doctorid} , function(data) { 
			$(this).hide;
		})
	});
	
	$('.button tiny').click(function() {
		
		var id; 
		id = $(this).attr("id")
		
		if (id == "patient_accept") {
			var patient_accept_id = $(this).attr("data-id");
			$.get('/icare/request/accept/patient/', {patientid: patient_accept_id}, function(data) { 
				$(this).hide; 
			});
		}
		if (id == "patient_reject") {
			var patient_reject_id = $(this).attr("data-id");
			$.get('/icare/request/reject/patient/', {patientid : patient_reject_id}, function(data) {
				$(this).hide;
			});
		}
		if (id == "doctor_accept"){ 
			var doctor_accept_id = $(this).attr("data-id");
			$.get('/icare/request/accept/doctor/', {doctorid : doctor_accept_id}, function(data) { 
				$(this).hide; 
			});
		} 
		if (id == "doctor_reject"){ 
			var doctor_reject_id = $(this).attr("data-id"); 
			$.get('/icare/request/reject/doctor/', {doctorid: doctor_reject_id}, function(data){ 
				$(this).hide;
			});
		}
	});
	//edit patient's weight 
	$("#weight_update").click(function() { 
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/weigth/edit/',{patient_record_id: patient_record_id}, function(data) { 
			$("#weight_edit").append(data);
		});
	});
	$("#patient_weight_submit").submit(function() { 
		even.preventDefault();
		$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType: 'html',
			success: function(response)(
				$("#weight").html(response);
				$("#weight_edit").empty();
			)
		});
		return false;
	});
	//edit patient height 
	$("#height_update").click(function() {
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/height/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#height_edit").append(data);
		});
		
	});
	
	$("#patient_height_submit").submit(function() { 
		even.preventDefault(); 
		$.ajax({ 
			data:$(this).serialize(),
			type:$(this).attr('method'),
			url:$(this).attr('action'),
			dataType: 'html',
			success: function(response)(
				$("#height").html(response);
				$("#height_edit").empty();
			)
		});
	});
	// edite patient ethnicity 
	$('#ethnicity_update').click(function() {
		var patient_record_id = $(this).attr("data-id");
		S(this).hide();
		$.get('/icare/patient/ethnicity/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#ethnicity_edit").append(data);
		});
	});
	
	$("#patient_ethnicity_submit").submit(function() { 
		even.preventDefault(); 
		$.ajax({ 
			data:$(this).serialize(),
			type:$(this).attr('method'),
			url:$(this).attr('action'),
			dataType: 'html',
			success: function(reponse)(
				$("#ethnicity").html(response);
				$("#ethnicity_edit").empty();
			)
		});
	});
	//edit vaccination 
	$("#vaccination_update").click(function() {
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/vaccination/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#vaccination_edit").append(data);
		});
		
	});
	
	$("#patient_vaccination_submit").submit(function() { 
		even.preventDefault(); 
		$.ajax({ 
			data:$(this).serialize(),
			type:$(this).attr('method'),
			url:$(this).attr('action'),
			dataType: 'html',
			success: function(response)(
				$("#vaccination").html(response);
				$("#vaccination_edit").empty();
			)
		});
	});
	//edit dietary restriction 
	$("#dietary_restriction_update").click(function() {
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/dietary/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#dietary_restriction_edit").append(data);
		});
		
	});
	
	$("#patient_vaccination_submit").submit(function() { 
		even.preventDefault(); 
		$.ajax({ 
			data:$(this).serialize(),
			type:$(this).attr('method'),
			url:$(this).attr('action'),
			dataType: 'html',
			success: function(response)(
				$("#dietary_restriction").html(response);
				$("#dietary_restriction_edit").empty();
			)
		});
	});
	//edit alcohol 
	$("#alcohol_update").click(function() {
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/alcohol/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#alcohol_edit").append(data);
		});
		
	});
	
	$("#alcohol_submit").submit(function() { 
		even.preventDefault(); 
		$.ajax({ 
			data:$(this).serialize(),
			type:$(this).attr('method'),
			url:$(this).attr('action'),
			dataType: 'html',
			success: function(response)(
				$("#alcohol").html(response);
				$("#alcohol_edit").empty();
			)
		});
	});
	//edit tobacco 
	$("#tobacco_update").click(function() {
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/tobacco/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#tobacco_edit").append(data);
		});
		
	});
	
	$("#tobacco_submit").submit(function() { 
		even.preventDefault(); 
		$.ajax({ 
			data:$(this).serialize(),
			type:$(this).attr('method'),
			url:$(this).attr('action'),
			dataType: 'html',
			success: function(response)(
				$("#tobacco").html(response);
				$("#tobacco_edit").empty();
			)
		});
	});
	//edit sex 
	$("#sex_update").click(function() {
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/sex/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#sex_edit").append(data);
		});
		
	});
	
	$("#sex_submit").submit(function() { 
		even.preventDefault(); 
		$.ajax({ 
			data:$(this).serialize(),
			type:$(this).attr('method'),
			url:$(this).attr('action'),
			dataType: 'html',
			success: function(response)(
				$("#sex").html(response);
				$("#sex_edit").empty();
			)
		});
	});
	//edit drug 
	$("#recreational_drug_update").click(function() {
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/recreational_drug/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("recreational_drug_edit").append(data);
		});
		
	});
	
	$("#recreational_drug_submit").submit(function() { 
		even.preventDefault(); 
		$.ajax({ 
			data:$(this).serialize(),
			type:$(this).attr('method'),
			url:$(this).attr('action'),
			dataType: 'html',
			success: function(response)(
				$("#recreational_drug").html(response);
				$("#recreational_drug_edit").empty();
			)
		});
	});
	//apend new item in checklist 
	$("#add_new_item").click(function() {
		var checklist_id = $(this).attr("data-checklistid");
		$.get('/icare/item/add/',{checklist_id:checklist_id},function(data){ 
			$("new_item").append(data);
		});
		
	});
	$("form").submit(function(){ 
		event.preventDefault();
		$.ajax({ 
			data:$(this).serialize;
			type: $(this).attr('method');
			url:$(this).attr('action');
			dataType:'html';
			success:function(response){
				alert('submitted');
			}
		});
	});
	$('span.stars').stars();
	$("#test").click(function(){ 
		$(this).hide();
	});
});

$.fn.stars = function(){
	return $(this).each(function(){ 
	//get the value 
	var val = parseFloat($(this).html());
	//Make sure that the value is in 0-5 range, multiply to get width
	
	var size = Math.max(0,(Math.min(5,val))) * 16;
	//Create stars holder
	var $span = $('<span/>').width(size);
	//Replace the numberical value with stars
	$(this).html($span);
	});
}