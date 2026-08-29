async function loadCourse(){

    const res = await fetch(`/course/${courseId}`);

    const data = await res.json();


    if(data.error){

        document.getElementById("scheduleList").innerHTML =
        `<p>${data.error}</p>`;

        return;
    }


    document.getElementById("courseTitle").textContent =
    data.course.title;


    document.getElementById("courseDescription").textContent =
    data.course.description;


    const container =
    document.getElementById("scheduleList");


    container.innerHTML = "";


    if(data.schedule.length === 0){

        container.innerHTML =
        "<p>Your tutor has not added a class schedule yet.</p>";

        return;
    }


    data.schedule.forEach(slot => {

        container.innerHTML += `

        <div class="card">

            <h3>
                ${slot.day}
            </h3>

            <p style="color:var(--slate);">
                ${slot.time}
            </p>


            ${
                slot.meeting_link
                ?
                `
                <a 
                href="${slot.meeting_link}" 
                target="_blank"
                class="btn btn-accent">
                    Join Google Meet
                </a>
                `
                :
                `
                <p>
                    Meeting link not available yet.
                </p>
                `
            }


        </div>

        `;

    });

}


loadCourse();