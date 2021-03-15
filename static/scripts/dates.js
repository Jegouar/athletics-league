/*

if (document.getElementById("match_season").value == "2012") {
    if (document.getElementById("match_weekday").value == "Monday") {
        const dates = [
            "2nd April", "9th April", "16th April", "23rd April", "30th April",
            "7th May", "14th May", "21st May", "28th May",
            "4th June", "11th June", "18th June", "25th June",
            "2nd July", "9th July", "16th July", "23rd July", "30th July",
            "6th August", "13th August", "20th August", "27th August"
        ];
    }
    else if (document.getElementById("match_weekday").value == "Tuesday") {
        const dates = [
            "3rd April", "10th April", "17th April", "24th April",
            "1st May", "8th May", "15th May", "22nd May", "29th May",
            "5th June", "12th June", "19th June", "26th June",
            "3rd July", "10th July", "17th July", "24th July", "31st July",
            "7th August", "14th August", "21st August", "28th August"
        ];
    }
    else if (document.getElementById("match_weekday").value == "Wednesday") {
        const dates = [
            "4th April", "11th April", "18th April", "25th April",
            "2nd May", "9th May", "16th May", "23rd May", "30th May",
            "6th June", "13th June", "20th June", "27th June",
            "4th July", "11th July", "18th July", "25th July",
            "1st August", "8th August", "15th August", "22nd August", "29th August"
        ];
    }
    else if (document.getElementById("match_weekday").value == "Thursday") {
        const dates = [
            "5th April", "12th April", "19th April", "26th April",
            "3rd May", "10th May", "17th May", "24th May", "31st May",
            "7th June", "14th June", "21st June", "28th June",
            "5th July", "12th July", "19th July", "26th July",
            "2nd August", "9th August", "16th August", "23rd August", "30th August"
        ];
    }
    else if (document.getElementById("match_weekday").value == "Friday") {
        const dates = [
            "6th April", "13th April", "20th April", "27th April",
            "4th May", "11th May", "18th May", "25th May",
            "1st June", "8th June", "15th June", "22nd June", "29th June",
            "6th July", "13th July", "20th July", "27th July",
            "3rd August", "10th August", "17th August", "24th August", "31st August"
        ];
    }
    else if (document.getElementById("match_weekday").value == "Saturday") {
        const dates = [
            "7th April", "14th April", "21st April", "28th April",
            "5th May", "12th May", "19th May", "26th May",
            "2nd June", "9th June", "16th June", "23rd June", "30th June",
            "7th July", "14th July", "21st July", "28th July",
            "4th August", "11th August", "18th August", "25th August"
        ];
    }
    else if (document.getElementById("match_weekday").value == "Sunday") {
        const dates = [
            "1st April", "8th April", "15th April", "22nd April", "29th April",
            "6th May", "13th May", "20th May", "27th May",
            "3rd June", "10th June", "17th June", "24th June",
            "1st July", "8th July", "15th July", "22nd July", "29th July",
            "5th August", "12th August", "19th August", "26th August"
        ];
    }
}
*/
function dateList() {
    const dates = [
        "2nd April", "9th April", "16th April", "23rd April", "30th April",
        "7th May", "14th May", "21st May", "28th May",
        "4th June", "11th June", "18th June", "25th June",
        "2nd July", "9th July", "16th July", "23rd July", "30th July",
        "6th August", "13th August", "20th August", "27th August"
    ];

    for (date in dates) {
        let newOption = document.createElement("option");
        newOption.setAttribute("value", date);
        let newTextNode = document.createTextNode(date);
        newOption.appendChild(newTextNode);
        document.getElementById("match_date").appendChild(newOption);
    }
}

dateList();
