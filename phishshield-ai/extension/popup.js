document.getElementById("check").addEventListener("click", async () => {

    let tabs = await chrome.tabs.query({active:true,currentWindow:true});
    let url = tabs[0].url;

    try {

        const response = await fetch("http://127.0.0.1:8000/predict", {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({url:url})
        });

        const data = await response.json();

        document.getElementById("result").innerText =
            "Prediction: " + data.prediction;

    } catch(error) {

        document.getElementById("result").innerText =
            "API Connection Failed";

    }

});
