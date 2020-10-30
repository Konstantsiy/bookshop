function scrollAppear() {
    var introText = document.querySelector(".intro-text");
    var introPosition = introText.getBoundingClientRect().top;
    var screenPosition = window.innerHeight / 2;

    var introImg = document.querySelector(".intro-img");
    var introImgPos = introImg.getBoundingClientRect().top;
    var screenPositionForImg = window.innerHeight / 0.9;

    var introDesc = document.querySelector(".intro-desc");
    var introDescPos = introDesc.getBoundingClientRect().top;
    var screenPositionForDesc = window.innerHeight / 1.3;

    if(introPosition < screenPosition) {
        introText.classList.add('intro-appear');
    }

    if(introImgPos < screenPositionForImg) {
        introImg.classList.add('intro-appear');
    }

    if(introDescPos < screenPositionForDesc) {
        introDesc.classList.add('intro-appear');
    }
}

window.addEventListener('scroll', scrollAppear);