document.addEventListener("DOMContentLoaded", () => {

    console.log("Expense Tracker Loaded");

});

setTimeout(() => {

    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        alert.remove();
    });

}, 5000);