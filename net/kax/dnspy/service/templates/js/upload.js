var clientname;

        
$.ajax({

    type: "GET",
    url: "../hostname",
    dataType: "text",
    success: function(response){
        clientname = response
        document.getElementById("whois").innerHTML = "Du bist: " + clientname;
        document.getElementById("name").value = clientname;
    }
}) 