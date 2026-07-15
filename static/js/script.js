window.onload = function () {

    setTimeout(function () {

        document.getElementById("loader").style.display = "none";

    }, 2200);

}
setTimeout(function () {

    let alert = document.querySelector(".alert");

    if (alert) {

        alert.style.display = "none";

    }

}, 3000);