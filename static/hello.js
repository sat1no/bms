
$(document).ready(function () {
   
//  
//load the content initially
//
   working = false;
    $(document).ajaxStart(function(r, s) {
        $("#contentLoading").show();
         $("#contentLoading2").hide();
        $("#ready").hide();
        working = true;
    });

    $(document).ajaxStop(function(r, s) {
        $("#contentLoading").hide();
         $("#contentLoading2").hide();
        $("#ready").show();
        working = false;
    });

    //$('#form').submit(function() {
    //    if (working) return;
    //    $.post('/some/url', $(this).serialize(), function(data){
    //        alert(data);
    //    });
    //});

   update_task_table();


//
//TWORZENIE EVENTU DLA KAZDEGO PRZYCISKU DODOWANIA URZADZEN
//
   
   for(let i = 0; i < $('#liczba_modulow').val(); i++){
      

      $('#dodaj'+(i+1)).click(function (event){
        
         //UKRYWANIE POL FORMULARZA
         $('#nazwa'+(i+1)).toggle();
         $('#rejestr'+(i+1)).toggle();
         $('#submit'+(i+1)).toggle();
         $('#sterowanie'+(i+1)).toggle();
      });
   }


//
//FORMULARZ DODAWANIA URZADZEN
//
         
   for(let i = 0; i < $('#liczba_modulow').val(); i++){
      
      
      $('#post'+(i+1)).submit(function (event) {
         
         //check valid
         
         $('input#nazwa'+(i+1)).toggle();
         $('input#rejestr'+(i+1)).toggle();
         $('input#submit'+(i+1)).toggle();
         $('#sterowanie'+(i+1)).toggle();
         let nazwa = $("input#nazwa"+(i+1)).val();
         let rejestr = $("input#rejestr"+(i+1)).val();
         let id_modul = $("input#id_modul"+(i+1)).val();
         let sterowanie = $("#sterowanie"+(i+1)).val();
      
         event.preventDefault();
         let json = {nazwa: nazwa, rejestr:rejestr, id_modul:id_modul, sterowanie:sterowanie}
         ajaxPost(json);
         //insert new element in db
         //$.ajax("/moduly",
         //       {
         //         method: "POST",
         //         contentType: 'application/json',
         //         data: JSON.stringify(json),
         //         
         //         success: function(data,status) {
         //            alert(status);
         //            clear_text();
         //
         //         }
         //         
         //       });
      });
   }
});     
      
   
   
   
   
//   
//FUNKCJE   
//

function update_task_table() {
   
   //get json with list of elements from server


 
   getrequest = $.ajax(
     '/moduly',
     {
         method: "GET",
         dataType: "json",
         success: function(data, status) {
            //alert(data.nowe[0].name);
            //alert(status);
            clear_text();
            var moduly = data.moduly;

            for(var i = 0;i<moduly.length;i++){
               //for(var i = 0; i<moduly[i].urzadzenia.length;i++){
               // Get the size of an object
               var iloscUrzadzen = Object.size(moduly[i].urzadzenia);
               var modul_id = moduly[i].id;
               for(var j = 0;j<iloscUrzadzen;j++){
                  
                  var urzadzenia = moduly[i].urzadzenia[j];
                  $('p#text'+(i+1)).append(urzadzenia.name+'<br>');
                  $("#contentLoading").hide();
                  $("#ready").hide();
                  $("#contentLoading2").show();
                  if(urzadzenia.sterowanie != 'tylko do odczytu')$('p#text'+(i+1)).append('<a><div id="onoff'+modul_id+urzadzenia.id+'" class="on_off"></div></a>');
                  else{valueChange(modul_id,urzadzenia.wartosc)}
                  RGB(urzadzenia.sterowanie,modul_id,urzadzenia.rejestr,urzadzenia.r,urzadzenia.g,urzadzenia.b);
                  if(urzadzenia.sterowanie == '0-100%') sliderChange('#bar'+modul_id+urzadzenia.id,urzadzenia.rejestr,modul_id,urzadzenia.id,urzadzenia.wartosc);

                  
                  

                  $('p#text'+(i+1)).append('<br><br>');
                  togClasses('#onoff'+modul_id+urzadzenia.id,'on_off','on_off2', urzadzenia.rejestr, modul_id);
                  if (urzadzenia.stan > 0){
                     
                     $('#onoff'+modul_id+urzadzenia.id).toggleClass('on_off');
                     $('#onoff'+modul_id+urzadzenia.id).toggleClass('on_off2');
                  }
                  
               }                  
                  
               }



            },
            complete: function (){
              
              
              setTimeout(update_task_table, 1500);
            return false;
            }
         
     });

   
   
}
function valueChange(modul_id,wartosc){
   
   if (wartosc == null) nowaWartosc = 0;
   $('p#text'+modul_id).append('<p class="slider"><h3 class="h3">'+nowaWartosc+'</h3></p>')
   
}


function clear_text() {
   
   $('p.card-text').empty()
   var list = document.getElementsByClassName("colorpicker");
   for (var i = 0; i < list.length-4; i++) {
    list[i].outerHTML = "";
    delete list[i];
   }

   
}



function togClasses(id,class1,class2,rejestr,modul_id){
   
   
   $(id).bind('click', function(event){
      $(id).toggleClass(class1);
      
      $(id).toggleClass(class2);
      
      var json = {modul_id: modul_id, rejestr: rejestr};
      var className = $(id).attr("class");
      if( className == 'on_off') json['stan'] = 0;
      else json['stan'] = 1;

   
      ajaxPost(json);
      

   }); 
}
function sliderChange(id,rejestr,modul_id,urzadzenia_id,urzadzenia_wartosc){
   


      $('p#text'+modul_id).append('<p class="slider"><input type="range" id="bar'+modul_id+urzadzenia_id+'" min="0" max="100" step="1" value="'+urzadzenia_wartosc+'"></p>');
      $('p#text'+modul_id).append('<div class="costam slider">'+urzadzenia_wartosc+'%</div>');

   $(id).bind('click', function(event){  
      var value = $(this).val();

      $('.costam').empty();
      $('.costam').append(value+'%')
      value = parseInt(value)
      var json = {rejestr: rejestr, modul_id: modul_id, wartosc: value}
      ajaxPost(json);
      
      });
}

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};
var ileUrzadzen = 0;

function RGB(sterowanie,modul_id,rejestr,r,g,b){
   
   
   
   if (sterowanie == 'RGB'){
      ileUrzadzen++;
      if(r === null || g === null || b === null){
         r=0;
         g=0;
         b=0;
         }
         
      $('p#text'+modul_id).append('<div id="colorSelector" class="rgb'+modul_id+'"><div class="rgbi'+modul_id+'"style="background-color: rgb('+r+','+g+','+b+')" ></div></div>');
       
   
      if (true){
         $('.rgb'+modul_id).ColorPicker({
         color: {r: r, g: g,b: b},
         onShow: function (colpkr) {
            $(colpkr).fadeIn(500);
               if($.active > 0){ 
               getrequest.abort();
            }
         
            return false;
         },
         onHide: function (colpkr) {
            $(colpkr).fadeOut(500);
            if($.active > 0){ 
               getrequest.abort();
            }
            return false;
         },
         onChange: function (hsb, hex, rgb) {
            $('.rgbi'+modul_id).css('backgroundColor', '#' + hex);
            if($.active > 0){ 
               getrequest.abort();
            }
            return false;
         },
         
         onSubmit: function (hsb, hex, rgb) {
         
         
            var json = {r: rgb.r, g: rgb.g, b: rgb.b, modul_id: modul_id, rejestr: rejestr};
               
            ajaxPost(json);
            return false;
         
         }
         
         });} 
      
}
}
function ajaxPost(json){
   
   if($.active > 0){ 
      getrequest.abort();
   }
   
   $.ajax(
         "/moduly",
         {
           method: "POST",
           contentType: "application/json",
           data: JSON.stringify(json),
           success: function () {}
           });
      
}
