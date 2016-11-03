var Monitor = (function(){
    var id = ID;

    function render(){
      var texto = "";
      $.getJSON($SCRIPT_ROOT + '/_all_turn/'+ id, function(datos){
        $.each(datos.settings, function(i, settings){
          texto += "<tr class='tb-head'>";
          texto += "<th class='black-green' id='/column_turn/' >" + settings.column_turn + "</th>";
          texto += "<th class='black-green' id='/column_custname/' >" + settings.column_custname + "</th>";
          texto += "<th class='black-green' id='/column_type/' >" + settings.column_type + "</th>";
          texto += "</tr>";
        });
        $.each(datos.allTurn, function(i, allTurn){
          texto += "<tr class='tb-text' data-id='" + allTurn.table_id + "' data-user='" + allTurn.user_id + "' >";
          texto += "<td class='text-center' >" + allTurn.number + "</td>";
          texto += "<td class='text-center' >" + allTurn.cust_name + "</td>";
          texto += "<td class='text-center'' >" + allTurn.request_type + "</td>";
          texto += "</tr>";
        });
        $("#turnos").html(texto);
      });
    }

    function updateRow(row){
      var rute = '/_update_status/' + row.attr('data-id') + '/' + row.attr('data-user');
      $.ajax({
        url: $SCRIPT_ROOT + '/_update_status/' + row.attr('data-id') + '/' + row.attr('data-user'),
        type: 'PUT',
        success: function(response) {
          console.log('puto el que lee');
        }
      });
    } 

    function cleanAll(){
      $.ajax({
        url: $SCRIPT_ROOT + '/_clean_all/' + id,
        type: 'PUT',
        success: function(response) {
          console.log('puto el que lee');
        }
      });
    }

    function changeRowHeader(column){
      var person = prompt("Ingrese Nombre de Columna", "");  
      if (person != null) {
        $.ajax({
          url: $SCRIPT_ROOT + '/_change_settings/' + id + column.attr('id') + person,
          type: 'PUT',
          success: function(response) {
            console.log('puto el que lee');
          }
        });
      }
    }

    var object = {
      render: render,
      updateRow: updateRow,
      cleanAll: cleanAll,
      changeRowHeader: changeRowHeader
    }

    return object;
  }
  )();

$(document).ready(function(){
    $('.bxslider').bxSlider({auto:true});

    setInterval(function(){
            Monitor.render();
          }, 1000);

    $('#turnos').on('click', 'th', function(){
        Monitor.changeRowHeader($(this));
      });
  
    $('#turnos').on('click', '.tb-text', function(){
      Monitor.updateRow($(this));
    });
});
