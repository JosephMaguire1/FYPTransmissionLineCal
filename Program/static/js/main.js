DEBUG=false
function log(class_name, msg) {
  console.log(class_name + ": " + msg)
}
/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction1() {
    document.getElementById("myDropdown1").classList.toggle("show1");
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn1')) {

    var dropdowns = document.getElementsByClassName("dropdown-content1");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show1')) {
        openDropdown.classList.remove('show1');
      }
    }
  }
}

function myFunction2() {
    document.getElementById("myDropdown2").classList.toggle("show2");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn2')) {

    var dropdowns = document.getElementsByClassName("dropdown-content2");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show2')) {
        openDropdown.classList.remove('show2');
      }
    }
  }
}

//////////////////////////////////////////////////////////////////


///////////////////////////////////////////
function explinationMicrostrip() {
    alert("I am an alert box!");
}

function attachChangeEventToLayerInput(layerName) {
  $('#select_layers_' + layerName).on('change', function() {
    alert("WE are at this point")
    var num_layers_to_show = parseInt(this.value);
    var layers = $('.layer_' + layerName + '_input')
    for (var i = 0; i < layers.length; i++) {
      var layer = $(layers[i]);
      if (i < num_layers_to_show) {
        layer.show();
        alert("WE are at the second point")
        $('input', layer).prop('disabled', false);
      } else {
        alert("WE are at the third point")
        layer.hide();
        $('input', layer).prop('disabled', true);
      }
    }
  })
}


$(document).ready(function() {
  attachChangeEventToLayerInput('above');
  attachChangeEventToLayerInput('below');
})


function validateForm() {
  var errors = [];

  var Width_Of_Track = document.forms["myform"]["Width_Of_Track"].value;
  console.log(Width_Of_Track)
  if (isNaN(parseInt(Width_Of_Track))) {
    errors.push("Width of trace (S) must be an number");
  }

  var layers_permittivity = $('input[name=layers_heights]').value;
  for (var i in layers_permittivity) {
    if (isNaN(parseInt(layers_permittivity[i]))) {
      errors.push("Relative Permittivity of each layer must be an number");
    }
  }

  var layers_heights = document.forms.getlist["myform"]["layers_heights"].value;
  console.log(layers_heights)
  ($('input[name=select_option]').each(
    if (isNaN(parseInt(layers_heights[i]))) {
      errors.push("Height of each layer must be an number");
    }
  )

  if (errors.length == 0) {
    return true
  }
  else {
    var errorMessage = "Errors are:\n" + errors.join("\n")
    alert(errorMessage)
    return false
  }
}
