window.onscroll = function() {
    const navbar = document.getElementById('navbar');

    if (window.scrollY > 50) {  // If scrolled down 50px or more
        navbar.classList.add('white');  // Add class to invert colors
    } else {
        navbar.classList.remove('white');  // Remove class to revert colors
    }
};
