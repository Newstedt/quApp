var xhr = null;

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        getDate();
        dataDiv = document.getElementById('result-container');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
}
function getUsers() {
    console.log("Get users...");
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = dataCallback;
    // asynchronous requests
    xhr.open("GET", "http://localhost:6969/users", true);
    // Send the request over the network
    xhr.send(null);
}
function getDate() {
    date = new Date().toString();

    document.getElementById('time-container').textContent
        = date;
}

function sendDataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log("Data creation response received!");
        getDate();
        dataDiv = document.getElementById('sent-data-container');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
}

function sendData() {
    dataToSend = document.getElementById('data-input').value;
    if (!dataToSend) {
        console.log("Data is empty.");
        return;
    }
    console.log("Sending data: " + dataToSend);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = sendDataCallback;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/users", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send(JSON.stringify({"data": dataToSend}));
}

function yieldCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("Yield data received!");
        const jsonResponse = JSON.parse(xhr.responseText);
        const dataAtIndex = Object.values(jsonResponse)[0];
        const data = [{
            x:Object.keys(dataAtIndex),
            y:Object.values(dataAtIndex),
            type:"line",
            orientation:"v",
            marker: {color:"rgba(0,0,255,0.6)"}
            }];
        const layout = {title:"US Treasury Yield"};
        Plotly.newPlot('yield-result-container', data, layout);
    }
}

function plotYields() { 

    console.log("Get yields...");
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = yieldCallback;
    // asynchronous requests
    xhr.open("GET", "http://localhost:6969/ustYields", true);
    // Send the request over the network
    xhr.send(null);
}

function yieldCallbackOnDate() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("Yield data received!");
        const jsonResponse = JSON.parse(xhr.responseText);
        const dataAtIndex = Object.values(jsonResponse)[0];
        const data = [{
            x:Object.keys(dataAtIndex),
            y:Object.values(dataAtIndex),
            type:"line",
            orientation:"v",
            marker: {color:"rgba(0,0,255,0.6)"}
            }];
        const layout = {title:"US Treasury Yield"};
        Plotly.newPlot('yield-on-date-result', data, layout);
    }
}

function plotYieldOnDate() { 

    yieldDate = document.getElementById('yield-date-input').value;
    if (!yieldDate) {
        console.log("Date is empty.");
        return;
    }
    console.log("Fetching yield for date: " + yieldDate);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = yieldCallbackOnDate;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/ustYields", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send(JSON.stringify({"yield date": yieldDate}));
}

(function () {
    getDate();
})();