async function loadProfile() {
    const res = await fetch("/profile/data");
    const data = await res.json();

    document.getElementById("profileName").textContent = data.name;
    document.getElementById("profileEmail").textContent = data.email;
    document.getElementById("profilePhone").textContent = data.phone || "Not provided";

    if (data.profile_image) {
    const img = document.getElementById("profileImg");
    img.src = "/static/" + data.profile_image;
    img.style.display = "block";
    }
}

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("photoInput");
    if (!fileInput.files.length) {
        document.getElementById("uploadResponse").innerText = "Please choose a photo first.";
        return;
    }

    const formData = new FormData();
    formData.append("photo", fileInput.files[0]);

    const res = await fetch("/profile/upload", {
        method: "POST",
        body: formData
    });

    const result = await res.json();
    document.getElementById("uploadResponse").innerText = result.message || result.error;

    if (result.profile_image) {
        document.getElementById("profileImg").src = "/static/" + result.profile_image + "?t=" + Date.now();
    }
});

loadProfile();