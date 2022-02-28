var map = L.map('city_map', {
    zoom: 16,
    minZoom: 15,
    center: [45.1800301, 5.6992145],
    timeDimension: true,
    timeDimensionOptions: {
        timeInterval: "2023-02-06/P7D",
        period: "PT1H",
    }
});

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
    let request = new Request('api/' + fileName, {
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

loadBloc('seyssinet_pariset_bloc__clairage_public.json')

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
