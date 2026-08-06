const TUTOR_WHATSAPP = "2347063186164";
let studentName = "";

async function loadProfileName() {
    const res = await fetch("/profile/data");
    const data = await res.json();
    studentName = data.name || "A student";
}

async function loadMyCourses() {
    await loadProfileName();

    const res = await fetch("/my-courses");

    if (res.status === 401) {
        window.location.href = "/login-page";
        return;
    }

    const courses = await res.json();
    const container = document.getElementById("myCourseList");
    container.innerHTML = "";

    if (courses.length === 0) {
        container.innerHTML = "<p>You haven't enrolled in any course yet. <a href='/courses-page'>Browse courses</a></p>";
        return;
    }

    container.className = "course-container";

    courses.forEach(course => {
        const message = encodeURIComponent(
            `Hi! I'm ${studentName}, I just paid for "${course.title}" on Joshim. Can we schedule my class time?`
        );
        const whatsappLink = `https://wa.me/${TUTOR_WHATSAPP}?text=${message}`;

        const whatsappButton = `
            <a href="${whatsappLink}" target="_blank" style="display:inline-flex; align-items:center; gap:8px; background:#25D366; color:#fff; text-decoration:none; padding:11px 18px; border-radius:6px; font-size:0.95rem;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.48 1.32 5L2 22l5.25-1.38c1.46.8 3.1 1.22 4.78 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0012.04 2m0 1.67c2.2 0 4.26.86 5.82 2.42a8.19 8.19 0 012.41 5.82c0 4.54-3.7 8.23-8.24 8.23a8.2 8.2 0 01-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.18 8.18 0 01-1.26-4.37c0-4.54 3.7-8.24 8.25-8.24m-4.53 4.72c-.16 0-.42.06-.64.3-.22.24-.85.83-.85 2.02 0 1.19.87 2.34.99 2.5.12.16 1.7 2.6 4.12 3.64.58.25 1.03.4 1.38.51.58.18 1.11.16 1.53.1.47-.07 1.44-.59 1.64-1.16.2-.57.2-1.06.14-1.16-.06-.1-.22-.16-.46-.28-.24-.12-1.44-.71-1.66-.79-.22-.08-.38-.12-.55.12-.16.24-.63.79-.77.95-.14.16-.28.18-.52.06-.24-.12-1.01-.37-1.93-1.19-.71-.63-1.19-1.42-1.33-1.66-.14-.24-.02-.37.1-.49.11-.11.24-.28.36-.42.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.42-.06-.12-.55-1.34-.76-1.83-.2-.48-.4-.42-.55-.42h-.47z"/></svg>
                Book your class
            </a>`;

        let actionHtml = "";

        if (course.paid) {
            actionHtml = whatsappButton;
        } else if (course.price && course.price > 0) {
            actionHtml = `
                <button class="btn btn-accent" onclick="payForCourse(${course.id})">💳 Pay now — ₦${course.price}</button>
                <button class="btn delete" style="width:100%; margin-top:8px;" onclick="cancelEnrollment(${course.id})">Remove this course</button>
            `;
        } else {
            actionHtml = `
                <div>
                    <p style="font-size:0.88rem; color:var(--slate); margin-bottom:8px;">
                        Have an access code from your tutor? Enter it below.
                    </p>
                    <input type="text" id="code-${course.id}" placeholder="Enter access code" style="text-transform:uppercase;">
                    <button class="btn btn-accent" style="width:100%; margin-top:8px;" onclick="redeemCode(${course.id})">Unlock access</button>
                    <p id="codeMsg-${course.id}" style="font-size:0.85rem; margin-top:6px;"></p>
                    <button class="btn delete" style="width:100%; margin-top:8px;" onclick="cancelEnrollment(${course.id})">Remove this course</button>
                </div>
            `;
        }

        container.innerHTML += `
            <div class="card">
                <h3>${course.title}</h3>
                <p>${course.description}</p>
                <div class="actions">
                    ${actionHtml}
                </div>
            </div>
        `;
    });
}

async function payForCourse(courseId) {
    const res = await fetch("/pay", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ course_id: courseId })
    });

    const result = await res.json();

    if (result.error) {
        alert(result.error);
        return;
    }

    window.location.href = result.authorization_url;
}

async function redeemCode(courseId) {
    const codeInput = document.getElementById(`code-${courseId}`);
    const msgBox = document.getElementById(`codeMsg-${courseId}`);

    const res = await fetch("/redeem-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ course_id: courseId, code: codeInput.value })
    });

    const result = await res.json();

    if (result.error) {
        msgBox.style.color = "var(--danger)";
        msgBox.textContent = result.error;
        return;
    }

    msgBox.style.color = "var(--accent-deep)";
    msgBox.textContent = result.message;

    setTimeout(loadMyCourses, 1000);
}

async function cancelEnrollment(courseId) {
    if (!confirm("Remove this course from your dashboard?")) return;

    const res = await fetch(`/my-courses/${courseId}`, { method: "DELETE" });
    const result = await res.json();

    if (result.error) {
        alert(result.error);
        return;
    }

    loadMyCourses();
}

loadMyCourses();