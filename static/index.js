function add(){
  let formfield = document.getElementById('formfield');
  let input_tags = formfield.getElementsByTagName('input');
  let palette_id = input_tags.length / 2 + 1;

  let formfieldRow = document.createElement('div');
  formfieldRow.setAttribute('class', 'formfield-row');

  let formfieldName = document.createElement('p');
  formfieldName.appendChild(document.createTextNode(`Palette ${palette_id}`));

  let newFieldLeft = document.createElement('input');
  newFieldLeft.setAttribute('type','number');
  newFieldLeft.setAttribute('min','0');
  newFieldLeft.setAttribute('name',`palette-${palette_id}-left`);
  newFieldLeft.setAttribute('class','palette-left');
  newFieldLeft.setAttribute('placeholder', `width`);
  newFieldLeft.setAttribute('required', '');

  let newFieldRight = document.createElement('input');
  newFieldRight.setAttribute('type','number');
  newFieldRight.setAttribute('min','0');
  newFieldRight.setAttribute('name',`palette-${palette_id}-right`);
  newFieldRight.setAttribute('class','palette-right');
  newFieldRight.setAttribute('placeholder', `length`);
  newFieldRight.setAttribute('required', '');


  formfieldRow.appendChild(formfieldName);
  formfieldRow.appendChild(newFieldLeft);
  formfieldRow.appendChild(newFieldRight);

  formfield.appendChild(formfieldRow);
}

function remove(){
  let formfield = document.getElementById('formfield');
  let input_tags = formfield.getElementsByTagName('div');
  if(input_tags.length > 1) {
    formfield.removeChild(input_tags[(input_tags.length) - 1]);
  }
}

