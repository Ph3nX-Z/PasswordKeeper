const closeNavMenuButton = document.querySelector(".closeNavButton");
const nav = document.querySelector(".navMenu");
const openNavMenu = document.querySelector(".openNavMenu");
var isNavMenuOpened = false;
const ContentDiv = document.querySelector(".content");
const PasswordsDiv = document.querySelector(".passwords-div");
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
    console.log(ContentDiv.childElementCount);
    if (ContentDiv.childElementCount === 0) {
        console.log("position relative");
        hintText.classList.add("hint-relative");
        hintText.classList.remove("hint-absolute");
        PasswordsDiv.style.height = "200px";
    } else {
        console.log("position absolute");
        hintText.classList.add('hint-absolute');
        hintText.classList.remove("hint-relative");
        PasswordsDiv.style.height = "fit-content";
    }
});