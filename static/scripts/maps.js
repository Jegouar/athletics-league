/* Co-ordinates of participating club venues */
const tilsley = { lat: 51.68851413424184, lng: -1.2844304304305583 };
const horspath = { lat: 51.7375972575029, lng: -1.1871759304287552 };
const palmer = { lat: 51.451455101790785, lng: -0.9376482397139002 };
const swindon = { lat: 51.56697977134897, lng: -1.76940873043505 };
const crookham = { lat: 51.380717539827984, lng: -1.2511990592783035 };
const johnnike = { lat: 51.400788248114885, lng: -0.7499129592775471 };

/* Venue variable for each fixture */
let venue20124 = document.getElementById("20124").previousElementSibling.firstElementChild.innerHTML;
if (venue20124 == "Tilsley Park") {
    venue20124 = tilsley;
}
else if (venue20124 == "Horspath Athletics and Sports Ground") {
    venue20124 = horspath;
}
else if (venue20124 == "Palmer Park Stadium") {
    venue20124 = palmer;
}
else if (venue20124 == "Swindon Athletics Track") {
    venue20124 = swindon;
}
else if (venue20124 == "Crookham Common Athletics Track") {
    venue20124 = crookham;
}
else if (venue20124 == "John Nike Stadium") {
    venue20124 = johnnike;
}

let venue20142 = document.getElementById("20142").previousElementSibling.firstElementChild.innerHTML;
if (venue20142 == "Tilsley Park") {
    venue20142 = tilsley;
}
else if (venue20142 == "Horspath Athletics and Sports Ground") {
    venue20142 = horspath;
}
else if (venue20142 == "Palmer Park Stadium") {
    venue20142 = palmer;
}
else if (venue20142 == "Swindon Athletics Track") {
    venue20142 = swindon;
}
else if (venue20142 == "Crookham Common Athletics Track") {
    venue20142 = crookham;
}
else if (venue20142 == "John Nike Stadium") {
    venue20142 = johnnike;
}

let venue20204 = document.getElementById("20204").previousElementSibling.firstElementChild.innerHTML;
if (venue20204 == "Tilsley Park") {
    venue20204 = tilsley;
}
else if (venue20204 == "Horspath Athletics and Sports Ground") {
    venue20204 = horspath;
}
else if (venue20204 == "Palmer Park Stadium") {
    venue20204 = palmer;
}
else if (venue20204 == "Swindon Athletics Track") {
    venue20204 = swindon;
}
else if (venue20204 == "Crookham Common Athletics Track") {
    venue20204 = crookham;
}
else if (venue20204 == "John Nike Stadium") {
    venue20204 = johnnike;
}

let venue20202 = document.getElementById("20202").previousElementSibling.firstElementChild.innerHTML;
if (venue20202 == "Tilsley Park") {
    venue20202 = tilsley;
}
else if (venue20202 == "Horspath Athletics and Sports Ground") {
    venue20202 = horspath;
}
else if (venue20202 == "Palmer Park Stadium") {
    venue20202 = palmer;
}
else if (venue20202 == "Swindon Athletics Track") {
    venue20202 = swindon;
}
else if (venue20202 == "Crookham Common Athletics Track") {
    venue20202 = crookham;
}
else if (venue20202 == "John Nike Stadium") {
    venue20202 = johnnike;
}

/* Rendering of Google maps and markers */
function initMap() {
    const map20124 = new google.maps.Map(document.getElementById("20124"), {
        zoom: 10, center: venue20124,
    });
    const marker20124 = new google.maps.Marker({
        position: venue20124, map: map20124,
    });
    const map20142 = new google.maps.Map(document.getElementById("20142"), {
        zoom: 10, center: venue20142,
    });
    const marker20142 = new google.maps.Marker({
        position: venue20142, map: map20142,
    });
    const map20204 = new google.maps.Map(document.getElementById("20204"), {
        zoom: 10, center: venue20204,
    });
    const marker20204 = new google.maps.Marker({
        position: venue20204, map: map20204,
    });
    const map20202 = new google.maps.Map(document.getElementById("20202"), {
        zoom: 10, center: venue20202,
    });
    const marker20202 = new google.maps.Marker({
        position: venue20202, map: map20202,
    });
} 