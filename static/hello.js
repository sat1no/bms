$(document).ready(function () {
   
   // load the content initially
   // GET /
   clear_text();
   update_task_table() ;


   
   for(let i = 0; i < $('#liczba_modulow').val(); i++){
      
//
//TWORZENIE FUNKCJI DLA KAZDEGO PRZYCISKU DODOWANIA URZADZEN
//
      $('#dodaj'+(i+1)).click(function (event){
        
         //UKRYWANIE POL FORMULARZA GDY
         $('#nazwa'+(i+1)).toggle();
         $('#rejestr'+(i+1)).toggle();
         $('#submit'+(i+1)).toggle();
         $('#sterowanie'+(i+1)).toggle();
      });
   }


   
   
   
      
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
         //insert new element in db
         $.ajax("/moduly",
                {
                  method: "POST",
                  contentType: 'application/json',
                  data: JSON.stringify(json),
                  
                  success: function(data,status) {
                     alert(status);
                     clear_text();
                     update_task_table();
                  }
                  
                });
      });
   }
});     // post
      
      //update content
      // GET /
      
   
   
   
   
   
   


function update_task_table() {
   
   //get json with list of elements from server
   $.ajax(
     '/moduly',
     {
         method: "GET",
         dataType: "json",
         success: function(data, status) {
            //alert(data.nowe[0].name);
            //alert(status);
            var moduly = data.moduly;
            for(var i = 0;i<moduly.length;i++){
               //for(var i = 0; i<moduly[i].urzadzenia.length;i++){
                  
               var urzadzenia = moduly[i].urzadzenia[i];
               var modul_id = moduly[i].id
               $('p#text'+(i+1)).append(urzadzenia.name+': <div id="onoff'+modul_id+'" class="on_off"></div>');
               $(document).on('click', '#onoff'+modul_id , function(event){
                  $('#onoff'+modul_id).toggleClass('on_off');

                  $('#onoff'+modul_id).toggleClass('on_off2');



               
               }); 
               if (urzadzenia.sterowanie == 'RGB'){
                  $('p#text'+modul_id).append('<a id="colorSelector"><div style="background-color: rgb('+urzadzenia.r+','+urzadzenia.g+','+urzadzenia.b+')" ></div></a>');
                   

                 
                    
                  
                  
                  
                  $('#colorSelector').ColorPicker({
                  color: {r: urzadzenia.r, g: urzadzenia.g,b: urzadzenia.b},
                  onShow: function (colpkr) {
                  $(colpkr).fadeIn(500);
                  
                  return false;
                  },
                  onHide: function (colpkr) {
                  $(colpkr).fadeOut(500);
                  return false;
                  },
                  onChange: function (hsb, hex, rgb) {
                  $('#colorSelector div').css('backgroundColor', '#' + hex);
                  },
                  
                  onSubmit: function (hsb, hex, rgb) {
                  
                  
                  var rgbwithid = {r: rgb.r, g: rgb.g, b: rgb.b, modul_id: modul_id}
                     
                  $.ajax(
                         "/moduly",
                         {
                           method: "POST",
                           contentType: "application/json",
                           data: JSON.stringify(rgbwithid),
                           success: function (status) {alert(status)}
                           })
                  
                  
                  }
                  
                  });
                  
               }

            }
         }
     });

   
   
}

function clear_text() {
   
   $('p.card-text').empty()
   

   
}


    //function changeImage() {
    //
    //    if (document.getElementById("imgClickAndChange").src == "http://www.userinterfaceicons.com/80x80/minimize.png") 
    //    {
    //        document.getElementById("imgClickAndChange").src = "http://www.userinterfaceicons.com/80x80/maximize.png";
    //    }
    //    else 
    //    {
    //        document.getElementById("imgClickAndChange").src = "http://www.userinterfaceicons.com/80x80/minimize.png";
    //    }
    //}




