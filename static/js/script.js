document.querySelectorAll('.toggler').forEach(button => {
    button.addEventListener('click', e => {
      let targ = `#${e.target.dataset.ref}`;
      document.querySelectorAll('.toggles').forEach(div => div.classList.add('hide'));
      document.querySelector(targ).classList.remove('hide');
    });
});