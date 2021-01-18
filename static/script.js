const closeNavMenuButton = document.querySelector(".closeNavButton");
const nav = document.querySelector(".navMenu");
const openNavMenu = document.querySelector(".openNavMenu");
var isNavMenuOpened = false;
const passwordsDiv = document.querySelector(".content");
const hintText = document.querySelector(".hint")

openNavMenu.addEventListener("click",function(){
        nav.classList.toggle("nav-menu-shown");
        closeNavMenuButton.classList.toggle("close-nav-button-shown");
        isNavMenuOpened = true;
});
closeNavMenuButton.addEventListener("click",function(){
    nav.classList.toggle("nav-menu-shown");
    closeNavMenuButton.classList.toggle("close-nav-button-shown");
    isNavMenuOpened = false;
});
addEventListener("scroll",function(){
    if (isNavMenuOpened === true) {
        nav.classList.toggle("nav-menu-shown");
        closeNavMenuButton.classList.toggle("close-nav-button-shown");
        isNavMenuOpened = false;
    }
});

addEventListener("load",function(){
    if (passwordsDiv.childElementCount === 0) {
        hintText.classList.add("hint-relative");
        hintText.classList.remove("hint-absolute");
        passwordsDiv.style.height = "200px";
    } else {
        hintText.classList.add('hint-absolute');
        hintText.classList.remove("hint-relative");
        passwordsDiv.style.height = "fit-content";
    }
});