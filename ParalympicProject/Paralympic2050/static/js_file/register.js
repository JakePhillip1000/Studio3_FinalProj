window.addEventListener("DOMContentLoaded", function () {
    let isTaken = document.getElementById("username_taken").value === "True";
    if (isTaken) {
        let takenUser = document.getElementById("taken_username").value;
        alert("Username '" + takenUser + "' is already taken. Choose new username");
        document.getElementById("register-form").reset();
    }

    let notmatch = document.getElementById("password_mismatch").value === "True";
    if (notmatch) {
        alert("Password and confirm password does not match");
        document.getElementById("register-form").reset();
    }
});