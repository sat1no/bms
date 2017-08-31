$(document).ready(function () {
   
   // load the content initially
   // GET /
   update_task_table() ;
   
   
   $('form').submit(function (event) {
      
      //check valid
      
      
      //insert new element in db
      // post
      
      //update content
      // GET /
      
   });
   
   
   
   
   
});

function update_task_table() {
   
   //get json with list of elements from server
   $.ajax(
     '/getnowe',
     {
         method: "GET",
         dataType: "json",
         success: function(data, status) {
            alert(data);
            alert(status);
         }
     }
   );
   
};