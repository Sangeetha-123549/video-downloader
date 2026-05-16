document.addEventListener("DOMContentLoaded", function () {

const button = document.getElementById("downloadBtn");
const spinner = document.getElementById("spinner");
const message = document.getElementById("message");
const progressBar = document.getElementById("progressBar");
const input = document.getElementById("videoUrl");
const thumbnailBox = document.getElementById("thumbnailBox");
const thumbnail = document.getElementById("thumbnail");
const installBtn = document.getElementById("installBtn");

const socket = io();

/* ---------------- THUMBNAIL ---------------- */
input.addEventListener("input", function () {

    let url = input.value;
    let videoId = null;

    if (url.includes("watch?v=")) {
        videoId = url.split("watch?v=")[1].split("&")[0];
    }

    if (url.includes("youtu.be/")) {
        videoId = url.split("youtu.be/")[1];
    }

    if (videoId) {
        thumbnail.src = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
        thumbnailBox.style.display = "block";
    } else {
        thumbnailBox.style.display = "none";
    }
});


/* ---------------- DOWNLOAD ---------------- */
button.addEventListener("click", async function () {

    const url = input.value;

    if (url === "") {
        message.innerHTML = "Please enter URL ❌";
        return;
    }

    spinner.style.display = "block";
    button.disabled = true;

    progressBar.style.width = "0%";
    message.innerHTML = "Starting... ⏳";

    await fetch("/download", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
    });
});


/* ---------------- SOCKET ---------------- */
socket.on("progress_update", function (data) {
    progressBar.style.width = data.progress + "%";

    if (data.progress < 100) {
        message.innerHTML = "Downloading... " + data.progress + "%";
    }
});

socket.on("download_complete", function () {
    progressBar.style.width = "100%";
    message.innerHTML = "Download Complete ✅";

    spinner.style.display = "none";
    button.disabled = false;
});


/* ---------------- SERVICE WORKER ---------------- */
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/static/sw.js")
    .then(() => console.log("Service Worker Registered ✅"))
    .catch(err => console.log(err));
}


/* ---------------- PWA INSTALL ---------------- */
let deferredPrompt;

window.addEventListener("beforeinstallprompt", (e) => {

    e.preventDefault();
    deferredPrompt = e;

    if (installBtn) {
        installBtn.style.display = "block";
    }
});

if (installBtn) {
installBtn.addEventListener("click", async () => {

    if (!deferredPrompt) return;

    deferredPrompt.prompt();

    const choiceResult = await deferredPrompt.userChoice;

    if (choiceResult.outcome === "accepted") {
        console.log("App installed");
    }

    deferredPrompt = null;
    installBtn.style.display = "none";
});
}

});