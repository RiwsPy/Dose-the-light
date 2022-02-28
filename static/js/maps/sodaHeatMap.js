var intervalInMlsec = 60*60*1000;
var timeStart = 1675645200000;

L.TimeDimension.Layer.SODAHeatMap = L.TimeDimension.Layer.extend({
    _onNewTimeLoading: function(ev) {
        this._currentLoadedTime = ev.time;
        if (this.isCurrentLayerTime(ev.time) || this.isNextLayerTime(ev.time)) {
            this._getDataForTime(ev.time);
        }
    },

    isNextLayerTime: function(time) {
        return (time == this._timeDimension.getCurrentTime() + intervalInMlsec)
    },

    isReady: function(time) {
        return true;
        //return (this._currentLoadedTime == time);
    },

    isCurrentLayerTime(time) {
        return (time == this._timeDimension.getCurrentTime());
    },

    _update: function(heatMapData) {
        if (this._timeDimension.getCurrentTime() == this._currentLayerTime) {
            return;
        }

        let new_layer = L.heatLayer(heatMapData, {
            maxZoom: 17,
            radius: 30,
            max: 1.0,
            blur: 20,
            gradient: {
                0.0: 'violet',
                0.20: 'blue',
                0.40: 'green',
                0.60: 'yellow',
                0.80: 'orange',
                1.0: 'red'}
         });

        if (this._currentLayer !== null) {
            map.removeLayer(this._currentLayer);
        }
        this._currentLayer = new_layer
        this._currentLayerTime = this._timeDimension.getCurrentTime()

        L.TimeDimension.Layer
            this._currentLayer.addTo(map);
        //this._getDataForTime(this._currentLayerTime + intervalInMlsec);
    },

    onAdd: function(map) {
        this._map = map;
        if (!this._timeDimension && map.timeDimension) {
            this._timeDimension = map.timeDimension;
        }
        this._timeDimension.on("timeloading", this._onNewTimeLoading, this);
        //this._timeDimension.on("timeload", this._update, this);
        this._timeDimension.registerSyncedLayer(this);
        this._getDataForTime(timeStart);
    },

    _getDataForTime: function(time) {
        this._layersData = this._layersData || {}
        this._layersIsRequested = this._layersIsRequested || {}

        if (this._layersData[time]) {
            if (this.isNextLayerTime(time)) {
                this._update(this._layersData[time]);
            }
            return;
        }
        if (this._layersIsRequested[time]) {
            return;
        }
        this._layersIsRequested[time] = true;

        let request = new Request('/maps/api/date/' + (time - timeStart + intervalInMlsec), {
            method: 'GET',
            headers: new Headers(),
            })

        fetch(request)
        .then((resp) => resp.json())
        .then((data) => {
            var heatMapData = [];
            data.features.forEach(function(d) {
                heatMapData.push([
                    +d.geometry.coordinates[1],
                    +d.geometry.coordinates[0],
                    Math.min(+d.properties.conflicts_value/30.0, 1.0)]);
            });

            this._layersData[time] = heatMapData;
            if (this.isCurrentLayerTime(time) || this.isNextLayerTime(time)) {
                this._update(heatMapData);
            }
       })
    }
})

L.timeDimension.layer.sodaHeatMap = function(options) {
    return new L.TimeDimension.Layer.SODAHeatMap(options);
};