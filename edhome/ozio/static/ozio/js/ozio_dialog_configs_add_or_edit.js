function bind_submit_event(url, tbody_element_id) {
	var form = $('#id_form_add_or_edit');
	form.submit(function () {
		$.ajax({
			type: form.attr('method'),
		    url: form.attr('action'),
		    data: convertFormToJSON(form),
		    success: function(rendered_form_html) {
		    	// rendered_form_html == '' means submition is successful. 
		    	// check view.ozio_add_or_edit()
		    	if (rendered_form_html == '') {
		    		$('#id_div_configs_dialog_add_edit').dialog('close');
		    		var obj_name = form.attr('action').split('/')[3];
		    		refreshTableContent_caller(url, obj_name, 'tbody#' + tbody_element_id);
		    		return false;
		    	}
		    	
		    	// rendered_form_html != '' means either submitted form is invalid 
		    	// or it is a new edit request. 
		    	$('#id_div_configs_dialog_add_edit').empty();
				$('#id_div_configs_dialog_add_edit').append(rendered_form_html);
				bind_submit_event(url, tbody_element_id);
		    }
		 });
		
		return false;
	});
}

function on_AddOrEdit_Click_Cancel(){
	$('#id_div_configs_dialog_add_edit').dialog("close");
	return false;
}


$( "#id_div_configs_dialog_add_edit" ).dialog({
	autoOpen: false,
	title: 'ADD/EDIT',
	dialogClass: 'ed-dialog-flatly',
	width: 'auto',
	height: 'auto',
	modal: true,
	show: {
		duration: 300
	},
});