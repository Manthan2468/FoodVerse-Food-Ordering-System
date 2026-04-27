window.addEventListener('scroll', () => {
  const nav = document.querySelector('nav');

  if (window.scrollY > 20) {
    nav.style.background = 'rgba(253,246,236,0.97)';
    nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.05)';
  } else {
    nav.style.background = 'rgba(253,246,236,0.85)';
    nav.style.boxShadow = 'none';
  }
});

// Category active toggle
    document.querySelectorAll('.cat-item').forEach(item => {
      item.addEventListener('click', () => {
        document.querySelectorAll('.cat-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');
      });
    });

    // Food tag toggle
    document.querySelectorAll('.tag').forEach(tag => {
      tag.addEventListener('click', () => {
        document.querySelectorAll('.tag').forEach(t => {
          t.classList.remove('tag-active');
          t.classList.add('tag-passive');
        });
        tag.classList.add('tag-active');
        tag.classList.remove('tag-passive');
      });
    });

