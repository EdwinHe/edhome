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

$('form.form-horizontal').submit(function () {
	var id = $(this).attr('id');
	var obj_name = id.replace('_add_form','');
	$('#' + obj_name + '_add_msg').remove();
	
    $.ajax({
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        data: convertFormToJSON($(this)),
        success: function (data) {
        	$("#configs_dialog_add").dialog("close");
        	refreshTable_caller(obj_name);
        },
        error: function(data) {
            var msg = "";
        	msg += '<div id="' + obj_name + '_add_msg" class="alert alert-dismissable alert-warning">';
        	msg += '<button type="button" class="close" data-dismiss="alert">×</button>';
        	
            var d = $.parseJSON(data.responseText);
            for (var k in d) {
            	msg += k + ': ' + d[k];
            	msg += '<br>'
            }
            msg += '</div>';
            $('#' + obj_name + '_add_form').prepend(msg);
        }
    });
    return false;
});