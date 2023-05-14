const showFormButton = document.getElementById('show-form');
const plusIcon = document.getElementById('plus');
const cUpIcon = document.getElementById('c-up');

showFormButton.addEventListener('click', function() {
  plusIcon.classList.toggle('hidden-element');
  cUpIcon.classList.toggle('hidden-element');
});