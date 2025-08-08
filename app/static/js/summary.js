document.addEventListener("DOMContentLoaded", () => {
    const summaryContainer = document.querySelector(".summary-container");
    
    
    summaryContainer.classList.add("hidden");
  
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("show");
          observer.unobserve(entry.target); 
        }
      });
    }, {
      threshold: 0.3
    });
  
    observer.observe(summaryContainer);
  });