console.log("PhishShield started");

window.addEventListener("load", function () {

    const banner = document.createElement("div");

    banner.innerText = "PhishShield checking website...";
    banner.style.position = "fixed";
    banner.style.top = "0";
    banner.style.left = "0";
    banner.style.width = "100%";
    banner.style.padding = "12px";
    banner.style.background = "blue";
    banner.style.color = "white";
    banner.style.textAlign = "center";
    banner.style.zIndex = "999999";

    document.body.prepend(banner);

    fetch("http://127.0.0.1:8000/predict",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            url:window.location.href
        })
    })
    .then(response=>response.json())
    .then(data=>{

        if(data.prediction==="Phishing Website")
        {
            banner.innerText="⚠ Phishing Website Detected";
            banner.style.background="red";
        }
        else
        {
            banner.innerText="✅ Safe Website";
            banner.style.background="green";
        }

        setTimeout(()=>{
            banner.remove();
        },5000);

    })
    .catch(error=>{

        banner.innerText="⚠ API Connection Failed";
        banner.style.background="orange";

        setTimeout(()=>{
            banner.remove();
        },5000);

    });

});