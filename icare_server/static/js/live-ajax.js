

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
			$("#new_item_submit").empty();
			$("#item_save_alert").html(response);
				
		}
	});
	
});

