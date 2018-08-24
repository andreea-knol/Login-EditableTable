function changeAge(id){

    // the id that is passed as a parameter is actually the id of the record that has been modified

    // the 'age' variable contains the new age that the user entered
    age = document.getElementById(id).value;

    document.getElementById("demo").innerHTML = "The id is: " + id + " and the new age is: " + age;


    if (id && age) { // values are not empty
        $.ajax({
            type: "POST",
            url: "/cgi-bin/receive_ajax_request.cgi",
            dataType: "application/json",
            data: {
                'data_id' : id,
                'data_age': age
            },
            error: function(){
                alert("script call was not successful");
            },
            success: function(data){
                alert("success" + data);
            }
        });  

    } else {
        alert("script call was not successful");
    }

}
