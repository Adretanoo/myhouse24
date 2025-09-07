document.getElementById("showPass").addEventListener("click", function () {
    const passwordFields = ["id_password", "id_confirm_password"]; // id ваших інпутів
    let show = false;

    passwordFields.forEach(function (id) {
        const input = document.getElementById(id);
        if (input && input.type === "password") {
            show = true;
        }
    });

    passwordFields.forEach(function (id) {
        const input = document.getElementById(id);
        if (input) {
            input.type = show ? "text" : "password";
        }
    });

    const icon = this.querySelector("i");
    if (show) {
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
});

function generatePassword(fieldIds) {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()";
    let password = "";
    for (let i = 0; i < 12; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
    }

    fieldIds.forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.value = password;
        }
    });
}
