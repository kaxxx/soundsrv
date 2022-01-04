var clientname;

        
$.ajax({

    type: "GET",
    url: "../hostname",
    dataType: "text",
    success: function(response){
        clientname = response
        document.getElementById("name").value = clientname;
    }
}) 