var days_fr = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];

L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
    _getDisplayDateFormat: function(date){
        return days_fr[date.getDay()] + ' ' + date.getHours() + 'h';
    }
});

let urlParams = new URL(window.location.href).searchParams;
var postal_code = urlParams.get('postal_code');
var city_center = [parseFloat(urlParams.get('lat')), parseFloat(urlParams.get('lon'))];
console.log(city_center);

var map = L.map('city_map', {
    zoom: 15,
    maxZoom: 17,
    minZoom: 15,
    center: city_center,
    timeDimension: true,
    timeDimensionOptions: {
        timeInterval: "2023-02-06/P7D",
        period: "PT1H",
    }
});

// Active control buttons
map.addControl(new L.Control.Fullscreen({
    title: {
        'false': 'Vue plein écran',
        'true': 'Quitter le plein écran'
    }
}));

var legendData = {
    white:  "tout va bien",
    violet: "0 < I < 0.2",
    blue:   "0.2 < I < 0.4",
    green:  "0.4 <= I < 0.6",
    yellow: "0.6 <= I < 0.8",
    orange: "0.8 <= I < 1",
    red:    "I >= 1",
};

// Active legend
var legend = L.control({ position: "bottomright" });

legend.onAdd = function(map) {
    var div = L.DomUtil.create("div", "legend");
    div.innerHTML += "<h4>Intensité (I)</h4>"
    for (let [color, txt] of Object.entries(legendData)) {
        div.innerHTML += '<i style="background: ' + color + '"></i><span>' + txt + '</span><br>'
    }
    return div;
};
legend.addTo(this.map);

if (postal_code) {
    loadBloc(map, postal_code + '_bloc_eclairage_public.json')
}

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);

addGeoJSONLayer(map);

var timeDimensionControl = new L.Control.TimeDimensionCustom(
    {
        timeSliderDragUpdate: true,
        position: 'bottomleft',
        loopButton: false,
        autoPlay: false,
        minSpeed: 0.1,
        maxSpeed: 1,
        playerOptions: {
            loop: true
        }
    }
);
map.addControl(timeDimensionControl);


var colorNameToRGB = {
    Yellow: '#FFFF00',
    Lime: '#00FF00',
    DarkOliveGreen: '#556B2F',
    LimeGreen: '#32CD32',
    DarkGreen: '#006400',
    DarkOrange: '#FF8C00',
    Blue: '#0000FF',
    Magenta: '#FF00FF',
    Cyan: '#00FFFF',
    Green: '#00FF00',
    SandyBrown: '#F4A460',
    Fuchsia: '#FD3F92',
    Salmon: '#FA8072',
    DeepSkyBlue: '#00BFFF',
    Red: '#FF0000',
    YellowGreen: '#9ACD32',
    Chocolate: '#84563C',
    LawnGreen: '#7CFC00',
}

function loadBloc(map, fileName) {
    let request = new Request('http://127.0.0.1:8000/maps/api/file/' + fileName, {
        method: 'GET',
        headers: new Headers(),
        })

    fetch(request)
    .then((resp) => resp.json())
    .then((data) => {
        if (data.features.length == 0) {
            return;
        }

        let blocLayer = new L.FeatureGroup();
        L.geoJSON(data, {
            style: function (feature) {
                return {color: colorNameToRGB[(feature.properties._umap_options || {color: 'Red'}).color],
                        weight: 7,
                        opacity: 0.3};
        }}).addTo(blocLayer);
        L.control.layers(null, {
            "Bloc luminaires": blocLayer,
        }).addTo(map);
    });
}

function addGeoJSONLayer(map) {
    let geoJSONLayer = L.geoJSON({features: []});
    let soda = L.timeDimension.layer.sodaHeatMap(geoJSONLayer);
    soda.addTo(map);
};
