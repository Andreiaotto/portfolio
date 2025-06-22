// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
  // Smooth scrolling for internal links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      document.querySelector(targetId).scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    });
  });

  // Add active class to current navigation item
  const navLinks = document.querySelectorAll('.navbar a');
  const currentPage = window.location.pathname.split('/').pop();
  
  navLinks.forEach(link => {
    const linkHref = link.getAttribute('href');
    if (linkHref === currentPage || 
        (currentPage === '' && linkHref === 'index.html')) {
      link.classList.add('active');
    }
  });
  
  // Subtle parallax effect on scroll
  window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY;
    document.body.style.backgroundPositionY = `${scrollPosition * 0.5}px`;
  });
  
  // Function to change background image
  function changeBackground(imagePath) {
    document.body.style.backgroundImage = `linear-gradient(rgba(240, 255, 240, 0.8), rgba(230, 248, 230, 0.8)), url('${imagePath}')`;
  }
  
  // Optional: Randomly select from multiple background images
  const backgrounds = [
    'images/background.jpg',
    'images/background-chat.jpg'
  ];
  
  // Use the original background by default
  // If you want to randomize, uncomment the line below
  // changeBackground(backgrounds[Math.floor(Math.random() * backgrounds.length)]);
});