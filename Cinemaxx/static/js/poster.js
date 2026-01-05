
document.addEventListener('DOMContentLoaded', function() {
  const posterSection = document.getElementById('poster');
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('#dots .dot');
  
  if (!slides.length) return; // No slides to animate
  
  let currentSlide = 0;
  const changeInterval = 5000; // 5 seconds between slides
  
  function showSlide(index) {
    // Remove active class from all slides and dots
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));
    
    // Add active class to current slide and dot
    slides[index].classList.add('active');
    dots[index].classList.add('active');
    
    currentSlide = index;
  }
  
  // Auto-advance slides
  function autoAdvance() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  }
  
  // Click handlers for dots
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      showSlide(index);
    });
  });
  
  // Start auto-advance
  setInterval(autoAdvance, changeInterval);
});

