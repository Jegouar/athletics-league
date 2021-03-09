const tilsley = { lat: 51.68851413424184, lng: -1.2844304304305583 };
const horspath = { lat: 51.7375972575029, lng: -1.1871759304287552 };
const palmer = { lat: 51.451455101790785, lng: -0.9376482397139002 };
const swindon = { lat: 51.56697977134897, lng: -1.76940873043505 };
const crookham = { lat: 51.380717539827984, lng: -1.2511990592783035 };
const johnnike = { lat: 51.400788248114885, lng: -0.7499129592775471 };

function initMap() {
    if (document.getElementById("venue").textContent == "Tilsley Park") {
        const map20201 = new google.maps.Map(document.getElementById(20201), {
            zoom: 10, center: tilsley,
        });
        const marker20201 = new google.maps.Marker({
            position: tilsley, map: map20201,
        });
    }
    else if (document.getElementById("venue").textContent == "Horspath Athletics and Sports Ground") {
        const map20201 = new google.maps.Map(document.getElementById(20201), {
            zoom: 10, center: horspath,
        });
        const marker20201 = new google.maps.Marker({
            position: horspath, map: map20201,
        });
    }
    else if (document.getElementById("venue").textContent == "Palmer Park Stadium") {
        const map20201 = new google.maps.Map(document.getElementById(20201), {
            zoom: 10, center: palmer,
        });
        const marker20201 = new google.maps.Marker({
            position: palmer, map: map20201,
        });
    }
    else if (document.getElementById("venue").textContent == "Swindon Athletics Track") {
        const map20201 = new google.maps.Map(document.getElementById(20201), {
            zoom: 10, center: swindon,
        });
        const marker20201 = new google.maps.Marker({
            position: swindon, map: map20201,
        });
    }
    else if (document.getElementById("venue").textContent == "Crookham Common Athletics Track") {
        const map20201 = new google.maps.Map(document.getElementById(20201), {
            zoom: 10, center: crookham,
        });
        const marker20201 = new google.maps.Marker({
            position: crookham, map: map20201,
        });
    }
    else if (document.getElementById("venue").textContent == "John Nike Stadium") {
        const map20201 = new google.maps.Map(document.getElementById(20201), {
            zoom: 10, center: johnnike,
        });
        const marker20201 = new google.maps.Marker({
            position: johnnike, map: map20201,
        });
    }
}
    