var moduly;
$(document).ready(function () {

     $(document).ajaxStart(function() {
      working = true;
    });

    $(document).ajaxStop(function() {
      
      //query dla wszystkich urzadzen ,ktore urzadzenie wybrano - po id urzadzenia
      for(let i = 0; i < moduly.length; i++){
         var iloscUrzadzen = Object.size(moduly[i].urzadzenia);
         let modul = moduly[i];
         for(let j = 0; j < iloscUrzadzen; j++ ){
               //Przypisanie urzadzenia do zmiennej
               
               let urzadzenie = moduly[i].urzadzenia[j];
               
            
               $('#urzadzenie'+urzadzenie.id).bind('click', function(event){
               //Wyswietlenie nazwy wybranego urzadzenia i modulu
                  $('#sceny').append('<div class="bloczek"><h3>'+modul.name+'</h3><h4>'+urzadzenie.name+'</h4></div>');
                  //Wybranie i wyswietlenie urzadzenia wedlug sterowania
                  if(urzadzenie.sterowanie == '0-100%'){
                     
                     $('.bloczek').append('<input type="range" id="bar'+urzadzenie.id+'" min="0" max="100" step="1" value="0">');
                     $('.bloczek').append('<p id="costam">0%</p>');
                     $('#urzadzenie'+urzadzenie.id).attr('hidden',true);
                     
                     $('#bar'+urzadzenie.id).bind('click', function(event){  
                     var value = $(this).val();
                  
                     $('#costam').empty();
                     $('#costam').append(value+'%');
                     value = parseInt(value);
                     //var json = {rejestr: rejestr, modul_id: modul_id, wartosc: value};
                     //ajaxPost(json);
                        
                     });
                     
                     
                                        };
                  if(urzadzenie.sterowanie != 'tylko do odczytu'){};
                  if (urzadzenie.sterowanie == 'RGB'){};
                  if (urzadzenie.sterowanie == 'on/off'){};
                  //Submit button - AJAX POST do /sceny
               });
         }
      }
      
      working = false;
    });


    //$('.btn-lg').click(function(){
    //    $("#myDropdown").toggleClass("show");
    //});

    getModuly();
    
    
    //$('#').click(function(){
    //    $("#myDropdown").toggleClass("show")
    //});
    
    //


});
function getModuly() {
    
    $.ajax('/moduly',
            {
            method: 'GET',
            dataType: 'json',
            success: function(data){ moduly = data.moduly;}
            }
        );
}

function urzadzenieBlock(idModul,idUrzadzenie){
   
   
   
   //Przypisanie urzadzenia do zmiennej
   modul = moduly[idModul];
   urzadzenie = moduly[idModul].urzadzenia[idUrzadzenie];
   

   $('#'+urzadzenie.id).bind('click', function(event){
   //Wyswietlenie nazwy wybranego urzadzenia i modulu
      $('#sceny').append('<h2>'+modul.name+'</h2><br><h3>'+urzadzenie.name+'</h3>');
      //Wybranie i wyswietlenie urzadzenia wedlug sterowania
      if(urzadzenie.sterowanie == '0-100%'){};
      if(urzadzenie.sterowanie != 'tylko do odczytu'){};
      if (urzadzenie.sterowanie == 'RGB'){};
      if (urzadzenie.sterowanie == 'on/off'){};
      //Submit button - AJAX POST do /sceny
   });
}



function ajaxPost(json){
   
   if($.active > 0){ 
      getrequest.abort();
   }
   
   $.ajax(
         "/sceny",
         {
           method: "POST",
           contentType: "application/json",
           data: JSON.stringify(json),
           success: function () {}
           });
      
};

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};