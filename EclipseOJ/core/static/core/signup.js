document.getElementById('id_username').onblur = function () {
    var username = $(this).val();
    //alert("Called");
    var regex = /^[a-zA-Z0-9_@.+-]+$/
    if (!regex.test(username)){
      document.getElementsByClassName('help-block')[0].setAttribute("style","color : red");
      document.getElementsByClassName('help-block')[0].textContent = "Your username should contain only letters, numbers and symbols including _ @ . + -";
      //document.getElementById('id_username').focus();
    }
    else {
    console.log("here!");
    $.ajax({
      url: '/ajax/validate_username/',
      data: {
        'username': username
      },
      dataType: 'json',
      success: function (data) {
        if (data.is_taken) {
            document.getElementsByClassName('help-block')[0].setAttribute("style","color : red");
            document.getElementsByClassName('help-block')[0].textContent = "This username has already been taken";
            //document.getElementById('id_username').focus();
        }
        else {
          document.getElementsByClassName('help-block')[0].setAttribute("style","color : green");
          document.getElementsByClassName('help-block')[0].textContent = "This username can be used";
        }
      }
    });
    }
};
