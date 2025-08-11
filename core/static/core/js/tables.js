(function () {
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-toggle="table"]').forEach(function (tbl) {
      const wrapper = tbl.closest('.table-responsive');
      if (wrapper) wrapper.classList.add('table-card');
      const card = wrapper?.closest('.card');
      if (card) card.classList.add('card-soft');
    });
  });
})();
