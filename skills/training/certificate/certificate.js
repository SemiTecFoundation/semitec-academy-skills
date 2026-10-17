/* Publisher-owned HTML/CSS/JavaScript certificate; textContent keeps learner data literal. */
(function () {
  function draw(data) {
    document.querySelectorAll('[data-field]').forEach(function (node) {
      var key = node.dataset.field;
      if (data[key] != null) node.textContent = key === 'date' ? new Date(data[key]).toLocaleDateString() : String(data[key]);
    });
  }
  window.addEventListener('message', function (event) {
    if (event.source !== window.parent || !event.data || event.data.type !== 'semitec-certificate') return;
    draw(event.data.data || {});
  });
  if (window.CERTIFICATE_PREVIEW) draw({name:'Sample Learner',training:'Example Course',issuer:'Example Publisher',date:'2026-01-01',id:'PREVIEW — NOT ISSUED'});
}());
