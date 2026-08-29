function updateClock(){

const options={
hour:"2-digit",
minute:"2-digit",
hour12:true
};


const nigeria=document.getElementById("nigeria-time");
const uk=document.getElementById("uk-time");
const usa=document.getElementById("usa-time");


if(nigeria){

nigeria.textContent=
new Date().toLocaleTimeString(
"en-US",
{
...options,
timeZone:"Africa/Lagos"
}
);

}


if(uk){

uk.textContent=
new Date().toLocaleTimeString(
"en-US",
{
...options,
timeZone:"Europe/London"
}
);

}


if(usa){

usa.textContent=
new Date().toLocaleTimeString(
"en-US",
{
...options,
timeZone:"America/New_York"
}
);

}

}


updateClock();

setInterval(updateClock,1000);