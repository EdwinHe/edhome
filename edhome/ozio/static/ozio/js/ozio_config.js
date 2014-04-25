// Function to Build Tabs and Table Header
function buildTabs(obj_name, obj_display_name){
	
	var li_class = '';
	var div_class = ' class="tab-pane fade"';
	if ( obj_name == 'type' ) {
		li_class = ' class="active"';
		div_class = ' class="tab-pane fade active in"';
	}
		
	// ============= Build Tabs ============= 
	
	//Add list item: <li class="active"><a href="#type" data-toggle="tab">Types</a></li>
	$('ul#config_tabs').append('<li' + li_class + ' id="' + obj_name + '_tab"><a href="#' + obj_name + 
			'" data-toggle="tab">' + obj_display_name + '</a></li>');
	
	// Add <div class="tab-pane fade active in" id="type">
	// id should be the same as href above
	var tab_content = '';
	tab_content += '<div' + div_class + ' id="' + obj_name + '">';
	tab_content += '<div>';
	tab_content += '<table class="table table-striped table-hover">';
	// Build Empty Table Header
	tab_content += '<thead id="' + obj_name + '">';
	tab_content += '</thead>';
	// Build Empty Table Body
	tab_content += '<tbody id="' + obj_name + '">';
	tab_content += '</tbody>';
	tab_content += '</table>';
	tab_content += '</div>';
	tab_content += '</div>';
	
	$('div#id_div_config_tabs_content').append(tab_content);

}


function on_Config_Click_Add() {
	var obj_name = $('#config_tabs li.active a').attr('href').split('#')[1];
	var obj_display_name = $('#config_tabs li.active a').text();
	
	$('#id_div_configs_dialog_add_edit').dialog('option', 'title', 'Add ' + obj_display_name);
	
	$.ajax(
			{	type: "GET", 
				async: false, 
				url: "/ozio/add_or_edit/" + obj_name + "/-1/", //Set id to -1 means Add new, see view.py
				success: function(rendered_form_html) {
					$('#id_div_configs_dialog_add_edit').empty();
					$('#id_div_configs_dialog_add_edit').append(rendered_form_html);
					$('#id_div_configs_dialog_add_edit').dialog("open");
					bind_submit_event('/API/'+obj_name+'/', obj_name);
				},
			}
	);
}



//--- Set add dialog properties ---
$( "#id_div_configs_dialog_add" ).dialog({
	autoOpen: false,
	title: 'ADD',
	dialogClass: 'ed-dialog-flatly',
	width: 'auto',
	height: 'auto',
	modal: true,
	show: {
		duration: 300
	},
});

///////////////////////////////////////////////////////////
// RUN THESE CODE ONLY WHEN IT IS ON CONFIG PAGE
///////////////////////////////////////////////////////////
if ( $('#id_div_page_ozio_config').length == 1 ) {
	// Objects to show in configuration dialog
	var objects=[['type','Type'], ['cate','Category'], ['subcate','Sub Category'], 
	             ['keyword','Keyword'], ['sourcefile','Source File'], 
	             ['transaction','Transaction'], ['transactionfilter', 'Transaction Filter'], ['filtersql','Filter SQL']
	];
	
	// Clear up HTML object id='config_tabs' and id='id_div_config_tabs_content'
	// in ozio_dialog_configs.html
	$('ul#config_tabs').empty();
	$('div#id_div_config_tabs_content').empty();
	
	// For each object, build tab and the table
	for (var iter = 0; iter < objects.length; iter++) {	
		obj_name = objects[iter][0];
		obj_display_name = objects[iter][1];
		
		buildTabs(obj_name,obj_display_name);
		buildTableHead_caller(obj_name, 'thead#' + obj_name); //ozio_utils.js
		refreshTableContent_caller("/API/" + obj_name + "/", obj_name, 'tbody#' + obj_name); //ozio_utils.js
		/*
		hide_table_columns('thead#' + obj_name, 
						   'tbody#' + obj_name, 
						   json_exclude_cols['#'+obj_name]
		);*/
	}
}

