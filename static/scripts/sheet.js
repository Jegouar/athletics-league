/* Rotation of sheet */

function sheetRotation() {
    const randomAngle = Math.floor(20 * (Math.random() - 0.5));
    const angledSheet = "rotate(" + randomAngle + "deg)";
    document.querySelector(".sheet").style.transform = angledSheet;
}

sheetRotation()
