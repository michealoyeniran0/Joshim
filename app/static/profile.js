async function loadProfile(){

const res=await fetch("/profile/data");
const data=await res.json();

document.getElementById("profileName").textContent=data.name;
document.getElementById("profileEmail").textContent=data.email;

document.getElementById("profilePhone").value=data.phone||"";
document.getElementById("childName").value=data.child_name||"";
document.getElementById("childClass").value=data.child_class_level||"";

if(data.profile_image){
document.getElementById("profileImg").src="/static/"+data.profile_image;
}

}


document.getElementById("saveProfile").onclick=async()=>{

const res=await fetch("/profile/update",{

method:"POST",

headers:{
"Content-Type":"application/json",
"X-CSRFToken":getCSRFToken()
},

body:JSON.stringify({

phone:document.getElementById("profilePhone").value,

child_name:document.getElementById("childName").value,

child_class_level:document.getElementById("childClass").value

})

});


const data=await res.json();

document.getElementById("profileResponse").textContent=data.message;

};



document.getElementById("uploadForm").addEventListener("submit",async(e)=>{

e.preventDefault();

const file=document.getElementById("photoInput").files[0];

if(!file){
return;
}

const formData=new FormData();

formData.append("photo",file);


const res=await fetch("/profile/upload",{

method:"POST",

headers:{
"X-CSRFToken":getCSRFToken()
},

body:formData

});


const data=await res.json();

if(data.profile_image){
document.getElementById("profileImg").src="/static/"+data.profile_image;
}

document.getElementById("uploadResponse").textContent="Profile picture updated";

});


loadProfile();
document.getElementById("changePassword").onclick=async()=>{

const res=await fetch("/profile/change-password",{

method:"POST",

headers:{
"Content-Type":"application/json",
"X-CSRFToken":getCSRFToken()
},

body:JSON.stringify({

old_password:document.getElementById("oldPassword").value,

new_password:document.getElementById("newPassword").value

})

});


const data=await res.json();

const box=document.getElementById("passwordResponse");


if(data.error){

box.textContent=data.error;
box.style.color="red";

return;

}


box.textContent=data.message;
box.style.color="green";


};