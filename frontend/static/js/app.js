document.addEventListener('DOMContentLoaded', () => {
  // Flash messages
  document.querySelectorAll('.alert').forEach((a, i) => {
    setTimeout(() => {
      a.classList.add('alert-hide');
      setTimeout(() => a.remove(), 450);
    }, 3500 + i * 250);
  });

  // Reveal-on-load animation
  document.querySelectorAll('.reveal').forEach((el, i) => {
    el.style.setProperty('--delay', `${Math.min(i * 80, 320)}ms`);
    el.classList.add('is-visible');
  });

  // Books: live search + result count
  const search = document.getElementById('bookSearch');
  const clear = document.getElementById('clearSearch');
  const cards = [...document.querySelectorAll('.searchable-card')];
  const count = document.getElementById('resultCount');
  const empty = document.getElementById('liveEmpty');
  const hint = document.getElementById('searchHint');

  function filterBooks() {
    if (!search || !cards.length) return;
    const term = search.value.trim().toLowerCase();
    let visible = 0;
    cards.forEach(card => {
      const matches = card.dataset.search.toLowerCase().includes(term);
      card.hidden = !matches;
      if (matches) {
        visible++;
        card.classList.remove('card-hidden');
        requestAnimationFrame(() => card.classList.add('card-visible'));
      } else {
        card.classList.remove('card-visible');
      }
    });
    if (count) count.textContent = visible;
    if (empty) empty.hidden = visible !== 0;
    if (hint) hint.textContent = term ? `Showing matches for “${term}”` : 'Live search is enabled';
    if (clear) clear.classList.toggle('show', !!term);
  }

  if (search) {
    search.addEventListener('input', filterBooks);
    filterBooks();
  }
  if (clear) {
    clear.addEventListener('click', () => {
      search.value = '';
      filterBooks();
      search.focus();
    });
  }

  // Mobile number: allow digits only, max 10
  const phone = document.getElementById('phone');
  const phoneHelp = document.getElementById('phoneHelp');
  if (phone) {
    phone.addEventListener('input', () => {
      phone.value = phone.value.replace(/\D/g, '').slice(0, 10);
      const valid = phone.value.length === 10;
      phone.classList.toggle('valid-field', valid);
      phone.classList.toggle('invalid-field', phone.value.length > 0 && !valid);
      if (phoneHelp) phoneHelp.textContent = valid ? '✓ Valid 10-digit mobile number.' : 'Enter exactly 10 digits.';
    });
  }

  const memberForm = document.getElementById('memberForm');
  if (memberForm) {
    memberForm.addEventListener('submit', (e) => {
      if (phone && phone.value.length !== 10) {
        e.preventDefault();
        phone.focus();
        phone.classList.add('invalid-field');
        if (phoneHelp) phoneHelp.textContent = 'Please enter exactly 10 digits.';
      }
    });
  }

  // Small button/card interaction
  document.querySelectorAll('.btn, .category-pill').forEach(el => {
    el.addEventListener('pointerdown', () => el.classList.add('pressed'));
    el.addEventListener('pointerup', () => el.classList.remove('pressed'));
    el.addEventListener('pointerleave', () => el.classList.remove('pressed'));
  });
});