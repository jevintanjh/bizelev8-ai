/* bizElev8 shared mobile nav: toggle, link-click close, Escape, outside click */
(function () {
  'use strict';
  var nav = document.querySelector('header nav');
  if (!nav) return;
  var toggle = nav.querySelector('.nav-toggle');
  var menu = nav.querySelector('.nav-links');
  if (!toggle || !menu) return;

  function isOpen() { return menu.classList.contains('open'); }
  function setOpen(open) {
    menu.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  toggle.addEventListener('click', function (e) {
    e.stopPropagation();
    setOpen(!isOpen());
  });

  /* Close after choosing any link (covers same-page anchors like #why) */
  menu.addEventListener('click', function (e) {
    if (e.target && e.target.closest && e.target.closest('a')) setOpen(false);
  });

  /* Close on click/tap outside the header nav */
  document.addEventListener('click', function (e) {
    if (isOpen() && !nav.contains(e.target)) setOpen(false);
  });

  /* Close on Escape and return focus to the toggle */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen()) { setOpen(false); toggle.focus(); }
  });
})();
