var postal_code = window.location.href.split('/')[4];

var city_center_pos = {
    38170: [45.1800301, 5.6992145],
};


var map = L.map('city_map', {
    zoom: 16,
    minZoom: 15,
    center: city_center_pos[postal_code] || [45.1800301, 5.6992145],
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

function loadBloc(fileName) {
    let request = new Request('http://127.0.0.1:8000/maps/api/file/' + fileName, {
        method: 'GET',
        headers: new Headers(),
        })

    fetch(request)
    .then((resp) => resp.json())
    .then((data) => {
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

if (postal_code) {
    loadBloc(postal_code + '_bloc_eclairage_public.json')
}

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);

function addGeoJSONLayer(map) {
    var geoJSONLayer = L.geoJSON({features: []});
    var soda = L.timeDimension.layer.sodaHeatMap(geoJSONLayer);
    soda.addTo(map);
};

addGeoJSONLayer(map);

days_fr = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']

L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
    _getDisplayDateFormat: function(date){
        return days_fr[date.getDay()] + ' ' + date.getHours() + 'h';
    }
});

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
map.addControl(this.timeDimensionControl);