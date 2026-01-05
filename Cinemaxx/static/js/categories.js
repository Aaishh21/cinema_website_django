document.addEventListener('DOMContentLoaded', function() {
  const categoriesContainer = document.querySelector('.categories-container');
  const rightArrow = document.querySelectorAll('.arrow-btn')[1];
  const leftArrow = document.querySelectorAll('.arrow-btn')[0];
  const dots = document.querySelectorAll('.dot');

  // Get all category cards and split into pages (5 per page)
  const categoryCards = Array.from(document.querySelectorAll('.category-card'));
  const cardsPerPage = 5;
  const totalPages = Math.ceil(categoryCards.length / cardsPerPage);

  let currentPage = 0;
  let touchStartX = 0;
  let touchEndX = 0;

  function showPage(pageIndex) {
    // Calculate the translation distance
    // Each item width (200px) + gap (60px) = 260px per item
    const itemWidth = 200;
    const gap = 60;
    const itemTotalWidth = itemWidth + gap;
    const translateDistance = (pageIndex * cardsPerPage) * itemTotalWidth;
    
    // Apply smooth slide animation
    categoriesContainer.style.transform = `translateX(-${translateDistance}px)`;
    
    // Update active dot
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === pageIndex);
    });
    
    // Update arrow button states
    leftArrow.disabled = pageIndex === 0;
    rightArrow.disabled = pageIndex === totalPages - 1;
    
    leftArrow.style.opacity = pageIndex === 0 ? '0.5' : '1';
    rightArrow.style.opacity = pageIndex === totalPages - 1 ? '0.5' : '1';
    leftArrow.style.cursor = pageIndex === 0 ? 'not-allowed' : 'pointer';
    rightArrow.style.cursor = pageIndex === totalPages - 1 ? 'not-allowed' : 'pointer';
  }

  rightArrow.addEventListener('click', () => {
    if (currentPage < totalPages - 1) {
      currentPage++;
      showPage(currentPage);
    }
  });

  leftArrow.addEventListener('click', () => {
    if (currentPage > 0) {
      currentPage--;
      showPage(currentPage);
    }
  });

  // Dot click handlers
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      if (index < totalPages) {
        currentPage = index;
        showPage(currentPage);
      }
    });
  });

  // Touch/Swipe handlers
  categoriesContainer.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, false);

  categoriesContainer.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, false);

  function handleSwipe() {
    const swipeThreshold = 50; // Minimum distance to be considered a swipe
    const diff = touchStartX - touchEndX;

    if (Math.abs(diff) > swipeThreshold) {
      if (diff > 0) {
        // Swiped left - show next page
        if (currentPage < totalPages - 1) {
          currentPage++;
          showPage(currentPage);
        }
      } else {
        // Swiped right - show previous page
        if (currentPage > 0) {
          currentPage--;
          showPage(currentPage);
        }
      }
    }
  }

  // Mouse wheel/trackpad support
  categoriesContainer.addEventListener('wheel', (e) => {
    if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
      // Horizontal scroll detected (trackpad slide)
      e.preventDefault();
      
      if (e.deltaX > 0) {
        // Scrolling right - show next page
        if (currentPage < totalPages - 1) {
          currentPage++;
          showPage(currentPage);
        }
      } else {
        // Scrolling left - show previous page
        if (currentPage > 0) {
          currentPage--;
          showPage(currentPage);
        }
      }
    }
  }, { passive: false });

  // Pointer drag support for trackpad
  let pointerStartX = 0;
  let isPointerDown = false;

  categoriesContainer.addEventListener('pointerdown', (e) => {
    isPointerDown = true;
    pointerStartX = e.clientX;
  });

  categoriesContainer.addEventListener('pointermove', (e) => {
    if (!isPointerDown) return;
  });

  categoriesContainer.addEventListener('pointerup', (e) => {
    if (!isPointerDown) return;
    isPointerDown = false;

    const diff = pointerStartX - e.clientX;
    const threshold = 50;

    if (Math.abs(diff) > threshold) {
      if (diff > 0) {
        // Dragged left - show next page
        if (currentPage < totalPages - 1) {
          currentPage++;
          showPage(currentPage);
        }
      } else {
        // Dragged right - show previous page
        if (currentPage > 0) {
          currentPage--;
          showPage(currentPage);
        }
      }
    }
  });

  // Initialize
  showPage(currentPage);
});