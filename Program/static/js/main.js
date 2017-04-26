DEBUG=false
function log(class_name, msg) {
  console.log(class_name + ": " + msg)
}

// Functions to create the drop down menu
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

// Function to check if all inputs in form are correct CPW
function validateFormCPW() {
  var errors = [];

  var Width_Of_Track = document.forms["myform"]["Width_Of_Track"].value;
  var Width_Of_Gap = document.forms["myform"]["Width_Of_Gap"].value;
  var Width_Of_Ground = document.forms["myform"]["Width_Of_Ground"].value;
  var conducting_trace_layer = document.forms["myform"]["conducting_trace_layer"].value;

  if (isNaN(parseInt(Width_Of_Track))) {
    errors.push("Width of conductor (S) must be an number.");
  }

  if (isNaN(parseInt(Width_Of_Gap))) {
    errors.push("Width of gap (W) must be an number.");
  }

  if (isNaN(parseInt(Width_Of_Ground))) {
    errors.push("Width of ground (D) must be an number.");
  }

  $('input[name="layers_heights"]').each(function(){
    if ($(this).is(":visible") && isNaN(parseInt(this.value))) {
      errors.push('Layer Height "' + this.value + '" must be a number.');
    }
  })

  $('input[name="layers_permittivity"]').each(function(){
    if ($(this).is(":visible") && isNaN(parseInt(this.value))) {
      errors.push('Layer Permittivity "' + this.value + '" must be a number.');
    }
  })

  if (conducting_trace_layer == ""){
    errors.push('One radio button to select conductors layer must be pressed.');
  }

  if (errors.length == 0) {
    return true
  } else {
    var errorMessage = "Errors are:\n" + errors.join("\n")
    alert(errorMessage)
    return false
  }
}

// Function to check if all inputs in form are correct Microstrip
function validateFormMicrostrip() {
  var errors = [];

  var Width_Of_Track = document.forms["myform"]["Width_Of_Track"].value;
  var Thickness_Of_Conductor = document.forms["myform"]["Thickness_Of_Conductor"].value;
  var conducting_trace_layer = document.forms["myform"]["conducting_trace_layer"].value;

  if (isNaN(parseInt(Width_Of_Track))) {
    errors.push("Width of conductor (S) must be an number.");
  }

  if (isNaN(parseInt(Thickness_Of_Conductor)) && Thickness_Of_Conductor != "") {
    errors.push("Thickness of Conductor (T) need to be a number or left empty.");
  }

  $('input[name="layers_heights"]').each(function(){
    if ($(this).is(":visible") && isNaN(parseInt(this.value))) {
      errors.push('Layer Height "' + this.value + '" must be a number.');
    }
  })

  $('input[name="layers_permittivity"]').each(function(){
    if ($(this).is(":visible") && isNaN(parseInt(this.value))) {
      errors.push('Layer Permittivity "' + this.value + '" must be a number.');
    }
  })

  if (conducting_trace_layer == ""){
    errors.push('One radio button to select conductors layer must be pressed.');
  }

  if (errors.length == 0) {
    return true
  } else {
    var errorMessage = "Errors are:\n" + errors.join("\n")
    alert(errorMessage)
    return false
  }
}

// Function to change the number of heights and relative permittivities
//shown when the number of layers is picked from the drop down menu
function attachChangeEventToLayerInput() {
  console.log('This is running')
  $('#select_layers').on('change', function() {
    var num_layers_to_show = parseInt(this.value);
    var layers = $($('.layer_input').get().reverse())
    for (var i = 0; i < layers.length; i++) {
      var layer = $(layers[i]);
      if (i < num_layers_to_show) {
        layer.show();
        console.log('This is running two')
        $('input', layer).prop('disabled', false);
      } else {
        layer.hide();
        console.log('This is running three')
        $('input', layer).prop('disabled', true);
      }
    }
  })
}

// When the document is loaded load the attachChangeEventToLayerInput function
$(document).ready(function() {
  attachChangeEventToLayerInput();
})
