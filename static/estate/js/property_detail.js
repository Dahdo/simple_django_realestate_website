document.addEventListener("DOMContentLoaded", function() {
    const imageSlider = document.getElementById('imageSlider');
    const images = imageSlider.querySelectorAll('img');
    let currentIndex = 0;

    function showImage(index) {
        images.forEach((image, i) => {
            image.style.display = i === index ? 'block' : 'none';
        });
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        showImage(currentIndex);
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        showImage(currentIndex);
    }

    // Add event listeners for next and previous buttons
    const nextButton = document.getElementById('nextButton');
    const prevButton = document.getElementById('prevButton');

    nextButton.addEventListener('click', nextImage);
    prevButton.addEventListener('click', prevImage);

    // Initially show the first image
    showImage(currentIndex);
});
