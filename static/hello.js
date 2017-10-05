
$(document).ready(function () {
"use strict";


    $(document).ajaxStart(function() {

       
    });

    $(document).ajaxStop(function() {

    });

   update_task_table();


//
//TWORZENIE EVENTU DLA KAZDEGO PRZYCISKU DODOWANIA URZADZEN
//
  $.get( "/moduly", function(data) { 
   for(let i = 0; i < $("#liczba_modulow").val(); i++){
   
   
         
         $("#dodaj"+data.moduly[i].id).click(function (event){
        
         //UKRYWANIE POL FORMULARZA
         $("#nazwa"+data.moduly[i].id).toggle().val('');
         $('input#rejestr'+data.moduly[i].id).css("background-color", "white").val('');
         $('#rejestr'+data.moduly[i].id).toggle().val('');
         $('#submit'+data.moduly[i].id).toggle();
         $('#sterowanie'+data.moduly[i].id).toggle();
      });
   }
   






//
//FORMULARZ DODAWANIA URZADZEN
//
         
   for(let i = 0; i < $('#liczba_modulow').val(); i++){
      

      
      
     
      $('#post'+data.moduly[i].id).submit(function (event) {
         
         //$.get("/moduly", function(data){
         //   modul = data.moduly
         //      var iloscUrzadzen = Object.size(modul[i+1].urzadzenia);
         //      
         //      for(var k = 0;k<iloscUrzadzen;k++){
         //         var urzadzenie = modul[i+1].urzadzenia[k];
         //         if (urzadzenie.rejestr == $("input#rejestr"+(i+1)).val()) alert('zajete')
         //      }
         //
         //});

         //alert(data);
         
         //$("input#rejestr"+(i+1)).val()
         //$("input#nazwa"+(i+1)).val()
         
         $('input#rejestr'+(i+1)).css("background-color", "white")
         let nazwa = $("input#nazwa"+data.moduly[i].id).val();
         let rejestr;
         if (isNumber($("input#rejestr"+data.moduly[i].id).val())){
            rejestr = $("input#rejestr"+data.moduly[i].id).val();
         }
         else {event.preventDefault();
         $('input#rejestr'+data.moduly[i].id).css("background-color", "red")
         return}
         let id_modul = $("input#id_modul"+data.moduly[i].id).val();
         
         let sterowanie = $("#sterowanie"+data.moduly[i].id).val();
         $('input#nazwa'+data.moduly[i].id).toggle();
         $('input#rejestr'+data.moduly[i].id).toggle();
         $('input#submit'+data.moduly[i].id).toggle();
         $('#sterowanie'+data.moduly[i].id).toggle();
         event.preventDefault();
         let json = {nazwa: nazwa, rejestr:rejestr, id_modul:id_modul, sterowanie:sterowanie};
         ajaxPost(json);
      });
   }
});
});
   
   
   

   
//   
//FUNKCJE   
//
function isNumber(obj) { return !isNaN(parseInt(obj)) }

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
            var date = data.date;
            

            for(var i = 0;i<moduly.length;i++){
               //for(var i = 0; i<moduly[i].urzadzenia.length;i++){
               // Get the size of an object
               var iloscUrzadzen = Object.size(moduly[i].urzadzenia);
               var modul_id = moduly[i].id;
               for(var j = 0;j<iloscUrzadzen;j++){
                  
                  var urzadzenia = moduly[i].urzadzenia[j];
                  if (urzadzenia.sterowanie !== 'odczyt pozar')$('p#text'+modul_id).append(urzadzenia.name+'<br>');
/*                  $("#contentLoading").hide();
                  $("#ready").hide();
                  $("#contentLoading2").show()*/;
                  if(urzadzenia.sterowanie == 'on/off')
                  $('p#text'+modul_id).append('<a><p class="text-info datesize">'+date+'</p><div id="onoff'+modul_id+urzadzenia.id+'" class="on_off"></div></a>');
                  if(urzadzenia.sterowanie == 'tylko do odczytu' || 'odczyt temperatura' || 'odczyt cisnienie' || 'odczyt wilgotnosc' || 'odczyt prad' || 'odczyt kontaktron' || 'odczyt PIR' || 'odczyt co2')
                  valueChange(modul_id,urzadzenia.wartosc,date,urzadzenia.sterowanie);
                  
                  RGB(urzadzenia.sterowanie,modul_id,urzadzenia.rejestr,urzadzenia.r,urzadzenia.g,urzadzenia.b,date);
                  if(urzadzenia.sterowanie == '0-100%') sliderChange('#bar'+modul_id+urzadzenia.id,urzadzenia.rejestr,modul_id,urzadzenia.id,urzadzenia.wartosc,date);
                  // dodac kolejne mozliwosci sterowania
                  
                  

                  if (urzadzenia.sterowanie !== 'odczyt pozar')$('p#text'+modul_id).append('<br><br><br>');
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
            
            }
         
     });

   
   
}
function valueChange(modul_id, wartosc, date, sterowanie){
   
   if (wartosc === null) wartosc = 0;
   
   if (sterowanie == 'tylko do odczytu'){
      sNumber = wartosc.toString();
      $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div class="container"><p class="default-0">'+sNumber+'</p></div>');}
      
   else if (sterowanie == 'odczyt kontaktron'){
      console.log(wartosc);
      if (wartosc == 0) $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div class="kontaktron"></div>');
      else $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div class="kontaktron2"></div>');}
      
   else if (sterowanie == 'odczyt PIR'){
      console.log(wartosc);
      if (wartosc == 0) $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div class="pir"></div>');
      else $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div class="pirruch"></div>');}
       
   else if (sterowanie == 'odczyt temperatura'){
      sNumber = wartosc.toString();
      $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div><p class="default-0">'+sNumber+' &deg;C'+'</p></div>');}
      
   else if (sterowanie == 'odczyt cisnienie'){
      sNumber = wartosc.toString();
      $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div><p class="default-0">'+sNumber+' hPa'+'</p></div>');}
      
   else if (sterowanie == 'odczyt wilgotnosc'){
      sNumber = wartosc.toString();
      $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div><p class="default-0">'+sNumber+' %RH'+'</p></div>');}

   else if (sterowanie == 'odczyt co2'){
      sNumber = wartosc.toString();
      $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div><p class="default-0">'+sNumber+' ppm'+'</p></div>');}

   else if (sterowanie == 'odczyt pozar'){
      sNumber = wartosc.toString();
      if (wartosc == 1){
            $('#pozar').addClass('flameicon');
            //document.getElementById("datapozar").innerHTML = ""+date;
            /*$('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div class="flame"></div>');*/}
      if (wartosc == 0) {
            $('#pozar').removeClass('flameicon');
             //document.getElementById("datapozar").innerHTML = "";
            }
      }

   else if (sterowanie == 'odczyt prad'){
      nowaliczba = wartosc/100;
      //console.log(nowaliczba);
      //sNumber = wartosc.toString();
      $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div><p class="default-0">'+nowaliczba+' A'+'</p></div>');}   
   //output = [];
   //for (var i = 0, len = sNumber.length; i < len; i += 1) {
   //    output.push(+sNumber.charAt(i));
   //}
   
   //if (output.length == 1) $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div class="container"><p class="default-'+output[0]+'"></p></div>');
   //else if (output.length == 2) $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div class="container"><p class="default-'+output[1]+'"></p><p class="default-'+output[0]+'"></p></div>');
   //else if (output.length == 3) $('p#text'+modul_id).append('<p class="text-info datesize">'+date+'</p><div class="container"><p class="default-'+output[2]+'"></p><p class="default-'+output[1]+'"></p><p class="default-'+output[0]+'"></p></div>');
}


function clear_text() {
   
   $('p.card-text').empty();
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
function sliderChange(id,rejestr,modul_id,urzadzenia_id,urzadzenia_wartosc,date){
   


      $('p#text'+modul_id).append('<input class="slider" type="range" id="bar'+modul_id+urzadzenia_id+'" min="0" max="100" step="1" value="'+urzadzenia_wartosc+'">');
      $('p#text'+modul_id).append('<div class="costam slider">'+urzadzenia_wartosc+'%</div>');

   $(id).bind('input change', function(event){  
      var value = $(this).val();
      if($.active > 0){ 
      getrequest.abort();
      }
      $('.costam').empty();
      $('.costam').append(value+'%');
      value = parseInt(value);
      var json = {rejestr: rejestr, modul_id: modul_id, wartosc: value};
      ajaxPost(json);
      return false;
      
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

function RGB(sterowanie,modul_id,rejestr,r,g,b,date){
   
   
   
   if (sterowanie == 'RGB'){
      ileUrzadzen++;
      if(r === null || g === null || b === null){
         r=0;
         g=0;
         b=0;
         }
      $('p#text'+modul_id).append('<a><p class="text-info datesize">'+date+'</p></a>');  
      $('p#text'+modul_id).append('<div id="colorSelector" class="rgb'+modul_id+'"><div class="rgbi'+modul_id+rejestr+'"style="background-color: rgb('+r+','+g+','+b+')" ></div></div>');
       
   
      if (true){
         $('.rgb'+modul_id).ColorPicker({
         color: {r: r, g: g,b: b},
         //eventName: 'touchstart',
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
            $('.rgbi'+modul_id+rejestr).css('backgroundColor', '#' + hex);
            if($.active > 0){ 
               getrequest.abort();
            }
           
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
function ajaxGet(){
   
      if($.active > 0){ 
      getrequest.abort();
   }

   $.ajax(
         '/moduly',
   {
      method: "GET",
      dataType: "json",
  
   })
}


function wyslijAddress(){
   var address = $('#liczba_modulow').val();
   var nowyaddress = parseInt(address) + 1;
   var json = {address: nowyaddress};
   
   //alert(nowyaddress);
   ajaxPost(json);
   
}


   function handleData(data) {
    
  console.log(data)
   }   


