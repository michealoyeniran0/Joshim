const TUTOR_WHATSAPP="2347063186164";
let studentName="";

async function loadProfileName(){
    const res=await fetch("/profile/data");
    const data=await res.json();
    studentName=data.name||"A student";
}

async function loadMyCourses(){
    await loadProfileName();

    const res=await fetch("/my-courses");

    if(res.status===401){
        window.location.href="/login-page";
        return;
    }

    const courses=await res.json();
    const container=document.getElementById("myCourseList");
    container.innerHTML="";

    if(courses.length===0){
        container.innerHTML="<p>You haven't enrolled in any course yet. <a href='/courses-page'>Browse courses</a></p>";
        return;
    }

    container.className="course-container";

    courses.forEach(course=>{

        const message=encodeURIComponent(
            `Hi! I'm ${studentName}, I need help with my "${course.title}" class on Joshim.`
        );

        const whatsappLink=`https://wa.me/${TUTOR_WHATSAPP}?text=${message}`;

        const whatsappButton=`
        <a href="${whatsappLink}" target="_blank"
        style="display:inline-flex;align-items:center;gap:8px;background:#25D366;color:#fff;text-decoration:none;padding:11px 18px;border-radius:6px;font-size:0.95rem;">
        Contact Tutor
        </a>`;

        let scheduleHtml="";

        if(course.schedule&&course.schedule.length>0){

            scheduleHtml=`
            <div class="schedule-box">
            <h4>Class Schedule</h4>

            ${course.schedule.map(slot=>`

            <div class="schedule-item">

            <p>
            ${slot.day} at ${slot.time}
            </p>

            <a href="${slot.meeting_link}" target="_blank" class="btn btn-accent meet-btn">
            Join Google Meet
            </a>

            </div>

            `).join("")}

            </div>`;
        }

        let actionHtml="";

        if(course.paid){

            actionHtml=`
            <p style="color:green;">✓ Payment confirmed</p>
            ${scheduleHtml}
            ${whatsappButton}
            `;

        }else if(course.price&&course.price>0){

            actionHtml=`
            <button class="btn btn-accent" onclick="payForCourse(${course.id})">
            💳 Pay now — ₦${course.price}
            </button>

            <button class="btn delete" style="width:100%;margin-top:8px;" onclick="cancelEnrollment(${course.id})">
            Remove this course
            </button>
            `;

        }else{

            actionHtml=`
            <p>Have an access code from your tutor? Enter it below.</p>

            <input type="text" id="code-${course.id}" placeholder="Enter access code" style="text-transform:uppercase;">

            <button class="btn btn-accent" style="width:100%;margin-top:8px;" onclick="redeemCode(${course.id})">
            Unlock access
            </button>

            <p id="codeMsg-${course.id}"></p>

            <button class="btn delete" style="width:100%;margin-top:8px;" onclick="cancelEnrollment(${course.id})">
            Remove this course
            </button>`;
        }

        container.innerHTML+=`
        <div class="card">
        <h3>${course.title}</h3>
        <p>${course.description}</p>

        <div class="actions">
        ${actionHtml}
        </div>

        </div>`;
    });
}


async function payForCourse(courseId){

    const res=await fetch("/pay",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":getCSRFToken()
        },
        body:JSON.stringify({course_id:courseId})
    });

    const result=await res.json();

    if(result.error){
        alert(result.error);
        return;
    }

    window.location.href=result.authorization_url;
}


async function redeemCode(courseId){

    const codeInput=document.getElementById(`code-${courseId}`);
    const msgBox=document.getElementById(`codeMsg-${courseId}`);

    const res=await fetch("/redeem-code",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":getCSRFToken()
        },
        body:JSON.stringify({
            course_id:courseId,
            code:codeInput.value
        })
    });

    const result=await res.json();

    if(result.error){
        msgBox.style.color="red";
        msgBox.textContent=result.error;
        return;
    }

    msgBox.style.color="green";
    msgBox.textContent=result.message;

    setTimeout(loadMyCourses,1000);
}


async function cancelEnrollment(courseId){

    if(!confirm("Remove this course from your dashboard?")) return;

    const res=await fetch(`/my-courses/${courseId}`,{
        method:"DELETE",
        headers:{
            "X-CSRFToken":getCSRFToken()
        }
    });

    const result=await res.json();

    if(result.error){
        alert(result.error);
        return;
    }

    loadMyCourses();
}


loadMyCourses();