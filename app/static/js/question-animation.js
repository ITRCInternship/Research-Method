document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  
  form.addEventListener('submit', function(e) {
    if (e.submitter) {
      
      const buttonText = e.submitter.textContent.trim();
      const isNext = buttonText === 'بعدی' || buttonText === 'خلاصه';
      
      e.preventDefault();
      
      const container = document.querySelector('.question-container');
      container.style.opacity = '0';
      container.style.transform = isNext ? 'translateX(100px)' : 'translateX(-100px)';
      
      setTimeout(() => {
        
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'direction';
        input.value = isNext ? 'next' : 'prev';
        form.appendChild(input);
        form.submit();
      }, 300);
    }
  });
  
  
  const container = document.querySelector('.question-container');
  setTimeout(() => {
    container.style.opacity = '1';
    container.style.transform = 'translateX(0)';
  }, 100);
});
function adjustContainerHeight() {
  const wrapper = document.querySelector('.question-container-wrapper');
  const container = document.querySelector('.question-container');
  const content = document.querySelector('.cont3');
  
  
  const contentHeight = content.scrollHeight;
  const circleHeight = document.querySelector('.circle').scrollHeight;
  const padding = 40; 
  
  
  const finalHeight = Math.max(contentHeight, circleHeight) + padding;
  
 
  wrapper.style.height = `${finalHeight}px`;
  container.style.minHeight = `${finalHeight}px`;
}


window.addEventListener('load', adjustContainerHeight);
window.addEventListener('resize', adjustContainerHeight);


const observer = new MutationObserver(function(mutations) {
  adjustContainerHeight();
});

observer.observe(document.querySelector('.cont3'), {
  childList: true,
  subtree: true,
  characterData: true
});