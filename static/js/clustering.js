(() => {
  'use strict';
  const tbody = document.querySelector('#cluster-table tbody');
  if (!tbody) return;
  const rows = Array.from(tbody.rows);
  const q = document.getElementById('cluster-q');
  const filter = document.getElementById('cluster-filter');
  const sort = document.getElementById('cluster-sort');
  let page = 1;
  const normalize = text => text.toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d');
  function draw() {
    const terms = normalize(q.value).trim().split(/\s+/).filter(Boolean);
    const found = rows.filter(row => (!filter.value || row.dataset.cluster === filter.value) && terms.every(t => normalize(row.textContent).includes(t)));
    if (sort.value !== 'original') found.sort((a,b) => sort.value === 'name' ? a.cells[1].textContent.localeCompare(b.cells[1].textContent,'vi') : (Number(a.dataset[sort.value.replace('-desc','')]) - Number(b.dataset[sort.value.replace('-desc','')])) * (sort.value === 'price' ? 1 : -1));
    const pages = Math.max(1, Math.ceil(found.length / 10));
    page = Math.min(page, pages);
    rows.forEach(row => { row.hidden = true; });
    found.forEach(row => tbody.append(row));
    found.slice((page-1)*10,page*10).forEach(row => { row.hidden = false; });
    document.getElementById('cluster-count').textContent = `${found.length} mẫu laptop`;
    document.getElementById('cluster-page').textContent = `Trang ${page} / ${pages}`;
    document.getElementById('cluster-prev').disabled = page === 1;
    document.getElementById('cluster-next').disabled = page === pages;
    document.getElementById('cluster-pagination').hidden = false;
  }
  q.addEventListener('input',()=>{page=1;draw();});
  [filter,sort].forEach(select=>select.addEventListener('change',()=>{page=1;draw();}));
  document.getElementById('cluster-prev').addEventListener('click',()=>{page--;draw();});
  document.getElementById('cluster-next').addEventListener('click',()=>{page++;draw();});
  draw();
})();
