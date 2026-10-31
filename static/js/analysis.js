(() => {
  'use strict';
  const search = document.getElementById('stats-search');
  const brand = document.getElementById('stats-brand');
  if (!search || !brand) return;
  const rows = [...document.querySelectorAll('#stats-table tr[data-brand]')];
  const normalize = text => text.toLocaleLowerCase('vi').replaceAll('đ', 'd')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  function filter() {
    const query = normalize(search.value.trim());
    let count = 0;
    for (const row of rows) {
      row.hidden = !((brand.value === 'all' || row.dataset.brand === brand.value) &&
        normalize(row.cells[0].textContent + ' ' + row.cells[1].textContent + ' ' + row.dataset.feature).includes(query));
      if (!row.hidden) count++;
    }
    document.getElementById('stats-count').textContent = count + ' dòng thống kê';
    document.getElementById('stats-empty').hidden = count > 0;
  }
  search.addEventListener('input', filter);
  brand.addEventListener('change', filter);
})();
