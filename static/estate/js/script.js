function truncateText(elementClass, maxLength) {
    let elements = document.getElementsByClassName(elementClass);
    for (let i = 0; i < elements.length; i++) {
        let element = elements[i];
        let text = element.textContent;

        if (text.length > maxLength) {
            element.textContent = text.substring(0, maxLength - 3) + '...';
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    truncateText('property-description', 100);
});


// getting the property pk
document.addEventListener("DOMContentLoaded", function() {
    let propertyCards = document.querySelectorAll('.property-card');
    propertyCards.forEach(function(card) {
        card.addEventListener('click', function() {
            let pk = card.getAttribute('data-property-pk');
            window.location.href = '/property/' + pk + '/';
        });
    });
});
