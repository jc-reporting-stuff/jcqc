const checkEnter = (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        inputName = event.target.name.split('-')[0];
        buttons = document.getElementsByName('search');

        buttonToClick = null;
        for (button of buttons) {
            if (button.value === inputName) {
                buttonToClick = button;
            }
        }
        buttonToClick.click();
    }
}

const addKeyupListeners = (elements) => {
    for (element of elements) {
        element.onkeypress = checkEnter;
    }
}


textInputs = document.querySelectorAll('input[type="text"]');
addKeyupListeners(textInputs);

dateInputs = document.querySelectorAll('input[type="date"]');
addKeyupListeners(dateInputs);