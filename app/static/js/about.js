document.addEventListener("DOMContentLoaded", () => {
    const aboutSection = document.querySelector(".about-section");
  
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("show");
          observer.unobserve(entry.target); // فقط یک‌بار اجرا بشه
        }
      });
    }, {
      threshold: 0.3 // وقتی 30٪ دیده شد اجرا بشه
    });
  
    observer.observe(aboutSection);
  });
  