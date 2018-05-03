var map;
var markers = [];
var prev_infoWindow =false;

/*
 initialize the map.
 */
function initMap() {
    var astorPlace = {lat: 40.7128, lng: -74.0060}                   

    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.7128, lng: -74.0060},
        zoom: 14,
        streetViewControl: false,
        styles: [{
            "featureType": "landscape",
            "stylers": [{"hue": "#FFBB00"},
                {"saturation": 43.400000000000006},
                {"lightness": 37.599999999999994}, {"gamma": 1}]
        },
            {
                "featureType": "road.highway", "stylers": [{"hue": "#FFC200"},
                {"saturation": -61.8}, {"lightness": 45.599999999999994},
                {"gamma": 1}]
            },
            {
                "featureType": "road.arterial",
                "stylers": [{"hue": "#FF0300"},
                    {"saturation": -100},
                    {"lightness": 51.19999999999999}, {"gamma": 1}]
            },
            {
                "featureType": "road.local",
                "stylers": [{"hue": "#FF0300"},
                    {"saturation": -100},
                    {"lightness": 52}, {"gamma": 1}]
            },
            {
                "featureType": "water",
                "stylers": [{"hue": "#0078FF"},
                    {"saturation": -13.200000000000003},
                    {"lightness": 2.4000000000000057}, {"gamma": 1}]
            }
            ]
    });
}


function sendData() {
    clearMarkers();
    //console.log("Send data")
    var min_rank = $("#selector").val();
    var max_rank = $("#selector2").val();
    console.log(min_rank)
    console.log(max_rank)
    $.ajax({
        url : 'http://127.0.0.1:8000/request/',
        type: 'POST',
        data:{'min':min_rank,'max':max_rank},
        success : function (data) {
                    var houses = data['res'];
                    for (i = 0; i < houses.length; i++) {
                        var myLat = parseFloat(houses[i]['data']["latitude"]);
                        var myLong = parseFloat(houses[i]['data']["longitude"]);
                        var score = parseFloat(houses[i]['data']["score"]);
                        var price = parseInt(houses[i]['data']["price"])
                        var label = houses[i]['data']["label"]
                        var pos = {lat: myLat, lng: myLong};
                        var name = houses[i]['data']['name'];
                        var url = houses[i]['data']['url']
                        var id = parseInt(houses[i]['data']['cluster'])
                        //console.log(pos)
                        createMarker(name, pos, score, price, url, label, id,map);
                    }
                }
    });
}



function createMarker(name, pos, score, price, url, label, id, map) {
    //console.log('marker')
    var marker = new google.maps.Marker({
        position: pos,
        map: map,
        title: name,
        icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=' + id + '|FE6256|000000'
    });

    //console.log(name)
    var infoWindow = new google.maps.InfoWindow({
        content: '<div id="bodyContent">'+
            '<p><b> Address:'+name+'</b>'+
            '<p><b> Price:'+price+'</b>'+
            '<p><b> Score:'+score+'</b>'+
            '<p><b> Label:'+label+'</b>'+
            '</div>'
    });
    console.log('marker3')
    marker.addListener('mouseover', function() {
        //console.log('marker4')
        if( prev_infoWindow ) {
            prev_infoWindow.close();
        }

        prev_infoWindow = infoWindow;
        infoWindow.open(map, marker);
    });

    marker.addListener('click', function() {
        //console.log('marker5')
        window.location.href = url;
    });

    markers.push(marker);
    //console.log('marker6')
}

/*
 clean markers.
 */
function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);

    }
    markers = [];
}
