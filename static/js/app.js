$(document).ready(function () {
  const ctx = document.getElementById('myChart').getContext('2d');
  const currentVal = document.getElementById('currentVal');

  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [{ label: 'CPU' }],
    },
    options: {
      borderWidth: 3,
      borderColor: ['rgba(254,81,81,255)'],
      scales: {
        xAxes: {
          gridLines: {
            color: '#FFFFFF',
          },
        },
        yAxes: {
          gridLines: {
            color: '#FFFFFF',
          },
        },
      },
    },
  });

  function addData(label, data) {
    myChart.data.labels.push(label);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    myChart.update();
  }

  function removeFirstData() {
    myChart.data.labels.splice(0, 1);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 20;
  //connect to the socket server.
  //   var socket = io.connect("http://" + document.domain + ":" + location.port);
  var socket = io.connect();

  //receive details from server
  socket.on('updateSensorData', function (msg) {
    console.log('Received sensorData :: ' + msg.date + ' :: ' + msg.value);

    currentVal.innerText = msg.value.toFixed(2);
    // Show only MAX_DATA_COUNT data
    if (myChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData();
    }
    addData(msg.date, msg.value);
  });
});
