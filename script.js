const button = document.getElementById("downloadBtn");
const message = document.getElementById("message");
const progressBar = document.getElementById("progressBar");
const input = document.getElementById("videoUrl");

button.addEventListener("click", async function () {

    const url = input.value;

    if (!url) {
        message.innerHTML = "Please enter URL ❌";
        return;
    }

    message.innerHTML = "Starting... ⏳";

    await fetch("/download", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
    });

    checkProgress();
});

async function checkProgress() {
    let interval = setInterval(async () => {

        let res = await fetch("/progress");
        let data = await res.json();

        progressBar.style.width = data.progress + "%";

        message.innerHTML = "Downloading... " + data.progress + "%";

        if (data.progress >= 100) {
            clearInterval(interval);
            message.innerHTML = "Download Complete ✅";
        }

    }, 500);
}