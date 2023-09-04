Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

getXmlHttpRequestObject = function () { 
  // Create a new XMLHttpRequest object 
xhr = new XMLHttpRequest();

return xhr;
};

window.addEventListener('DOMContentLoaded', event => {
  var ctx = document.getElementById("myAreaChart");
  loadStartPage(ctx)
});

function someNewFunction(element, yieldData) {

  window.myAreaChart = new Chart(element, {
    type: 'line',
    data: {
      labels: yieldData[0]['x'],
      datasets: [{
        label: "Sessions",
        lineTension: 0,
        backgroundColor: "rgba(2,117,216,0.2)",
        borderColor: "rgba(2,117,216,1)",
        pointRadius: 5,
        pointBackgroundColor: "rgba(2,117,216,1)",
        pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: yieldData[0]['y'],
      }],
    },
    options: {
      scales: {
        xAxes: [{
          time: {
            unit: 'date'
          },
          gridLines: {
            display: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
        yAxes: [{
          ticks: {
            min: Math.floor(Math.min(...yieldData[0]['y'])),
            max: Math.ceil(Math.max(...yieldData[0]['y'])),
            maxTicksLimit: 5
          },
          gridLines: {
            color: "rgba(0, 0, 0, .125)",
          }
        }],
      },
      legend: {
        display: false
      }
    }
  });
  
}

function yieldCallback(resource, element) {

  promise = new Promise((resolve, reject) => {
      request = getXmlHttpRequestObject();
      request.addEventListener("readystatechange", () => {
          if (request.readyState === 4 && request.status === 200) {
              console.log("Yield data received!");
              const jsonResponse = JSON.parse(request.responseText);
              const dataAtIndex = Object.values(jsonResponse)[0];
              const data = [{
                  x:Object.keys(dataAtIndex),
                  y:Object.values(dataAtIndex),
                  type:"line",
                  orientation:"v",
                  marker: {color:"rgba(0,0,255,0.6)"}
                  }];
              const layout = {title:"US Treasury Yield"};
              someNewFunction(element, data)
              //Plotly.newPlot('yield-result-container', data, layout);
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

function bondListCallback(resource) {
  promise = new Promise((resolve, reject) => {
      request = getXmlHttpRequestObject();
      request.addEventListener("readystatechange", () => {
          if (request.readyState === 4 && request.status === 200) {
              console.log("Bond data received!");
              const jsonResponse = JSON.parse(request.responseText);
              //let placeholder = document.querySelector("#bond-table-output");
              const datatablesSimple = document.getElementById('datatablesSimple');
              let dataTable = new simpleDatatables.DataTable(datatablesSimple);
              dataTable.insert(simpleDatatables.convertJSON({data: JSON.stringify(jsonResponse)}))
              //placeholder.innerHTML = dataTable;

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

function loadStartPage(element){

  yieldCallback("http://localhost:6969/ustYields", element)
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

function yieldCallbackOnDate() {
  // Check response is ready or not
  
  if (xhr.readyState == 4 && xhr.status == 200) {
      console.log("Yield data received!");
      window.myAreaChart.destroy();
      const jsonResponse = JSON.parse(xhr.responseText);
      const dataAtIndex = Object.values(jsonResponse)[0];
      const data = [{
          x:Object.keys(dataAtIndex),
          y:Object.values(dataAtIndex),
          type:"line",
          orientation:"v",
          marker: {color:"rgba(0,0,255,0.6)"}
          }];
      var el = document.getElementById('myAreaChart')
      someNewFunction(el, data)
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

function destroychart() {
  mychart.destroy();
}