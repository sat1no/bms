var moduly;
$(document).ready(function () {

     $(document).ajaxStart(function() {
        working = true;
    });

    $(document).ajaxStop(function() {
    //$('#'+moduly[0].name).click(function(){
    //    $("#myDropdown2").toggleClass("show");
    //});
    //window.onclick = function(event) {
    //    if (!event.target.matches('.btn-lg')) {
    //  
    //      var dropdowns = document.getElementsByClassName("dropdown-content");
    //      var i;
    //      for (i = 0; i < dropdowns.length; i++) {
    //        var openDropdown = dropdowns[i];
    //        if (openDropdown.classList.contains('show')) {
    //          openDropdown.classList.remove('show');
    //        }
    //        }
    //    }
    //};
    //    working = false;
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
//Object.size = function(obj) {
//    var size = 0, key;
//    for (key in obj) {
//        if (obj.hasOwnProperty(key)) size++;
//    }
//    return size;
//};

//function modulyDict(moduly){
//    
//    
//}