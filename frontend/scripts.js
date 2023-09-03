var xhr = null;

getXmlHttpRequestObject = function () {
    
        // Create a new XMLHttpRequest object 
    xhr = new XMLHttpRequest();
    
    return xhr;
};

function getDate() {
    date = new Date().toString();

    document.getElementById('time-container').textContent
        = date;
}

function yieldCallback(resource) {

    promise = new Promise((resolve, reject) => {
        request = getXmlHttpRequestObject();
        request.addEventListener("readystatechange", () => {
            if (request.readyState === 4 && request.status === 200) {
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
                resolve(jsonResponse);
            } else if (request.readyState === 4) {
                reject("error getting resources");
            }
        });
        request.open("GET", resource, true);
        request.send(null);
    });
    return promise
}

function plotYields() { 

    console.log("Get yields...");
    yieldCallback("http://localhost:6969/ustYields")
        .then((data) => {
            console.log("promise resolved", data);
        })
        .catch((err) => {
            console.log("promise rejected", err);
        });
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
        Plotly.newPlot('yield-result-container', data, layout);
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

function bondListCallback(resource) {
    promise = new Promise((resolve, reject) => {
        request = getXmlHttpRequestObject();
        request.addEventListener("readystatechange", () => {
            if (request.readyState === 4 && request.status === 200) {
                console.log("Bond data received!");
                const jsonResponse = JSON.parse(xhr.responseText);
                let placeholder = document.querySelector("#bond-table-output");
                let out = "";
                for(let row of jsonResponse){
                    out += `
                        <tr>
                            <td>'${row.cusip}'</td>
                            <td>'${row.issueDate}'</td>
                            <td>'${row.securityType}'</td>
                            <td>'${row.interestRate}'</td>
                            <td>'${row.maturityDate}'</td>
                            <td>'${row.interestPaymentFrequency}'</td>
                        </tr>
                    `;
                }
                placeholder.innerHTML = out;
                resolve(jsonResponse);
            } else if (request.readyState === 4) {
                reject("error getting resources");
            }
        });
        request.open("GET", resource, true);
        request.send(null);
    });
    return promise 
}

function cashflowCallback(resource, input_cusip) {
    promise = new Promise((resolve, reject) => {
        request = getXmlHttpRequestObject();
        request.addEventListener("readystatechange", () => {
            if (request.readyState === 4 && request.status === 200) {
                console.log("Cashflow data received!");
                const jsonResponse = JSON.parse(request.responseText);
                priceVal = document.getElementById('theo-price-container');
                // Set current data text
                priceVal.innerHTML = jsonResponse[0]['theoPrice']
                let placeholder = document.querySelector("#cashflow-table-output");
                let out = "";
                isFirst = true;
                for(const row in jsonResponse){
                    if (isFirst) { 
                        isFirst = false; 
                        continue; // Skip the price element
                    }
                    out += `
                        <tr>
                            <td>'${jsonResponse[row]['date']}'</td>
                            <td>'${jsonResponse[row]['days_to']}'</td>
                            <td>'${jsonResponse[row]['cashflow']}'</td>
                            <td>'${jsonResponse[row]['disc_cashflows']}'</td>
                            <td>'${jsonResponse[row]['discount_factor']}'</td>
                        </tr>
                    `;
                }
                
                placeholder.innerHTML = out;
                resolve(jsonResponse);
            } else if (request.readyState === 4) {
                reject("error getting resources");
            }
        });
        request.open("POST", resource, true);
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        // Send the request over the network
        request.send(JSON.stringify({"bond cusip": input_cusip}));
    });
    return promise 
}

function getBondCashflows() {
    bondCusip = document.getElementById('cusip-input').value;
    if (!bondCusip) {
        console.log("Bond cusip is empty.");
        return;
    }
    console.log("Calculate bond cashflows...");
    cashflowCallback("http://localhost:6969/bondCashflows", bondCusip)
        .then((data) => {
            console.log("promise resolved", data);
        })
        .catch((err) => {
            console.log("promise rejected", err);
    });
}
/*
function getBondTheoPrice() {
    bondCusip = document.getElementById('cusip-input').value;
    if (!bondCusip) {
        console.log("Bond cusip is empty.");
        return;
    }
    console.log("Calculate bond cashflows...");
    cashflowCallback("http://localhost:6969/bondCashflows", bondCusip)
        .then(() => {
            console.log("Yield curve resolved");
            return bondTheoPrice("http://localhost:6969/ustCusips");
        })
        .then(() => {
            console.log("Bond list resolved");
        })
        .catch((err) => {
            console.log("promise rejected", err);
        });
} */

function getBondList() { 

    console.log("Get bond list...");
    bondListCallback("http://localhost:6969/ustCusips")
        .then((data) => {
            console.log("promise resolved", data);
        })
        .catch((err) => {
            console.log("promise rejected", err);
    });
}

function loadStartPage(){

    yieldCallback("http://localhost:6969/ustYields")
        .then(() => {
            console.log("Yield curve resolved");
            return bondListCallback("http://localhost:6969/ustCusips");
        })
        .then(() => {
            console.log("Bond list resolved");
        })
        .catch((err) => {
            console.log("promise rejected", err);
        }); 
}

 
(function () {
    getDate();
})();