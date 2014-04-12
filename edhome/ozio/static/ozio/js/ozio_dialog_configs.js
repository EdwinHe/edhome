$(function() {
    $( "#configs_dialog" ).dialog({
      autoOpen: false,
      title: 'CONFIGURATIONS',
      dialogClass: 'ed-dialog-flatly',
      width: '90%',
      height: 600,
      modal: true,
      show: {
        duration: 300
      },
    });
 
    $( "#configurations" ).click(function() {
        $( "#configs_dialog" ).dialog( "open" );
      });
  });
