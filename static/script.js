function add(){
  let formfield = document.getElementById('formfield');
  let input_tags = formfield.getElementsByTagName('input');
  let pallet_id = input_tags.length / 3 + 1;

  let formfieldRow = document.createElement('div');
  formfieldRow.setAttribute('class', 'formfield-row');

  let formfieldName = document.createElement('p');
  formfieldName.appendChild(document.createTextNode(`Pallet ${pallet_id}`));

  let newFieldLeft = document.createElement('input');
  newFieldLeft.setAttribute('type','number');
  newFieldLeft.setAttribute('min','0');
  newFieldLeft.setAttribute('name',`pallet-${pallet_id}-left`);
  newFieldLeft.setAttribute('class','pallet-left');
  newFieldLeft.setAttribute('placeholder', `width`);
  newFieldLeft.setAttribute('required', '');

  let newFieldRight = document.createElement('input');
  newFieldRight.setAttribute('type','number');
  newFieldRight.setAttribute('min','0');
  newFieldRight.setAttribute('name',`pallet-${pallet_id}-right`);
  newFieldRight.setAttribute('class','pallet-right');
  newFieldRight.setAttribute('placeholder', `length`);
  newFieldRight.setAttribute('required', '');

  let newFieldCount = document.createElement('input');
  newFieldCount.setAttribute('type','number');
  newFieldCount.setAttribute('min','1');
  newFieldCount.setAttribute('name',`pallet-${pallet_id}-count`);
  newFieldCount.setAttribute('class','pallet-count');
  newFieldCount.setAttribute('placeholder', `count`);
  newFieldCount.setAttribute('required', '');


  formfieldRow.appendChild(formfieldName);
  formfieldRow.appendChild(newFieldLeft);
  formfieldRow.appendChild(newFieldRight);
  formfieldRow.appendChild(newFieldCount);

  formfield.appendChild(formfieldRow);
}

function remove(){
  let formfield = document.getElementById('formfield');
  let input_tags = formfield.getElementsByTagName('div');
  if(input_tags.length > 1) {
    formfield.removeChild(input_tags[(input_tags.length) - 1]);
  }
}

