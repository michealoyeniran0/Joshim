document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("courseForm");
    let editingId = null;
    let allCourses = [];

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            title: document.getElementById("title").value,
            description: document.getElementById("description").value,
            price: document.getElementById("price").value,
            video_url: document.getElementById("video_url").value
        };

        let url = "/admin/course";
        let method = "POST";

        if (editingId) {
            url = `/admin/course/${editingId}`;
            method = "PUT";
        }

        const res = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        document.getElementById("response").innerText = result.message || result.error;

        editingId = null;
        document.getElementById("formTitle").innerText = "Add a course";
        form.reset();

        loadCourses();
    });

    async function loadCourses() {
        const res = await fetch("/admin/courses");

        if (res.status === 403) {
            document.getElementById("courseList").innerHTML =
                "<p>Admins only. Please log in with an admin account.</p>";
            return;
        }

        allCourses = await res.json();

        const container = document.getElementById("courseList");
        container.innerHTML = "";
        container.className = "course-container";

        allCourses.forEach(course => {
            container.innerHTML += `
                <div class="card">
                    <h3>${course.title}</h3>
                    <p>${course.description}</p>
                    <p style="font-family: var(--font-mono); color: var(--accent-deep); font-weight: 500;">
                        ${course.price ? '₦' + course.price : 'Negotiated (no fixed price)'}
                    </p>
                    <div class="actions">
                        <button class="btn edit" onclick="editCourse(${course.id})">Edit</button>
                        <button class="btn delete" onclick="deleteCourse(${course.id})">Delete</button>
                    </div>
                    <button class="btn btn-ghost" style="width:100%; margin-top:8px;" onclick="toggleSchedule(${course.id})">📅 Manage schedule</button>
                    <div id="schedule-${course.id}" style="display:none; margin-top:12px;"></div>
                </div>
            `;
        });
    }

    window.editCourse = function (id) {
        const course = allCourses.find(c => c.id === id);
        if (!course) return;

        document.getElementById("title").value = course.title;
        document.getElementById("description").value = course.description;
        document.getElementById("price").value = course.price;
        document.getElementById("video_url").value = course.video_url || "";

        document.getElementById("formTitle").innerText = "Edit course";
        editingId = course.id;
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    window.deleteCourse = async function (id) {
        if (!confirm("Delete this course? This can't be undone.")) return;

        await fetch(`/admin/course/${id}`, { method: "DELETE" });
        loadCourses();
    };

    window.toggleSchedule = async function (courseId) {
        const panel = document.getElementById(`schedule-${courseId}`);

        if (panel.style.display === "block") {
            panel.style.display = "none";
            return;
        }

        panel.style.display = "block";
        await loadSlots(courseId);
    };

    async function loadSlots(courseId) {
        const res = await fetch(`/admin/course/${courseId}/slots`);
        const slots = await res.json();

        const panel = document.getElementById(`schedule-${courseId}`);

        let slotsHtml = slots.map(s => `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-top:1px solid var(--line); font-size:0.9rem;">
                <span>${s.day} · ${s.time}</span>
                <button class="btn delete" style="padding:4px 10px; font-size:0.8rem;" onclick="deleteSlot(${s.id}, ${courseId})">Remove</button>
            </div>
        `).join("");

        if (slots.length === 0) {
            slotsHtml = `<p style="font-size:0.9rem; color:var(--slate);">No class times set yet.</p>`;
        }

        panel.innerHTML = `
            <div class="card" style="background:var(--paper);">
                ${slotsHtml}
                <form onsubmit="addSlot(event, ${courseId})" style="margin-top:14px; padding-top:0;">
                    <input type="text" id="day-${courseId}" placeholder="Day (e.g. Monday)" required>
                    <input type="text" id="time-${courseId}" placeholder="Time (e.g. 4:00 PM WAT)" required>
                    <input type="url" id="link-${courseId}" placeholder="Meeting link (Zoom/Meet URL)" required>
                    <button type="submit" class="btn btn-accent" style="width:100%;">Add class time</button>
                </form>
            </div>
        `;
    }

    window.addSlot = async function (event, courseId) {
        event.preventDefault();

        const data = {
            day: document.getElementById(`day-${courseId}`).value,
            time: document.getElementById(`time-${courseId}`).value,
            meeting_link: document.getElementById(`link-${courseId}`).value
        };

        await fetch(`/admin/course/${courseId}/slots`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        loadSlots(courseId);
    };

    window.deleteSlot = async function (slotId, courseId) {
        await fetch(`/admin/slot/${slotId}`, { method: "DELETE" });
        loadSlots(courseId);
    };

    async function loadPayments() {
        const res = await fetch("/admin/payments");
        const payments = await res.json();

        const container = document.getElementById("paymentsList");
        container.innerHTML = "";
        container.className = "course-container";

        payments.forEach(p => {
            container.innerHTML += `
                <div class="card">
                    <h3>${p.student_name}</h3>
                    <p>${p.student_email}</p>
                    <p>Course: ${p.course_title}</p>
                    <p style="color:${p.paid ? 'var(--accent-deep)' : 'var(--danger)'}; font-weight:500;">
                        ${p.paid ? '✓ Paid' : '✗ Unpaid'}
                    </p>
                    ${!p.paid ? `
                        <div class="actions">
                            <button class="btn btn-accent" onclick="generateCode(${p.enrollment_id})">Generate access code</button>
                            <button class="btn edit" onclick="markPaid(${p.enrollment_id})">Mark as paid</button>
                        </div>
                        <p id="code-${p.enrollment_id}" style="font-family:var(--font-mono); font-weight:600; margin-top:8px;"></p>
                    ` : ''}
                </div>
            `;
        });
    }

    window.generateCode = async function (enrollmentId) {
        const res = await fetch(`/admin/enrollment/${enrollmentId}/generate-code`, { method: "POST" });
        const result = await res.json();

        const codeBox = document.getElementById(`code-${enrollmentId}`);
        if (result.code) {
            codeBox.textContent = `Code: ${result.code}`;
        } else {
            codeBox.textContent = result.error || "Something went wrong";
        }
    };

    window.markPaid = async function (enrollmentId) {
        await fetch(`/admin/mark-paid/${enrollmentId}`, { method: "POST" });
        loadPayments();
    };

    async function loadCourseRequests() {
        const res = await fetch("/admin/course-requests");
        const requests = await res.json();

        const container = document.getElementById("requestsList");
        container.innerHTML = "";

        if (requests.length === 0) {
            container.innerHTML = `<p style="color:var(--slate); font-size:0.9rem;">No requests yet.</p>`;
            return;
        }

        container.className = "course-container";

        requests.forEach(r => {
            container.innerHTML += `
                <div class="card">
                    <h3>${r.requested_course}</h3>
                    <p>Parent: ${r.name}</p>
                    <p>Child: ${r.child_name || "N/A"}</p>
                    <p>${r.email} · ${r.phone}</p>
                </div>
            `;
        });
    }

    loadCourses();
    loadPayments();
    loadCourseRequests();
});