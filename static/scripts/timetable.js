let currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
    // Function to display the specified tab of the form
    let tabs = document.getElementsByClassName("tab");
    tabs[n].style.display = "block";
    // ...and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("previous").style.display = "none";
    } 
    else {
        document.getElementById("previous").style.display = "inline-block";
    }
    if (n == (tabs.length - 1)) {
        document.getElementById("next").style.display = "none";
    } 
    else {
        document.getElementById("next").style.display = "inline-block";
    }
}

function sequence(n) {
    // Function to figure out which tab to display
    let tabs = document.getElementsByClassName("tab");
    // Hide the current tab:
    tabs[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // if you have reached the end of the form... :
    if (currentTab >= tabs.length) {
        //...the form gets submitted:
        document.getElementById("add_timetable").submit();
        return false;
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
}
