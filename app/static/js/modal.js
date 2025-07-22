const lampBtn = document.getElementById('lampBtn');
const lampIcon = document.getElementById('lampIcon');
const helpModal = document.getElementById('helpModal');
const closeModal = document.getElementById('closeModal');

lampBtn.addEventListener('click', () => {
  helpModal.style.display = 'block';
  setTimeout(() => {
    helpModal.classList.add('show');
  }, 10); 
  lampIcon.classList.remove('bi-lightbulb');
  lampIcon.classList.add('bi-lightbulb-fill');
});

closeModal.addEventListener('click', () => {
  helpModal.classList.remove('show');
  setTimeout(() => {
    helpModal.style.display = 'none';
  }, 300); 
  lampIcon.classList.remove('bi-lightbulb-fill');
  lampIcon.classList.add('bi-lightbulb');
});