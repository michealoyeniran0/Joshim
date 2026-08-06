async function loadCourses() {
    const res = await fetch("/courses");
    const courses = await res.json();

    const container = document.getElementById("courseList");
    container.innerHTML = "";

    if (courses.length === 0) {
        container.innerHTML = "<p>No courses available yet — check back soon.</p>";
        return;
    }

    container.className = "course-container";

    courses.forEach(course => {
        container.innerHTML += `
            <div class="card">
                <h3>${course.title}</h3>
                <p>${course.description}</p>
                <p style="font-family: var(--font-mono); color: var(--accent-deep); font-weight: 500;">
                    ${course.price ? '₦' + course.price : 'Contact us for pricing'}
                </p>
                <div class="actions">
                    <button class="btn btn-accent" onclick="enroll(${course.id})">Enroll</button>
                </div>
            </div>
        `;
    });
}

async function enroll(courseId) {
    if (window.isLoggedIn) {
        const res = await fetch("/enroll", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ course_id: courseId })
        });

        const result = await res.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        window.location.href = "/student";
        return;
    }

    window.location.href = `/register-page?course_id=${courseId}`;
}

loadCourses();