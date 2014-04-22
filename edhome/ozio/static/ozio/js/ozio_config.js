// Function to Build Tabs and Table Header
function buildHeader(objs, obj_name){
	
	var li_class = '';
	var div_class = ' class="tab-pane fade"';
	if ( active_tab == obj_name.toLowerCase() ) {
		li_class = ' class="active"';
		div_class = ' class="tab-pane fade active in"';
	}
		
	// ============= Set Tabs ============= 
	var rest_obj_name = objs.name.replace(" List","");
	
	//Add list item: <li class="active"><a href="#type" data-toggle="tab">Types</a></li>
	$('ul#config_tabs').append('<li' + li_class + ' id="' + obj_name.toLowerCase() + '_tab"><a href="#' + obj_name.toLowerCase() + 
			'" data-toggle="tab">' + rest_obj_name + '</a></li>');
	
	// Add <div class="tab-pane fade active in" id="type">
	// id should be the same as href above
	var tab_content = '';
	tab_content += '<div' + div_class + ' id="' + obj_name.toLowerCase() + '">';
	tab_content += '<div>';
	tab_content += '<button type="button" class="btn btn-danger pull-right" \
					 onclick="on_Config_Click_Add(\''+ obj_name + '\')" \
					>ADD ' + obj_name.toUpperCase() + '</button>'; // Add button
	tab_content += '</div>';
	tab_content += '<div>';
	tab_content += '<table class="table table-striped table-hover">';
	tab_content += '<thead>';
	tab_content += '<tr class="success">';
	
	// ============= Set Table Header ==============
	$.each( objs.actions.POST, 
		function( key, value ) {
			// Add <th>COLUMN_NAME</th>
			tab_content += '<th>' + value.label + '</th>';
		}
	);
	// === Add two more columns for delete and change ===
	tab_content += '<th></th>';
	tab_content += '<th></th>';
	
	tab_content += '</tr>';
	tab_content += '</thead>';
	tab_content += '<tbody id="' + obj_name.toLowerCase() + '">';
	tab_content += '</tbody>';
	tab_content += '</table>';
	tab_content += '</div>';
	tab_content += '</div>';
	
	$('div#config_tabs_content').append(tab_content);

}

// ------- Function to Build Table Content ------- 
function refreshTable(objs, obj_name){
	
	var tab_records = '';
	
	// Clear up the table body 
	$('tbody#' + obj_name).empty();
	
	// Below code build this structure
	//<tr> <td>COL1</td> <td>COL2</td> <td>COL3</td> </tr>
	$.each( objs, 
		function( obj_id, obj ) {
			tab_records += '<tr>';
			$.each( obj, function(attr, value) {
				if ( $.type( value) == 'object' )
					tab_records += '<td>' + value.text + '</td>';
				else
					tab_records += '<td>' + value + '</td>';
			} );
			// === Add buttons for delete and modify ===
			tab_records += '<td><a href="#" class="deletelink" \
								 onclick="on_Config_Click_Delete(\''+ obj_name + '\', ' + obj.id + ')"> \
								 </a></td>'
			tab_records += '<td><a href="#" class="changelink" \
				 				 onclick="on_Config_Click_Change(\''+ obj_name + '\', ' + obj.id + ')"> \
				 				 </a></td>'
			tab_records += '</tr>';
		}
	);
	
	$('tbody#' + obj_name).append(tab_records);

}
// -------------------------------------------------


//------- On Click Handlers ----------------------- 
function on_Config_Click_Delete(obj_type, obj_id) {	
	$.ajax(
			{	type: "DELETE", 
				async: false, 
				url: "/API/" + obj_type + "/" + obj_id + "/", 
			}
		);
	refreshTable_caller(obj_type);
}

function on_Config_Click_Change(obj_type, obj_id) {
	$.ajax(
			{	type: "GET", 
				async: false, 
				url: "/ozio/add_or_edit/" + obj_type + "/" + obj_id + "/",
				success: function(rendered_form_html) {
					$('#configs_dialog_add_edit').empty();
					$('#configs_dialog_add_edit').append(rendered_form_html);
					$('#configs_dialog_add_edit').dialog("open");
					bind_submit_event();
				},
			}
	);
}

function on_Config_Click_Add(obj_type) {
	$.ajax(
			{	type: "GET", 
				async: false, 
				url: "/ozio/add_or_edit/" + obj_type + "/-1/", //Set id to -1 means Add new, see view.py
				success: function(rendered_form_html) {
					$('#configs_dialog_add_edit').empty();
					$('#configs_dialog_add_edit').append(rendered_form_html);
					$('#configs_dialog_add_edit').dialog("open");
					bind_submit_event();
				},
			}
	);
}

function on_Click_Add(obj_type) {
	$('form.form-horizontal').css("display", "none");
	$("#" + obj_type + "_add_form").css("display", "block");
	$("#configs_dialog_add").dialog( "open" );
}
//-------------------------------------------------


// ------- Two callers -------------------------------------------- 
// Created for one reason: Passing obj_name into buildHeader and refreshTable
function buildHead_caller(obj_name) {
	$.ajax(
		{	type: "OPTIONS", 
			async: false, 
			url: "/API/" + obj_name + "/", 
			success: function(objs) {
				buildHeader(objs, obj_name)
			}
		}
	);
}

function refreshTable_caller(obj_name) {
	$.ajax(
		{	type: "GET", 
			async: false, 
			url: "/API/" + obj_name + "/", 
			success: function(objs) {
				refreshTable(objs, obj_name)
			}
		}
	);
}
//----------------------------------------------------------------------

//--- Set add dialog properties ---
$( "#configs_dialog_add" ).dialog({
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


// Objects to show in configuration dialog
var objects=["type", "cate", "subcate", "keyword", "sourcefile", 
             "transaction", "transaction_filter", "filter_sql"];
//var objects=["subcate"];

// Clear up HTML object id='config_tabs' and id='config_tabs_content'
// in ozio_dialog_configs.html
$('ul#config_tabs').empty();
$('div#config_tabs_content').empty();

// For each object, build tab and the table
for (var iter = 0; iter < objects.length; iter++) {	
	buildHead_caller(objects[iter]);
	refreshTable_caller(objects[iter]);
}

if ( open_dialog_name != "" )
	onClick_Add(open_dialog_name);

