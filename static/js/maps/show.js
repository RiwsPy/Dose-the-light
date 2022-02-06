// var map = L.map('city_map').setView([45.1800301, 5.6992145], 15);
//L.marker([45.1800301, 5.6992145]).addTo(map);

var map = L.map('city_map', {
    zoom: 15,
    center: [45.1800301, 5.6992145],
    timeDimension: true,
    timeDimensionOptions: {
        timeInterval: "2014-09-30/2014-10-30",
        period: "PT1H"
    },
    timeDimensionControl: true,
    timeDimensionControlOptions: {
        timeSliderDragUpdate: true,
        loopButton: true,
        autoPlay: false,
        playerOptions: {
            transitionTime: 1000,
            loop: true
        }
    },
});

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);

var layer_date = 'Mo 00:00';
var gradientLayer = null;
var nb_hour = 0;

function addGeoJSONLayer(layer_date) {
    let request = new Request('/maps/api/' + layer_date, {
        method: 'GET',
        headers: new Headers(),
        })

    fetch(request)
    .then((resp) => resp.json())
    .then((data) => {
        //for (let node of data.features) {
            //L.marker(node.geometry.coordinates).addTo(map);
        //}

        var heatMapData = [];
        data.features.forEach(function(d) {
            heatMapData.push([
                +d.geometry.coordinates[0],
                +d.geometry.coordinates[1],
                +d.properties.conflicts_value/20.0]);
        });

        if (gradientLayer !== null) {
            map.removeLayer(gradientLayer);
        }

        gradientLayer = L.heatLayer(heatMapData, {
            maxZoom: 20,
            radius: 30,
            gradient: {
                0.0: 'violet',
                0.20: 'blue',
                0.40: 'green',
                0.60: 'yellow',
                0.80: 'orange',
                1.0: 'red'}
         });

        gradientLayer.addTo(map);

        if (nb_hour < 24) {
            if (nb_hour <= 9) {
                str_hour = '0' + nb_hour.toString()
            } else {
                str_hour = nb_hour.toString()
            }

            setTimeout(function(){
                addGeoJSONLayer('Mo ' + str_hour + ':00')
            }, 1000);
            nb_hour += 1
        }

      })
};

addGeoJSONLayer(layer_date);


/*
  setTimeout(function() {
    alert("Hi again!");
  }, 1000)
*/
