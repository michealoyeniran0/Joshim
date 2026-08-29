async function loadNavProfile(){

const res = await fetch("/profile/data");

const data = await res.json();

if(data.profile_image){

document.getElementById("navProfileImg").src="/static/"+data.profile_image;

}

}

loadNavProfile();