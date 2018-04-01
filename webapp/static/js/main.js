/**
 * Created by AUCHLY1 on 3/31/18.
 */

//Toggle menu visibility
function toggleMenu() {
    var menu = document.getElementById("dropdown");
    if (menu.style.display == 'block') {
        menu.style.display = 'none';
    }
    else {
        menu.style.display = 'block';
    }
}
