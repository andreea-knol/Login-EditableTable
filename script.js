function changeAge(id){

    // the id that is passed as a parameter is actually the id of the record that has been modified

    // the 'age' variable contains the new age that the user entered
    age = document.getElementById(id).value;

    document.getElementById("demo").innerHTML = "The id is: " + id + " and the new age is: " + age;

    if (id && age) { // values are not empty
        $.ajax({
            type: "POST",
            url: "/cgi-bin/ajax.cgi",
            dataType: "text",
            data: "id=" + id + "&age=" + age,
            error: function(){
                alert("script call was not successful");
            },
            success: function(){
                alert("script call was successful");
            }
        });  

    }

}
