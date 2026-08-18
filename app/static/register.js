const urlParams = new URLSearchParams(window.location.search);
const courseIdFromUrl = urlParams.get("course_id");


async function loadCourseOptions() {
    const res = await fetch("/courses");
    const courses = await res.json();

    const select = document.getElementById("courseSelect");
    select.innerHTML = '<option value="">Select a course</option>';

    courses.forEach(course => {
        const option = document.createElement("option");
        option.value = course.id;
        option.textContent = course.title;

        if (courseIdFromUrl && parseInt(courseIdFromUrl) === course.id) {
            option.selected = true;
        }

        select.appendChild(option);
    });

    const otherOption = document.createElement("option");
    otherOption.value = "other";
    otherOption.textContent = "Other (not listed yet)";
    select.appendChild(otherOption);


    select.addEventListener("change", () => {
        const otherWrap = document.getElementById("otherCourseWrap");
        const otherInput = document.getElementById("otherCourse");
        const descBox = document.getElementById("courseDescription");

        if (select.value === "other") {
            otherWrap.style.display = "block";
            otherInput.required = true;
            descBox.textContent = "";
        } else {
            otherWrap.style.display = "none";
            otherInput.required = false;

            const selected = courses.find(
                c => c.id === parseInt(select.value)
            );

            descBox.textContent = selected ? selected.description : "";
        }
    });
}


loadCourseOptions();


const form = document.getElementById("registerForm");


form.addEventListener("submit", async (e) => {
    e.preventDefault();


    const courseValue = document.getElementById("courseSelect").value;
    const isOther = courseValue === "other";


    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        password: document.getElementById("password").value,
        child_name: document.getElementById("childName").value,
        child_class_level: document.getElementById("childClassLevel").value,
        course_id: isOther ? null : parseInt(courseValue),
        requested_course: isOther
            ? document.getElementById("otherCourse").value
            : null
    };


    const res = await fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(data)
    });


    const result = await res.json();

    document.getElementById("response").innerText =
        result.message || result.error;


    if (res.status === 200) {
        window.location.href = "/student";
    }
});