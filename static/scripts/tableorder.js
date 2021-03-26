/* Ordering of timetable */

function sortTable() {

    if (document.getElementById("timetable20121")) {
        let i, x, y, shouldSwitch;
        const timeTable20121 = document.getElementById("timetable20121");
        switching = true;
        while (switching) {
            let switching = false;
            const rows = timeTable20121.rows;
            for (i = 0; i < (rows.length - 1); i++) {
                shouldSwitch = false;
                x = rows[i].getElementsByTagName("td")[0];
                y = rows[i + 1].getElementsByTagName("td")[0];
                if (x.innerHTML > y.innerHTML) {
                    shouldSwitch = true;
                    break;
                }
            }
            if (shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
            }
        }
    }
    
}

sortTable()
