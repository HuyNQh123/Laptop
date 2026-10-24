(() => {
  'use strict';
  function fallback(img) {
    if (img.dataset.failed) return;
    img.dataset.failed = 'true';
    img.src = img.dataset.fallback;
    img.alt = 'Chưa có ảnh sản phẩm';
    const frame = img.closest('.product-image');
    if (!frame.querySelector('.image-caption')) {
      const caption = document.createElement('span');
      caption.className = 'image-caption'; caption.textContent = 'Chưa có ảnh sản phẩm';
      frame.append(caption);
    }
  }
  document.addEventListener('error', e => { if (e.target.matches?.('[data-product-image]')) fallback(e.target); }, true);
  function checkImages() {
    document.querySelectorAll('[data-product-image]').forEach(img => {
      if (img.complete && img.naturalWidth === 0) fallback(img);
    });
  }
  checkImages(); window.addEventListener('catalog:updated', checkImages);
  if (!window.HTMLDialogElement) return;
  const dialog = document.createElement('dialog');
  dialog.className = 'source-dialog'; dialog.setAttribute('aria-labelledby', 'source-title');
  dialog.innerHTML = '<div class="dialog-heading"><h2 id="source-title">Nguồn dữ liệu</h2><button type="button" aria-label="Đóng nguồn dữ liệu">Đóng</button></div><div class="source-body" aria-live="polite"></div>';
  document.body.append(dialog);
  let trigger, request, sequence = 0;
  const body = dialog.querySelector('.source-body');
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { request?.abort(); sequence++; trigger?.focus(); });
  const labels = { 'price & rating': 'Giá và đánh giá', cpu_score: 'Điểm CPU', gpu_score: 'Điểm GPU', 'specs (cpu, gpu, ram, storage, screen, battery, weight, os)': 'Thông số phần cứng', units_sold: 'Số lượng bán' };
  function element(tag, text, className) {
    const node = document.createElement(tag); node.textContent = text;
    if (className) node.className = className;
    return node;
  }
  document.addEventListener('click', async e => {
    const link = e.target.closest('[data-source-id]');
    if (!link || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button !== 0) return;
    e.preventDefault(); trigger = link; request?.abort(); request = new AbortController();
    const current = ++sequence;
    body.textContent = 'Đang tải nguồn của ' + link.dataset.sourceName + '…';
    dialog.showModal();
    try {
      const response = await fetch(link.href, { signal: request.signal });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const data = await response.json();
      if (current !== sequence) return;
      body.replaceChildren(element('h3', data.laptop_name), element('p', Number(data.price).toLocaleString('vi-VN') + ' ₫ · Giá tham khảo', 'source-summary'));
      const list = element('ul', '', 'source-list');
      for (const source of data.sources || []) {
        const item = element('li', '');
        item.append(element('strong', labels[source.field_name] || source.field_name || 'Thông số khác'));
        item.append(element('p', (source.source_name || 'Chưa rõ đơn vị') + ' · Ngày xác minh: ' + (source.verified_date || 'Chưa có') + ' · Trạng thái: ' + (source.status || 'Chưa có')));
        if (source.note) item.append(element('p', source.note));
        try {
          const url = new URL(source.source_url);
          if (['http:', 'https:'].includes(url.protocol)) {
            const a = element('a', 'Mở trang nguồn ↗');
            a.href = url.href; a.target = '_blank'; a.rel = 'noopener noreferrer'; item.append(a);
          }
        } catch (_) { /* Missing source URLs are displayed as metadata only. */ }
        list.append(item);
      }
      body.append(list.childElementCount ? list : element('p', 'Chưa có nguồn liên kết cho máy này.'));
    } catch (error) {
      if (error.name !== 'AbortError' && current === sequence) body.textContent = 'Không thể tải nguồn dữ liệu. Đóng cửa sổ và thử lại.';
    }
  });
})();
