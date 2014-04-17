function convertFormToJSON(form){
    var array = jQuery(form).serializeArray();
    var json = {};
    
    jQuery.each(array, function() {
        json[this.name.split('-')[1]] = this.value || '';
    });
    
    return json;
}

function onClick_Cancel(obj_name){
	$('#' + obj_name + '_add_msg').remove();
	$("#configs_dialog_add").dialog("close");
	return false;
}

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