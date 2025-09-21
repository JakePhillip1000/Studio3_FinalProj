window.addEventListener("DOMContentLoaded", function () {
    const errorDiv = document.getElementById("login-error");
    const form = document.getElementById("login-form");
    const entusern = document.getElementById("entered-username").value;

    const userNotExist = document.getElementById("username-not-exist").value === "1";
    if (userNotExist) {
        const msg = "Username "+ entusern + " does not exist";
        if (errorDiv) {
            errorDiv.textContent = msg;
            errorDiv.style.display = "block";
        }
        if (form){
            form.reset()
        }
        alert(msg);  
    }

    const wrongPass = document.getElementById("wrong-pass").value === "1";
    if (wrongPass) {
        const message = "Username or password is incorrect";
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = "block";
        }
        if (form){
            form.reset();
        }
        alert(message);
    }
});
