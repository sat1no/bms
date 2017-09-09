
$(document).ready(function () {
   
   // load the content initially
   // GET /
   
   //setInterval(function() {

   //}, 1500);

   update_task_table();


   
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
            clear_text();
            var moduly = data.moduly;
            for(var i = 0;i<moduly.length;i++){
               //for(var i = 0; i<moduly[i].urzadzenia.length;i++){
               // Get the size of an object
               var iloscUrzadzen = Object.size(moduly[i].urzadzenia);
               var modul_id = moduly[i].id;
               for(var j = 0;j<iloscUrzadzen;j++){
                  
                  var urzadzenia = moduly[i].urzadzenia[j];
                  $('p#text'+(i+1)).append(urzadzenia.name+'<br>')
                  if(urzadzenia.sterowanie != 'tylko do odczytu')$('p#text'+(i+1)).append('<a><div id="onoff'+modul_id+urzadzenia.id+'" class="on_off"></div></a>');
                  RGB(urzadzenia.sterowanie,modul_id,urzadzenia.rejestr,urzadzenia.r,urzadzenia.g,urzadzenia.b)
                  if(urzadzenia.sterowanie == '0-100%') sliderChange('#bar'+modul_id+urzadzenia.id,urzadzenia.rejestr,modul_id,urzadzenia.id,urzadzenia.wartosc);


                  

                  $('p#text'+(i+1)).append('<br><br>')
                  togClasses('#onoff'+modul_id+urzadzenia.id,'on_off','on_off2', urzadzenia.rejestr, modul_id);
                  if (urzadzenia.stan > 0){
                     
                     $('#onoff'+modul_id+urzadzenia.id).toggleClass('on_off')
                     $('#onoff'+modul_id+urzadzenia.id).toggleClass('on_off2')
                  }
                  
               }                  
                  
               }



            },
            complete: function (){
              
              setTimeout(update_task_table, 2500);
            return false;
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

function togClasses(id,class1,class2,rejestr,modul_id){
   
   //$(document).on('click', id , function(event){
      $(id).bind('click', function(event){
      $(id).toggleClass(class1);
      
      $(id).toggleClass(class2);
      
      var onOff = {modul_id: modul_id, rejestr: rejestr};
      var className = $(id).attr("class");
      if( className == 'on_off') onOff['stan'] = 0;
      else onOff['stan'] = 1;
   
   
      $.ajax('/moduly',
             {
               method: 'POST',
               contentType: 'application/json',
               data: JSON.stringify(onOff),
               success: function(status){}
               
               });
      
   

   
   
   }); 
}
function sliderChange(id,rejestr,modul_id,urzadzenia_id,urzadzenia_wartosc){
   


      $('p#text'+modul_id).append('<p class="slider"><input type="range" id="bar'+modul_id+urzadzenia_id+'" min="0" max="100" step="1" value="'+urzadzenia_wartosc+'"></p>')
      $('p#text'+modul_id).append('<div class="costam slider">'+urzadzenia_wartosc+'%</div>');

   $(id).bind('click', function(event){  
      var value = $(this).val();

      $('.costam').empty();
      $('.costam').append(value+'%')
      value = parseInt(value)
      $.ajax(
          "/moduly",
          {
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({rejestr: rejestr, modul_id: modul_id, wartosc: value}),
            success: function () {}
            });
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

function RGB(sterowanie,modul_id,rejestr,r,g,b){
   
   
   
   if (sterowanie == 'RGB'){
      if(r === null || g === null || b === null){r=0;
      g=0;
      b=0;}
      $('p#text'+modul_id).append('<div id="colorSelector" class="rgb'+modul_id+'"><div class="rgbi'+modul_id+'"style="background-color: rgb('+r+','+g+','+b+')" ></div></div>');
       
   
     
      $('.rgb'+modul_id).ColorPicker({
      color: {r: r, g: g,b: b},
      onShow: function (colpkr) {
      $(colpkr).fadeIn(500);
      
      return false;
      },
      onHide: function (colpkr) {
      $(colpkr).fadeOut(500);
      return false;
      },
      onChange: function (hsb, hex, rgb) {
      $('.rgbi'+modul_id).css('backgroundColor', '#' + hex);
      },
      
      onSubmit: function (hsb, hex, rgb) {
      
      
      var rgbwithid = {r: rgb.r, g: rgb.g, b: rgb.b, modul_id: modul_id, rejestr: rejestr}
         
      $.ajax(
             "/moduly",
             {
               method: "POST",
               contentType: "application/json",
               data: JSON.stringify(rgbwithid),
               success: function (status) {}
            });
      
      }
      
      }); 
     
}
}

//function interval(func, wait, times){
//    var interv = function(w, t){
//        return function(){
//            if(typeof t === "undefined" || t-- > 0){
//                setTimeout(interv, w);
//                try{
//                    func.call(null);
//                }
//                catch(e){
//                    t = 0;
//                    throw e.toString();
//                }
//            }
//        };
//    }(wait, times);
//
//    setTimeout(interv, wait);
//};

