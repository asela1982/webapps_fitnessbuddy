function buildPlot() {
    /* data route */
    var url = "/api/data/dashboard";
    Plotly.d3.json(url, function (error, response) {

        var trace1 = response

        var data = [
            {
              x: response.map(data => data.sports),
              y: response.map(data => data.buddies),
              type: 'bar'
            }
          ];
          
          Plotly.newPlot('barPlot', data);
    });
}

function buildMap() {
    var apiKey = "AIzaSyBPtERPD47WmGx7r91ibrHiC_lRpcT99Xo";
    var url = "/api/data/dashboard/map";
    Plotly.d3.json(url, function (error, response) {
  
      if (error) return console.warn(error);
  
      debug = response;
  
      var data = [{
        type: 'scattermapbox',
        lat: response.map(data => data.lat),
        lon: response.map(data => data.lng),
        mode: 'markers',
        marker: {
          color: '#D12D33',
          symbol: 'circle',
          size: 10
        }
      }]
  
      var layout = {
        hovermode: 'closest',
  
        mapbox: {
          style: 'mapbox://styles/mapbox/bright-v9',
          zoom: 1
        },
        margin: {
          l: 0,
          r: 0,
          b: 0,
          t: 0
        },
      }
  
      Plotly.setPlotConfig({
        mapboxAccessToken: 'pk.eyJ1IjoiYXNlbGExOTgyIiwiYSI6ImNqZDNocXRlNTBoMWEyeXFmdWY1NnB2MmIifQ.ziEOjgHun64EAp4W3LlsQg'
      })
  
      Plotly.plot('mapPlot', data, layout)
  
    })
  };
  
function buildPie() {
    /* data route */
    var url = "/api/data/dashboard/pie";
    Plotly.d3.json(url, function (error, response) {

        var trace1 = response

        var data = [
            {
              values: response.map(data => data.Frequency),
              labels: response.map(data => data.sportsBrands),
              type: 'pie'
            }
          ];

          var layout = {
            height: 400,
            width: 500
          };
          
          Plotly.newPlot('piePlot', data,layout);
    });
}

function buildPlotH() {
  /* data route */
  var url = "/api/data/dashboard/barH";
  Plotly.d3.json(url, function (error, response) {

      var trace1 = response

      var data = [
          {
            x: response.map(data => data.Frequency),
            y: response.map(data => data.Gender),
            type: 'bar',
            orientation: 'h'
          }
        ];

        Plotly.newPlot('barHPlot',data);
  });
}


buildPlot();
buildMap();
buildPie();
buildPlotH();



