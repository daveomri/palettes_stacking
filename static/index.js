var formfield = document.getElementById('formfield');

function add(){
  var newField = document.createElement('input');
  newField.setAttribute('type','text');
  newField.setAttribute('name','text');
  newField.setAttribute('class','text');
  newField.setAttribute('siz',50);
  newField.setAttribute('placeholder','Optional Field');
  formfield.appendChild(newField);
}

function remove(){
  var input_tags = formfield.getElementsByTagName('input');
  if(input_tags.length > 2) {
    formfield.removeChild(input_tags[(input_tags.length) - 1]);
  }
}

let form = document.querySelector('#palettes-form');
form.addEventListener('submit', function (event) {
	// Ignore the #toggle-something button
	if (event.submitter.matches('.input')) {
		event.preventDefault();
	}

    if (event.submitter.matches('.remove')) {
		event.preventDefault();
	}
});

