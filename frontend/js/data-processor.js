Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

getXmlHttpRequestObject = function () {
  // Create a new XMLHttpRequest object 
xhr = new XMLHttpRequest();

return xhr;
};

// Add event listener to table
const el = document.getElementById("cusip-input");
el.addEventListener("click", getBondCashflows, false);

function cashflowCallback(resource, input_cusip) {
  promise = new Promise((resolve, reject) => {
      request = getXmlHttpRequestObject();
      request.addEventListener("readystatechange", () => {
          if (request.readyState === 4 && request.status === 200) {
              console.log("Cashflow data received!");
              const jsonResponse = JSON.parse(request.responseText);
              priceVal = document.getElementById('theo-price-container');
              // Set current data text
              priceVal.innerHTML = 'Theoretical price: '.concat(jsonResponse['theoPrice'])
              let placeholder = document.getElementById("cashflow-table");
              let out = "";
              let onlyCfJson = [];
              for(const row in jsonResponse){
                  if (row == 'theoPrice') {  
                      continue; // Skip the price element
                  }
                  onlyCfJson.push(jsonResponse[row]);
              }
              
              const cashflowSimple = document.getElementById('cashflow-table');
              let dataTable = new simpleDatatables.DataTable(cashflowSimple);
              dataTable.insert(simpleDatatables.convertJSON({data: JSON.stringify(onlyCfJson)}))

              //placeholder.innerHTML = out;
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

