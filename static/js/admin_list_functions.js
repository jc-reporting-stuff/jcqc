const checkOwnBox = (event) => {
    let oligoID = /\d+/.exec(event.target.name)[0];
    let checkbox = document.getElementsByName(`${oligoID}-checkbox`)[0]
    checkbox.checked = true;
    if (event.target.key === 'Enter') {
        event.preventDefault();
        console.log('enter');
    }
}

const selectAll = (event) => {
    if (event.target.name === 'select-all') {
        event.preventDefault();
    }
    
    let button = document.querySelector('#select-all-button');

    let topCheckbox = document.querySelector('#top-checkbox');
    topCheckbox.checked = !topCheckbox.checked;
    let oligoCheckboxes = document.querySelectorAll('.oligo-view input[type="checkbox"]');
    
    for (box of oligoCheckboxes) {
        if (button.textContent === 'Select All') {
            box.checked = true;
        }
        else {
            box.checked = false;
        }
    }
    button.textContent = button.textContent === 'Select All' ? 'Select None' : 'Select All';
}

const checkEnter = (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        deliveryButton = document.querySelector('#update-delivery');
        deliveryButton.click();
    }
}