function load_gapanapa(panaText) {
             gapaNapa = L.tileLayer.wms('http://110.34.30.197:8080/geoserver/ows',{
                    layers:'Nepal:pactionAction',
                        format:'image/png',
                        CQL_FILTER: panaText,
                        transparent: true
                }).addTo(map);
            };

function set_panaText(mytext) {
    panaText = "gn='" + mytext + "'";
    console.log(panaText);

    //Remove old schools to prevent "a new point is added but the old one is not removed"
    //check if map has schools layer
    if (map.hasLayer(gapaNapa)) {
            map.removeLayer(gapaNapa);
            //if so, remove previously added schools layer before loading schools with new cql filter
    }
    ;

    load_gapanapa(panaText);
}

