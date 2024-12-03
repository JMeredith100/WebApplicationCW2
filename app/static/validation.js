
function validateLoginForm() {
    let name = document.getElementById('form_username').value;
    let password = document.getElementById('form_password').value;

    let isValid = true;

    // Username Field
    if (name.trim() == "") {
        alert("Name field cannot be empty.");
        isValid = false;
    }
    else if (name.length < 3 || name.length > 25) {
        alert("Username field must be between 3 and 25 characters.");
        isValid = false;
    }

    // Password Field
    else if (password.trim() == "") {
        alert("Password field cannot be empty.");
        isValid = false;
    }
    else if (password.length < 5 || password.length > 15) {
        alert("Password field must be between 5 and 15 characters.");
        isValid = false;
    }
    
    return isValid;
}


function validateRegisterForm() {
    let name = document.getElementById('form_username').value;
    let password = document.getElementById('form_password').value;
    let dob = document.getElementById('form_dob').value;

    let isValid = true;

    // Username Field
    if (name.trim() == "") {
        alert("Name field cannot be empty.");
        isValid = false;
    }
    else if (name.length < 3 || name.length > 35) {
        alert("Username field must be between 3 and 35 characters.");
        isValid = false;
    }

    // Password Field
    else if (password.trim() == "") {
        alert("Password field cannot be empty.");
        isValid = false;
    }
    else if (password.length < 5 || password.length > 15) {
        alert("Password field must be between 5 and 15 characters.");
        isValid = false;
    }

    // Date of Birth Field
    else if (!date) {
        alert("Date of Birth field must not be empty");
        isValid = false;
    }
    
    return isValid;
}

function validatePostForm() {
    let title = document.getElementById('form_post_title').value;
    let content = document.getElementById('form_content').value;

    let isValid = true;

    // Title Field
    if (title.trim() == "") {
        alert("Title field cannot be empty.");
        isValid = false;
    }
    else if (title.length < 4 || title.length > 35) {
        alert("Title field must be between 4 and 35 characters.");
        isValid = false;
    }

    // Content Field
    else if (content.trim() == "") {
        alert("Password field cannot be empty.");
        isValid = false;
    }
    else if (content.length < 10 || content.length > 500) {
        alert("Content field must be between 10 and 500 characters.");
        isValid = false;
    }
    
    return isValid;
}