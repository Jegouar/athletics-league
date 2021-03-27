/* Look for any elements with the class "custom-select": */
let customSelect = document.getElementsByClassName("custom-select");
for (let i = 0; i < customSelect.length; i++) {
    let selectElement = customSelect[i].getElementsByTagName("select")[0];
    /* For each element, create a new DIV that will act as the selected item: */
    let selectedItemDiv = document.createElement("div");
    selectedItemDiv.setAttribute("class", "select-selected");
    selectedItemDiv.innerHTML = selectElement.options[selectElement.selectedIndex].innerHTML;
    customSelect[i].appendChild(selectedItemDiv);
    /* For each element, create a new DIV that will contain the option list: */
    let optionListDiv = document.createElement("div");
    optionListDiv.setAttribute("class", "select-items select-hide");
    for (let j = 1; j < selectElement.length; j++) {
        /* For each option in the original select element,
        create a new DIV that will act as an option item: */
        let optionItemDiv = document.createElement("div");
        optionItemDiv.innerHTML = selectElement.options[j].innerHTML;
        optionItemDiv.addEventListener("click", function(e) {
            /* When an item is clicked, update the original select box and the selected item: */
            let selectBox = this.parentNode.parentNode.getElementsByTagName("select")[0];
            let selectedItem = this.parentNode.previousSibling;
            for (let i = 0; i < selectBox.length; i++) {
                if (selectBox.options[i].innerHTML == this.innerHTML) {
                    selectBox.selectedIndex = i;
                    selectedItem.innerHTML = this.innerHTML;
                    let sameAsSelected = this.parentNode.getElementsByClassName("same-as-selected");
                    for (let k = 0; k < sameAsSelected.length; k++) {
                        sameAsSelected[k].removeAttribute("class");
                    }
                    this.setAttribute("class", "same-as-selected");
                    break;
                }
            }
            selectedItem.click();
        });
        optionListDiv.appendChild(optionItemDiv);
    }
    customSelect[i].appendChild(optionListDiv);
    selectedItemDiv.addEventListener("click", function(e) {
        /* When the select box is clicked, close any other select boxes,
        and open/close the current select box: */
        e.stopPropagation();
        closeAllSelect(this);
        this.nextSibling.classList.toggle("select-hide");
        this.classList.toggle("select-arrow-active");
    });
}

function closeAllSelect(element) {
    /* A function that will close all select boxes in the document,
    except the current select box: */
    let arrNo = [];
    let selectItems = document.getElementsByClassName("select-items");
    let selectSelected = document.getElementsByClassName("select-selected");
    for (let i = 0; i < selectSelected.length; i++) {
        if (element == selectSelected[i]) {
            arrNo.push(i);
        } 
        else {
            selectSelected[i].classList.remove("select-arrow-active");
        }
    }
    for (let i = 0; i < selectItems.length; i++) {
        if (arrNo.indexOf(i)) {
            selectItems[i].classList.add("select-hide");
        }
    }
}

/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect);