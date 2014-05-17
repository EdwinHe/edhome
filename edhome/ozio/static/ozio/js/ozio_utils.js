$.fn.assertSize = function(size) { 
	if (this.length != size) { 
		alert("Assertion Failed: Expected " + size + " elements, but got " + this.length + ".");
	}
	return this;
};

$.fn.assertExist = function(caller) { 
	if (this.length == 0) { 
		//alert("Assertion Failed:" + caller + ": Element Not Exist!");
		console.log("Assertion Failed:" + caller + ": Element Not Exist!");
	}
	return this;
};

function convertFormToJSON(form){
    var array = $(form).serializeArray();
    var json = {};
    
    for (i in array) {
        json[array[i].name] = array[i].value || '';
    }
    return json;
}

function obj_fade_out(html_obj_id) {
	$(html_obj_id).assertExist('obj_fade_out').delay(3000).fadeOut();
}

function display_msg(msg_id, msg) {
	$(msg_id).css("display", "block");
	$(msg_id).empty();
	$(msg_id).append("<p>" + msg + "</p>");
	obj_fade_out(msg_id);
}

function delete_obj_by_id(obj_name, obj_id) {
	msg = ''
		
	$.ajax(
			{	type: "GET", 
				async: false, 
				url: "/ozio/on_object_delete/" + obj_name + "/" + obj_id + "/", 
				success: function(objs) {
					msg += objs
				},
				error: function(objs) {
					msg += objs
					return msg
				} 
			}
		);

	
	$.ajax(
			{	type: "DELETE", 
				async: false, 
				url: "/API/" + obj_name + "/" + obj_id + "/", 
				error: function(objs) {
					msg += 'Failed to delete ' + obj_name + '(id=' + obj_id + '): ' + objs.responseJSON.detail
				} 
			}
		);
	return msg
}

function hide_table_columns(thead_element_id, tbody_element_id, hide_col_array) {
	
	//Assertion
	$(thead_element_id).assertExist('hide_table_columns');
	$(tbody_element_id).assertExist('hide_table_columns');
	
	// Hide Columns in hide_col_array, Show the others
	cols = $(thead_element_id + ' tr th');
	
	for (var i=0; i< cols.length; i++) {
		if ( $.inArray(cols[i].id, hide_col_array) != -1 ){
			$(thead_element_id + ' tr th:nth-child(' + (i+1) + ')').hide();
			$(tbody_element_id + ' tr td:nth-child(' + (i+1) + ')').hide();
		} else {
			$(thead_element_id + ' tr th:nth-child(' + (i+1) + ')').show();
			$(tbody_element_id + ' tr td:nth-child(' + (i+1) + ')').show();
		}
	}
}

//------- Two callers -------------------------------------------- 
//Created for one reason: Passing obj_name into buildHeader and refreshTable
function buildTableHead_caller(obj_name, thead_element_id) {
	
	$(thead_element_id).assertExist('buildTableHead_caller');
	
	$.ajax(
		{	type: "OPTIONS", 
			async: false, 
			url: "/API/" + obj_name + "/", 
			success: function(objs) {
				buildTableHeader(objs, obj_name, thead_element_id)
			}
		}
	);
}

function refreshTableContent_caller(url, obj_name, tbody_element_id) {
	
	$(tbody_element_id).assertExist('refreshTableContent_caller');
	
	// Save URL to tbody's value, this will be used when tbody needs to be refreshed
	$(tbody_element_id).val(url);
	
	$.ajax(
		{	type: "GET", 
			async: false, 
			url: url, 
			success: function(objs) {
				refreshTableContent(objs, obj_name, tbody_element_id)
			}
		}
	);
}
//----------------------------------------------------------------------

//Function to Build Tabs and Table Header
function buildTableHeader(objs, obj_name, thead_element_id){
	
	$(thead_element_id).assertExist('buildTableHeader');
	
	$(thead_element_id).empty();
	table_header = '';
	table_header += '<tr class="success">';
	
	// ============= Set Table Header ==============
	for (key in objs.actions.POST) { 
		table_header += '<th id =' + key + '>' + objs.actions.POST[key].label + '</th>';
	}

	// === Add two more columns for delete and change ===
	table_header += '<th id="delete"></th>';
	table_header += '<th id="edit"></th>';
	
	table_header += '</tr>';
	
	$(thead_element_id).append(table_header);

}

//------- Function to Build Table Content ------- 
function refreshTableContent(objs, obj_name, tbody_element_id){
	
	$(tbody_element_id).assertExist('refreshTableContent');
	
	var table_content = '';
	
	// Clear up the table body 
	$(tbody_element_id).empty();
	
	// Below code build this structure
	// <tr> <td>COL1</td> <td>COL2</td> <td>COL3</td> </tr>
	
	// Loop through each record
	for (obj in objs) {
		table_content += '<tr>';
		// Loop through cols of a record
		for (key in objs[obj]) {
			table_content += '<td>' + objs[obj][key] + '</td>';
		}
		// === Add buttons for delete and modify ===
		table_content += '<td><a href="#" class="deletelink" \
							   id="' + obj_name + ',' + objs[obj].id + ',delete" \
							   onclick="on_delete_click(this)"> \
							   </a></td>'
		table_content += '<td><a href="#" class="changelink" \
							   id="' + obj_name + ',' + objs[obj].id + ',change" \
							   onclick="on_change_click(this)"> \
			 				   </a></td>'
		table_content += '</tr>';
	}
	
	$(tbody_element_id).append(table_content);
}
// -------------------------------------------------

function on_delete_click(caller) {
	obj_name = $(caller).attr('id').split(',')[0];
	obj_id = $(caller).attr('id').split(',')[1];
	tbody_element_id = $(caller).closest('tbody').attr('id');
	url = $(caller).closest('tbody').val();
	
	$( "#id_div_configs_dialog_confirm" ).assertExist('on_delete_click');
	
	$( "#id_div_configs_dialog_confirm" ).empty();
	$( "#id_div_configs_dialog_confirm" ).append("Are you sure you want to delete " + obj_name + ":" + obj_id + "?");
	$( "#id_div_configs_dialog_confirm" ).dialog({
		autoOpen: false,
		title: 'Are you sure?',
		dialogClass: 'ed-dialog-flatly',
		height:'auto',
		modal: true,
		buttons: {
			"Delete": function() {
				var msg = delete_obj_by_id(obj_name, obj_id);
				display_msg('#id_div_config_message', msg);
				refreshTableContent_caller(url, obj_name, 'tbody#' + tbody_element_id);
				$( this ).dialog( "close" );
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},
		show: {
			duration: 300
		},
	});
	$( "#id_div_configs_dialog_confirm" ).dialog('open');
}

function on_change_click(caller) {
	
	$( "#id_div_configs_dialog_confirm" ).assertExist('on_change_click');
	
	obj_name = $(caller).attr('id').split(',')[0];
	obj_id = $(caller).attr('id').split(',')[1];
	tbody_element_id = $(caller).closest('tbody').attr('id');
	url = $(caller).closest('tbody').val();
	
	$.ajax(
			{	type: "GET", 
				async: false, 
				url: "/ozio/add_or_edit/" + obj_name + "/" + obj_id + "/",
				success: function(rendered_form_html) {
					$('#id_div_configs_dialog_add_edit').empty();
					$('#id_div_configs_dialog_add_edit').append(rendered_form_html);
					$('#id_div_configs_dialog_add_edit').dialog("open");
					bind_submit_event(url, tbody_element_id);
				},
			}
	);
}

