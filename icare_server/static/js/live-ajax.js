
$('span').css( 'cursor', 'pointer' );




$('#add_patient_allergy').click(function() {
	$("#add_patient_allergy").hide();
	var patient_id = $(this).attr("data-id");
	$.get('/icare/patient/add_allergy/',{patient_id:patient_id},function(data) { 
		$("#new_patient_allergy").html(data);
		
	});
});

$('#add_patient_condition').click(function() {
	$("#add_patient_allergy").hide();
	var patient_id = $(this).attr("data-id");
	$.get('/icare/patient/add_condition/',{patient_id:patient_id},function(data) { 
		$("#new_patient_condition").html(data);
		
	});
});

$('#add_patient_medication').click(function() {
	$("#add_patient_medication").hide();
	var patient_id = $(this).attr("data-id");
	$.get('/icare/patient/add_medication/',{patient_id:patient_id},function(data) { 
		$("#new_patient_medication").html(data);
		
	});
});

$('#add_patient_family').click(function() {
	
	$("#add_patient_family").hide();
	var patient_id = $(this).attr("data-id");
	$.get('/icare/patient/add_family/',{patient_id:patient_id},function(data) { 
		$("#new_patient_family").html(data);
		
	});
});
//add live edit patient profile 
$(document.body).on('click','span',function() { 
	var id = $(this).attr("id");
	//patient edit allergy 
	if (id=="patient_allergy_edit"){
		var patient_allergy_id = $(this).attr("data-id");
		$.get('/icare/patient/edit_allergy/',{patient_allergy_id:patient_allergy_id},function(data){ 
			$("#new_patient_allergy").html(data);
		});
	}
	
	if (id =="patient_medication_edit"){ 
		
		var patient_medication_id = $(this).attr("data-id");
		$.get('/icare/patient/edit_medication',{patient_medication_id:patient_medication_id},function(data){
			$("#new_patient_medication").html(data);
		});
	}
	
	if (id == "patient_family_edit"){
		var patient_family_id = $(this).attr("data-id");
		$.get('/icare/patient/edit_family/',{patient_family_id:patient_family_id},function(data) {
			$("#new_patient_family").html(data);
		});
	}
	
	if (id == "patient_condition_edit"){
		
		var patient_condition_id = $(this).attr("data-id");
		
		$.get('/icare/patient/edit_condition/',{patient_condition_id:patient_condition_id} , function(data) {
			
			$("#new_patient_condition").html(data);
		});
	}
	return; 
});
//submit weight patient 
$(document.body).on('submit','#patient_weight_submit', function(event) {
	
	event.preventDefault();
	$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'html',
			success: function(response){
				$("#weight").html(response);
				$("#weight_edit").empty();
				$("#weight_update").show();
			}
		});
	
});

//submit allergy patient 
$(document.body).on('submit','#patient_allergy_submit',function(event) {
	event.preventDefault();
	$.ajax({
		data:$(this).serialize(),
		type:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType: 'html',
		success: function(response){
			$("#main_allergy").html(response);
			$("#new_patient_allergy").empty();
			$("#add_patient_allergy").show();
		}
	});
});
// submit allergy edit 

$(document.body).on('submit','#patient_allergy_submit_edit',function(event) {
	event.preventDefault();
	$.ajax({
		data:$(this).serialize(),
		type:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType: 'html',
		success: function(response){
			$("#main_allergy").html(response);
			$("#new_patient_allergy").empty();
			
		}
	});
});

//submit condition patient 
$(document.body).on('submit','#patient_condition_submit',function(event) {
	event.preventDefault();
	$.ajax({
		data:$(this).serialize(),
		type:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType: 'html',
		success: function(response){
			$("#main_condition").html(response);
			$("#new_patient_condition").empty();
			$("#add_patient_condition").show();
		}
	});
});
//submit condition edit 
$(document.body).on('submit','#patient_condition_submit_edit',function(event) {
	event.preventDefault();
	$.ajax({
		data:$(this).serialize(),
		type:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType: 'html',
		success: function(response){
			$("#main_condition").html(response);
			$("#new_patient_condition").empty();
			
		}
	});
});

//submit medication patient 
$(document.body).on('submit','#patient_medication_submit',function(event) {
	event.preventDefault();
	$.ajax({
		data:$(this).serialize(),
		type:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType: 'html',
		success: function(response){
			$("#main_medication").html(response);
			$("#new_patient_medication").empty();
			$("#add_patient_medication").show();
		}
	});
});
//submit medication edit 
$(document.body).on('submit','#patient_medication_submit_edit',function(event) {
	event.preventDefault();
	$.ajax({
		data:$(this).serialize(),
		type:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType: 'html',
		success: function(response){
			$("#main_medication").html(response);
			$("#new_patient_medication").empty();
			
		}
	});
});


//submit family history patient 

$(document.body).on('submit','#patient_family_submit',function(event) {
	
	event.preventDefault();
	$.ajax({
		data:$(this).serialize(),
		type:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType: 'html',
		success: function(response){
			$("#main_family").html(response);
			$("#new_patient_family").empty();
			$("#add_patient_family").show();
		}
	});
});
//submit family edit 

$(document.body).on('submit','#patient_family_submit_edit',function(event) {
	event.preventDefault();
	$.ajax({
		data:$(this).serialize(),
		type:$(this).attr('method'),
		dataType: 'html',
		success: function(response){
			$("#main_family").html(response);
			$("#new_patient_family").empty();
			
		}
	});
});

//submit height patient 
$(document.body).on('submit','#patient_height_submit', function(event) {
	event.preventDefault();
	$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'html',
			success: function(response){
				$("#height").html(response);
				//alert("submitted");
				$("#height_edit").empty();
				$("#height_update").show();
			}
		});
	
});

//submit ethnicity
$(document.body).on('submit','#patient_ethnicity_submit', function(event) {
	event.preventDefault();
	
	$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'html',
			success: function(response){
				$("#ethnicity").html(response);
				//alert("ethnicity");
				$("#ethnicity_edit").empty();
				$("#ethnicity_update").show();
			}
		});
	
});

//edit vaccination 
$(document.body).on('submit','#patient_vaccination_submit', function(event) {
	event.preventDefault();
	
	$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'html',
			success: function(response){
				$("#vaccination").html(response);
				//alert("ethnicity");
				$("#vaccination_edit").empty();
				$("#vaccination_update").show();
			}
		});
	
});
//dietary_restriction 
$(document.body).on('submit','#dietary_submit', function(event) {
	event.preventDefault();
	
	$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'html',
			success: function(response){
				$("#dietary_restriction").html(response);
				//alert("ethnicity");
				$("#dietary_restriction_edit").empty();
				$("#dietary_restriction_update").show();
			}
		});
	
});

//alcohol 
$(document.body).on('submit','#alcohol_submit', function(event) {
	event.preventDefault();
	
	$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'html',
			success: function(response){
				$("#alcohol").html(response);
				//alert("alcohol");
				$("#alcohol_edit").empty();
				$("#alcohol_update").show();
			}
		});
	
});

//tobacco 
$(document.body).on('submit','#tobacco_submit', function(event) {
	event.preventDefault();
	
	$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'html',
			success: function(response){
				$("#tobacco").html(response);
				//alert("ethnicity");
				$("#tobacco_edit").empty();
				$("#tobacco_update").show();
			}
		});
	
});

//sexually_active
$(document.body).on('submit','#sex_submit', function(event) {
	event.preventDefault();
	
	$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'html',
			success: function(response){
				$("#sex").html(response);
				//alert("ethnicity");
				$("#sex_edit").empty();
				$("#sex_update").show();
			}
		});
	
});

//recreational drug
$(document.body).on('submit','#recreational_drug_submit', function(event) {
	event.preventDefault();
	
	$.ajax({ 
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'html',
			success: function(response){
				$("#recreational_drug").html(response);
				//alert("ethnicity");
				$("#recreational_drug_edit").empty();
				$("#recreational_drug_update").show();
			}
		});
	
});

//handle save item checklist 
$(document.body).on('submit','#new_item_submit',function(event){
	event.preventDefault();
	$.ajax({ 
		data:$(this).serialize(),
		type:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType: 'html',
		success: function(response){
			$("#new_item_submit").remove();
			$("#item_save_alert").append(response);
				
		}
	});
	
});
