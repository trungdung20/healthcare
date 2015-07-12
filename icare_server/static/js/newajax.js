

$('#ethnicity_update').click(function() {
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/ethnicity/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#ethnicity_edit").html(data);
			$("#ethnicity_update").hide();
		});
});

//edit patient's weight 
	$("#weight_update").click(function() { 
		$("#weight_update").hide();
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/weight/edit/',{patient_record_id: patient_record_id}, function(data) { 
			$("#weight_edit").html(data);
			
			});
	});
	
//edit patient height 
$("#height_update").click(function() {
		$("#height_update").hide();
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/height/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#height_edit").html(data);
			
		});
		
});
	
//edit vaccination 
	$("#vaccination_update").click(function() {
		$("#vacination_update").hide();
		
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/vaccination/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#vaccination_edit").html(data);
			
		});
		
	});
	
//edit dietary restriction 
$("#dietary_restriction_update").click(function() {
		$("#dietary_restriction_update").hide();
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/dietary/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#dietary_restriction_edit").html(data);
			
		});
		
});
	
//edit alcohol 
$("#alcohol_update").click(function() {
		$("#alcohol_update").hide();
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/alcohol/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#alcohol_edit").html(data);
			
		});
});
	
	//edit tobacco 
	$("#tobacco_update").click(function() {
		$("#tobacco_update").hide();
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/tobacco/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#tobacco_edit").html(data);
			
		});
		
	});
	
	//edit sex 
$("#sex_update").click(function() {
		
		$("#sex_update").hide();
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/sex/edit/',{patient_record_id:patient_record_id}, function(data) { 
			$("#sex_edit").html(data);
			
		});
		
});
	
	//edit drug 
$("#recreational_drug_update").click(function() {
		$("#recreational_drug_update").hide();
		var patient_record_id = $(this).attr("data-id");
		$.get('/icare/patient/recreational_drug/edit/',{patient_record_id:patient_record_id}, function(data){ 
			
			$("#recreational_drug_edit").html(data);
		});
		
});


	
// handle patient doctor relationship
$('#add_friend_patient').click(function() { 
		var patientid;
		$('#add_friend_patient').hide();
		patientid = $(this).attr("data-id");
		
		$.get('/icare/patient_care_list_request/',{patientid: patientid} , function(data) {
			
		});
		
});
	
$('#add_friend_doctor').click(function() { 
		var doctorid;
		$('#add_friend_doctor').hide();
		doctorid = $(this).attr("data-id");
		$.get('/icare/doctor_care_list_request/', {doctorid: doctorid} , function(data) { 
			
		})
});

$('#add_advisor_doctor').click(function(){ 
	var doctorid = $(this).attr("data-id");
	$('#add_advisor_doctor').hide();
	$.get('/icare/request/patient/send/advisor_request/',{doctorid:doctorid},function(data){
		
		
	});
});	

$('a').click(function() {
		var id; 
		id = $(this).attr("id");
		//doctor accpet friend request
		if (id == "patient_accept") {
			var patient_accept_id = $(this).attr("data-id");
			$.get('/icare/request/accept/patient/', {patientid: patient_accept_id}, function(data) { 
				$("#patient_friend_request"+patient_accept_id).fadeOut(); 
			});
		}
		//doctor request frined request
		if (id == "patient_reject") {
			var patient_reject_id = $(this).attr("data-id");
			
			$.get('/icare/request/reject/patient/', {patientid : patient_reject_id}, function(data) {
				$("#patient_friend_request"+patient_reject_id).fadeOut();
			});
		}
		//patient reject friend request 
		 if (id == "doctor_accept"){ 
			var doctor_accept_id = $(this).attr("data-id");
			
			$.get('/icare/request/accept/doctor/', {doctorid : doctor_accept_id}, function(data) { 
				$("#doctor_friend_request"+doctor_accept_id).fadeOut(); 
			});
		} 
		//patient reject friend request 
		if (id == "doctor_reject"){ 
			var doctor_reject_id = $(this).attr("data-id"); 
			
			$.get('/icare/request/reject/doctor/', {doctorid: doctor_reject_id}, function(data){ 
				$("#doctor_friend_request"+doctor_reject_id).fadeOut();
			});
		}
		//patient viewed friend reject 
		if (id=="doctor_view_rejected"){
			
			var doctor_view_accepted_id = $(this).attr("data-id");
			$.get('/icare/patient/view_rejected_request/',{doctorid : doctor_view_accepted_id},function(data){ 
			$("#doctor_reject_friend_request"+doctor_view_accepted_id).fadeOut();
			
			});
			
		//patient view friend accept 
		}
		if (id == "doctor_view_accepted"){
			var doctor_view_accepted_id = $(this).attr("data-id");
			
			$.get('/icare/patient/view_accepted_request/',{doctorid : doctor_view_accepted_id},function(data){ 
			$("#doctor_accept_friend_request"+doctor_view_accepted_id).fadeOut();
			
			});
			}
		//patient view advisore reuqest accpet 
		if (id =="doctor_advisor_accepted"){
			var doctor_advisor_accepted_id =$(this).attr("data-id");
			
			$.get('/icare/patient/doctor_advisor_accepted/',{doctorid:doctor_advisor_accepted_id},function(data) { 
				$("#doctor_accept_advisor_request"+doctor_advisor_accepted_id).fadeOut();
			});
			
			}
		//patient view advisore request rejected
		if (id =="doctor_advisor_rejected"){
			var doctor_advisor_rejected_id =$(this).attr("data-id");
			
			$.get('/icare/patient/doctor_advisor_rejected/',{doctorid:doctor_advisor_rejected_id},function(data) { 
			$("#doctor_reject_advisor_request"+doctor_advisor_rejected_id).fadeOut();
				
			});
			
			}
		//patient view answered laert 
		 if (id =="doctor_answer_alert"){
			var answer_alert_id = $(this).attr("data-id");
			
			$.get('/icare/patient/doctor_answer_alert/',{answerid:answer_alert_id},function(data){ 
				$("#doctor_answer_alert"+answer_alert_id).fadeOut();
			});
			
		}
		//doctor view rejected request 
		if (id == "patient_view_rejected"){
			var patient_view_accepted_id = $(this).attr("data-id");
			
			$.get('/icare/doctor/view_rejected_request/',{patientid :patient_view_accepted_id},function(data){ 
			$("#patient_friend_reject"+patient_view_accepted_id).fadeOut();
			
			});
			}
		//doctor view accepted request 
		if (id == "patient_view_accepted"){
			var patient_view_rejected_id = $(this).attr("data-id");
			
			$.get('/icare/doctor/view_accepted_request/',{patientid:patient_view_rejected_id},function(data){ 
			$("#patient_friend_accept"+patient_view_rejected_id).fadeOut();
			
			});
			}
		//doctor accepted advisor 
		 if (id =="patient_advisor_accept"){
			var patient_advisor_request_id =$(this).attr("data-id");
			
			$.get('/icare/doctor/patient_advisor_accept/',{patientid:patient_advisor_request_id},function(data) { 
				$("#patient_advisor_request"+patient_advisor_request_id).fadeOut(); 
				
				});
			}
		//doctor rejected advisor 
		if (id =="patient_advisor_reject"){
			var patient_advisor_request_id =$(this).attr("data-id");
			
			$.get('/icare/doctor/patient_advisor_reject/',{patientid:patient_advisor_request_id},function(data) { 
				$("#patient_advisor_request"+patient_advisor_request_id).fadeOut(); 
				
				});
			}
		//doctor view question alert 	
		if (id == "patient_question_alert"){
			
			var question_alert_id = $(this).attr("data-id");
			
			$.get('/icare/doctor/patient_question_alert/',{questionid:question_alert_id},function(data){ 
				$("#patient_question_alert"+question_alert_id).fadeOut();
			});
			
		}
		if(id =="patient_reject_advisor"){
			var patient_id = $(this).attr("data-id");
			
			$.get('/icare/patient/reject_current_advisor/',{patient_id:patient_id},function(data){
				$("#patient_reject_advisor").fadeOut();
			});
		}
		//doctor view thanks answer 
		if(id=="doctor_thanks_answer_alert"){
			var doctor_thanks_answer_follow_id = $(this).attr("data-id");
			
			$.get("/icare/doctor/thanks_answer_follow/",{doctor_thanks_answer_follow_id:doctor_thanks_answer_follow_id},function(data){
				$("#doctor_thanks_answer"+doctor_thanks_answer_follow_id).fadeOut();
			});
			
		}
		//dcotor view agree answer 
		
		if(id=="doctor_agree_answer_alert"){
			var doctor_agree_answer_follow_id = $(this).attr("data-id");
			
			$.get("/icare/doctor/agree_answer_follow/",{doctor_agree_answer_follow_id:doctor_agree_answer_follow_id},function(data){
				$("#doctor_agree_answer"+doctor_agree_answer_follow_id).fadeOut();
			});
			
		}
		//doctor view agrre checklist 
		
		if(id=="doctor_agree_checklist_alert"){
			var doctor_agree_checklist_follow_id = $(this).attr("data-id");
			
			$.get("/icare/doctor/agree_checklist_follow/",{doctor_agree_checklist_follow_id:doctor_agree_checklist_follow_id},function(data){
				$("#doctor_agree_checklist"+doctor_agree_checklist_follow_id).fadeOut();
			});
			
		}
		//doctor thanks checklist 
			if(id=="doctor_thanks_checklist_alert"){
			var doctor_thanks_checklist_follow_id = $(this).attr("data-id");
			
			$.get("/icare/doctor/thanks_checklist_follow/",{doctor_thanks_checklist_follow_id:doctor_thanks_checklist_follow_id},function(data){
				$("#doctor_thanks_checklist"+doctor_thanks_checklist_follow_id).fadeOut();
			});
			
		}
		//doctor view add related topic to topic follow
		if(id=="doctor_add_related_topic_follow_alert"){
			var doctor_add_related_topic_follow_id = $(this).attr("data-id");
			
			$.get("/icare/doctor/add_related_topic_follow/",{doctor_add_related_topic_follow_id:doctor_add_related_topic_follow_id},function(data) {
				$("#doctor_add_related_topic_follow"+doctor_add_related_topic_follow_id).fadeOut();
			});
		}
		//doctor view edit topic follow 
		if(id=="doctor_edit_topic_follow_alert"){
			var doctor_edit_topic_follow_id = $(this).attr("data-id");
		
			$.get("/icare/doctor/edit_topic_follow/",{doctor_edit_topic_follow_id:doctor_edit_topic_follow_id},function(data) {
					$("#doctor_edit_topic_follow"+doctor_edit_topic_follow_id).fadeOut();
			});
		}
		//doctor view add answer follow 
		if(id=="doctor_add_answer_topic_follow_alert"){
			var doctor_add_answer_topic_follow_id = $(this).attr("data-id");
			
			$.get("/icare/doctor/add_answer_topic_follow/",{doctor_add_answer_topic_follow_id:doctor_add_answer_topic_follow_id},function(data) {
				$("#doctor_add_answer_topic_follow"+doctor_add_answer_topic_follow_id).fadeOut();
			});
		}
		//doctor view add question follow 
		if(id=="doctor_add_question_topic_follow_alert"){
			var doctor_add_question_topic_follow_id = $(this).attr("data-id");
			
			$.get("/icare/doctor/add_question_topic_follow/",{doctor_add_question_topic_follow_id:doctor_add_question_topic_follow_id},function(data) {
				$("#doctor_add_question_topic_follow"+doctor_add_question_topic_follow_id).fadeOut();
			});
		}
		//patient view add topic follow 
		if(id=="patient_add_related_topic_follow_alert"){
			var patient_add_related_topic_follow_id = $(this).attr("data-id");
			
			$.get("/icare/patient/add_related_topic_follow/",{patient_add_related_topic_follow_id:patient_add_related_topic_follow_id},function(data) {
				$("#patient_add_related_topic_follow"+patient_add_related_topic_follow_id).fadeOut();
			});
		}
		//patient view edit topic follow 
		if(id=="patient_edit_topic_follow_alert"){
			var patient_edit_topic_follow_id = $(this).attr("data-id");
			
			$.get("/icare/patient/edit_topic_follow/",{patient_edit_topic_follow_id:patient_edit_topic_follow_id},function(data) {
				$("#patient_edit_topic_follow"+patient_edit_topic_follow_id).fadeOut();
			});
		}
		//patient view  add answer follow 
		if(id=="patient_add_answer_topic_follow_alert"){
			var patient_add_answer_topic_follow_id = $(this).attr("data-id");
			
			$.get("/icare/patient/add_answer_topic_follow/",{patient_add_answer_topic_follow_id:patient_add_answer_topic_follow_id},function(data) {
				$("#patient_add_answer_topic_follow"+patient_add_answer_topic_follow_id).fadeOut();
			});
		}
		//patient view add question follow 
		if(id=="patient_add_question_topic_follow_alert"){
			var patient_add_question_topic_follow_id = $(this).attr("data-id");
			
			$.get("/icare/patient/add_question_topic_follow/",{patient_add_question_topic_follow_id:patient_add_question_topic_follow_id},function(data) {
				$("#patient_add_question_topic_follow"+patient_add_question_topic_follow_id).fadeOut();
			});
		}
		return;
});	

$('#topic_agree').click(function() {
	var topic_id = $(this).attr("data-id");
	$("#topic_agree").hide();
	$.get('/icare/doctor/agree_topic/',{topic_id:topic_id},function(data){
				
	});
});

$('a').click(function() { 
	var id = $(this).attr('id');
	//patient view answer post by doctor 
		if(id == "doctor_answer_follow"){
			var answer_follow_id = $(this).attr("data-id");
			$("#doctor_answer_follow"+answer_follow_id).fadeOut();
			$.get('/icare/patient/answer_follow_handles/',{answer_follow_id:answer_follow_id},function(data){
				
			});
		}
		//patient view new add topic 
		if(id =="doctor_add_topic"){
			var add_topic_id = $(this).attr("data-id");
			$("#doctor_add_topic"+add_topic_id).fadeOut();
			$.get("/icare/patient/view_add_topic_handles/",{add_topic_id:add_topic_id},function(data){ 
				
			});
		}
		
		//patient view new edit topic 
		if(id =="doctor_edit_topic"){
			var edit_topic_id = $(this).attr("data-id");
			$("#doctor_edit_topic"+edit_topic_id).fadeOut();
			$.get("/icare/patient/view_edit_topic_handles/",{edit_topic_id:edit_topic_id},function(data){ 
				
			});
		}
		// patient view new add checklist 
		if(id == "doctor_add_checklist"){
			var add_checklist_id = $(this).attr("data-id");
			$("#doctor_add_checklist"+add_checklist_id).fadeOut();
			$.get("/icare/patient/view_add_checklist_handles/",{add_checklist_id:add_checklist_id},function(data){ 
				
			});
		}
		//patient view new add checklsit
		if(id == "doctor_edit_checklist"){
			var edit_checklist_id = $(this).attr("data-id");
			$("#doctor_edit_checklist"+edit_checklist_id).fadeOut();
			$.get("/icare/patient/view_edit_checklist_handles",{edit_checklist_id:edit_checklist_id},function(data){
				
				
			});
		}
		return;
});
//handle checklist 	
$('a').click(function() {
		
		var id = $(this).attr("id");
		if (id == "agree_checklist"){ 
			var checklist_agree_id = $(this).attr("data-listid");
			$(this).hide();
			$.get('/icare/checklist/agree_checklist/',{checklist_agree_id: checklist_agree_id}, function(data) {
				
				$('#checklist_agree_count'+checklist_agree_id).html(data);
			});
		}
		if (id =="thanks_checklist"){ 
			var checklist_thanks_id = $(this).attr("data-listid");
			$(this).hide();
			$.get('/icare/checklist/thanks_checklist/',{checklist_thanks_id: checklist_thanks_id} , function(data) {
				
				$('#checklist_thanks_count'+checklist_thanks_id).html(data);
			});
		}
		if (id == "add_checklist"){
			
			var checklist_add_id = $(this).attr("data-listid");
			$(this).hide();
			$.get('/icare/checklist/patient_add_checklist/',{checklist_add_id: checklist_add_id}, function(data){ 
				
				$('#checklist_uses_count'+checklist_add_id).html(data);
			});
		}
		return;
});

//handle thank and agree the answer 
$('a').click(function() {
		var id = $(this).attr("id");
		if (id == "answer_agree"){
			$(this).hide();
			var answer_agree_id = $(this).attr("data-answeragreeid");
			$.get('/icare/agree_answer',{answer_agree_id: answer_agree_id} , function(data) { 
				
				$("#answer_agree_count"+answer_agree_id).html(data);
			});
		}
		if (id == "answer_thanks"){ 
			$(this).hide();
			var answer_thanks_id = $(this).attr("data-answerthankid");
			
			$.get('/icare/thanks_answer/',{answer_thanks_id: answer_thanks_id}, function(data) { 
				
				$("#answer_thanks_count"+answer_thanks_id).html(data);
			});
		}
		return;
	});
	
//handle checklist and checklist item 
$('a').click(function(){
		
		var id = $(this).attr('id');
		
		if(id == "item_complete"){
			var item_id = $(this).attr("data-itemid");
			$(this).hide();
			$.get('/icare/user_checklist_item/complete/',{item_id:item_id},function(data) {
				$("#complete_item"+item_id).html(data);
				
			});
		}
		
		if(id=="delete_select_item"){
			var item_id = $(this).attr("data-itemid");
			alert(item_id);
			$.get('/icare/item/delete/',{item_id:item_id},function(){
				
				$("#item_delete"+item_id).remove();
			});
		}
		return;
});

$('span').click(function() {
	var id = $(this).attr('id');
	if(id == "checklist_delete"){
			$(this).hide();
			var checklist_id = $(this).attr("data-listid");
			$.get('/icare/patient_checklist/delete/',{user_checklist_id:checklist_id},function(data){ 
				
				$("#patient_checklist"+checklist_id).remove();
			});
		}
	
});
$('a').click(function(){
		
		var id = $(this).attr("data-newid");
		
		if(id == "private"){
			var item_id = $(this).attr("data-id");
			
			$.get('/icare/patient/question/private/',{question_id:item_id},function(data) {
				
				
			});
		}
		if(id == "public"){
			
			var checklist_id = $(this).attr("data-id");
			$.get('/icare/patient/question/public/',{question_id:checklist_id},function(data){ 
				
			});
		}
		
		return;
	});	
	
$("#question_post").submit(function(event){ 
		event.preventDefault();
		
		
		$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'html',
			success: function(response){
				$("#new_question").append(response);
				$("#question_post").remove();
			
			}
		});
	});
	


	
	$("#add_new_item").click(function(){ 
		var checklist_id = $(this).attr('data-checklistid');
		$.get('/icare/item/add/',{checklist_id:checklist_id},function(data){ 
			$("#new_item_form").html(data);
		});
	});
	
$(document.body).on('click','#topic_follow_button',function(){ 
	$("#topic_follow_button").hide();
		var topic_id = $(this).attr('data-topicid');
		$.get('/icare/user/topic/follow/',{topic_id:topic_id},function(data) { 
			$("#new_topic_count").html(data);
			$("#follow_button").html('<button type="button" class="btn btn-md btn-info" id="topic_unfollow_button" data-topicid="'+topic_id+'" >Followed</button>')
		});
});	
$(document.body).on('click','#topic_unfollow_button',function(){
	$("#topic_unfollow_button").hide();
		var topic_id = $(this).attr("data-topicid");
		$.get("/icare/user/topic/unfollow/",{topic_id:topic_id},function(data){ 
			$("#new_topic_count").html(data);
			$("#follow_button").html('<button type="button" class="btn btn-md btn-primary" id="topic_follow_button" data-topicid="'+topic_id+'" >Follow</button>')
		});
});

$(document).ready(function() { 
$('span.stars').stars();

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
