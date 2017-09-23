$(document).ready(function(){


});
function ajaxDelete(rejestr, modul){
   
   var json = {rejestr: rejestr, modul: modul};
   
   console.log(rejestr);
   console.log(modul);
   
    $.ajax(
         "/moduly",
         {
           method: "DELETE",
           contentType: "application/json",
           data: JSON.stringify(json),
           success: function () {location.reload();}
           });
   
}