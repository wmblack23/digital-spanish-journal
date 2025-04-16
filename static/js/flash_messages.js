window.onload = function() {
    var flashMessage = document.getElementById('flash-message');
    if (flashMessage && flashMessage.innerHTML.trim() !== '') {
        alert(flashMessage.innerText); 
    }
}