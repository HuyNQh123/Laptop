(() => {
  'use strict';
  // Keep native details click/keyboard behavior; only enhance the desktop nav with hover.
  const navigation = document.querySelector('.more-navigation');
  if (navigation) {
    const summary = navigation.querySelector('summary');
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
    let hoverOpened = false;
    const closeNavigation = () => { navigation.open = false; hoverOpened = false; };
    navigation.addEventListener('pointerenter', e => {
      if (e.pointerType === 'mouse' && finePointer.matches && !navigation.open) {
        navigation.open = true; hoverOpened = true;
      }
    });
    navigation.addEventListener('pointerleave', () => {
      if (hoverOpened && !navigation.contains(document.activeElement)) closeNavigation();
    });
    summary.addEventListener('click', e => {
      // A click after hover pins the menu open instead of immediately toggling it shut.
      if (hoverOpened) { e.preventDefault(); hoverOpened = false; }
    });
    navigation.addEventListener('focusout', e => {
      if (!navigation.contains(e.relatedTarget) && !navigation.matches(':hover')) closeNavigation();
    });
    document.addEventListener('click', e => {
      if (!navigation.contains(e.target)) closeNavigation();
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && navigation.open) {
        closeNavigation(); summary.focus(); e.preventDefault();
      }
    });
    finePointer.addEventListener('change', () => { if (hoverOpened) closeNavigation(); });
  }
  function fallback(img) {
    if (img.dataset.failed) return;
    img.dataset.failed = 'true';
    img.src = img.dataset.fallback;
    img.alt = 'Chưa có ảnh: ' + (img.dataset.productName || 'laptop');
    const frame = img.closest('.product-image, .showcase-product');
    if (frame && !frame.querySelector('.image-caption')) {
      const caption = document.createElement('span');
      caption.className = 'image-caption'; caption.textContent = 'Chưa có ảnh';
      frame.append(caption);
    }
    const credit = img.closest('.product-figure')?.querySelector('.image-credit');
    if (credit) credit.textContent = 'Không tải được ảnh đã xác minh. Chưa có ảnh.';
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
  dialog.innerHTML = '<div class="dialog-heading"><h2 id="source-title">Đối chiếu Nguồn giá &amp; Dữ liệu Thị trường</h2><button type="button" data-close-source aria-label="Đóng nguồn dữ liệu">×</button></div><div class="source-body" aria-live="polite"></div><div class="source-footer"><p>Trạng thái theo hồ sơ kiểm chứng trong dữ liệu; không phải xác nhận giá bán hiện tại.</p><button type="button" data-close-source>Đóng</button></div>';
  document.body.append(dialog);
  let trigger, request, sequence = 0;
  const body = dialog.querySelector('.source-body');
  dialog.querySelectorAll('[data-close-source]').forEach(button => button.addEventListener('click', () => dialog.close()));
  dialog.addEventListener('close', () => { request?.abort(); sequence++; trigger?.focus(); });
  const labels = { 'price & rating': 'Giá niêm yết & Đánh giá', cpu_score: 'Benchmark PassMark CPU', gpu_score: 'Benchmark PassMark GPU', 'specs (cpu, gpu, ram, storage, screen, battery, weight, os)': 'Cấu hình phần cứng chuẩn hãng', units_sold: 'Doanh số & Số lượng bán' };
  function element(tag, text, className) {
    const node = document.createElement(tag); node.textContent = text;
    if (className) node.className = className;
    return node;
  }
  function sourceURL(value) {
    if (typeof value !== 'string') return null;
    try {
      const url = new URL(value);
      return ['http:', 'https:'].includes(url.protocol) && url.hostname && !url.username && !url.password ? url : null;
    } catch (_) { return null; }
  }
  function renderSources(data) {
    const summary = element('div', '', 'source-product-summary');
    const identity = element('div', '');
    identity.append(element('span', data.brand || 'Laptop', 'source-brand'), element('h3', data.laptop_name));
    const price = element('div', '', 'source-price');
    price.append(element('span', 'Giá trong bộ dữ liệu'));
    price.append(element('strong', Number.isFinite(Number(data.price)) && data.price !== null ? Number(data.price).toLocaleString('vi-VN') + ' ₫' : 'Chưa có giá'));
    summary.append(identity, price); body.replaceChildren(summary);
    if (!data.sources.length) {
      body.append(element('p', 'Chưa có nguồn kiểm chứng liên kết cho máy này.', 'source-notice'));
      return;
    }
    body.append(element('p', 'Danh sách nguồn và ghi chú đối chiếu:', 'source-intro'));
    body.append(element('p', 'Trượt ngang để xem đủ trạng thái, ghi chú và liên kết →', 'source-scroll-hint'));
    const scroll = element('div', '', 'source-table-scroll');
    scroll.tabIndex = 0; scroll.setAttribute('role', 'region'); scroll.setAttribute('aria-label', 'Bảng nguồn kiểm chứng, cuộn ngang để xem đủ cột');
    const table = element('table', '', 'source-table');
    const head = element('thead', ''), headRow = element('tr', '');
    for (const label of ['Mục dữ liệu', 'Đơn vị cung cấp', 'Trạng thái', 'Ghi chú kiểm chứng', 'Liên kết']) {
      const cell = element('th', label); cell.scope = 'col'; headRow.append(cell);
    }
    head.append(headRow); const rows = element('tbody', '');
    for (const source of data.sources) {
      const row = element('tr', '');
      const field = element('th', labels[source.field_name] || source.field_name || 'Thông số khác'); field.scope = 'row';
      const provider = element('td', source.source_name || 'Chưa rõ đơn vị');
      const verified = ['Đã xác minh', 'Verified'].includes(source.status);
      const pending = source.status === 'Chưa xác minh được';
      const status = element('td', '');
      status.append(element('span', verified ? 'Đã xác minh' : source.status || 'Chưa có nguồn xác minh', 'source-status ' + (verified ? 'is-verified' : pending ? 'is-pending' : 'is-missing')));
      const note = element('td', source.note || 'Chưa có ghi chú kiểm chứng.', 'source-note');
      note.append(element('small', 'Ngày ghi nhận: ' + (source.verified_date || 'Chưa có')));
      const links = element('td', ''); const url = sourceURL(source.source_url);
      if (url && (verified || pending)) {
        const anchor = element('a', verified ? 'Mở trang nguồn ↗' : 'Xem liên kết hãng ↗', 'source-action');
        anchor.href = url.href; anchor.target = '_blank'; anchor.rel = 'noopener noreferrer'; links.append(anchor);
      } else {
        links.append(element('span', source.source_url && !url ? 'Liên kết không hợp lệ' : 'Không có liên kết khả dụng', 'source-no-link'));
      }
      row.append(field, provider, status, note, links); rows.append(row);
    }
    table.append(head, rows); scroll.append(table); body.append(scroll);
    body.append(element('p', 'Liên kết hãng chưa xác minh chỉ phục vụ đối chiếu, không chứng minh giá hoặc thông số đã được xác nhận.', 'source-disclaimer'));
  }
  async function openSources(link) {
    trigger = link; request?.abort(); request = new AbortController();
    const current = ++sequence;
    body.replaceChildren(element('p', 'Đang tải nguồn của ' + link.dataset.sourceName + '…', 'source-notice'));
    body.setAttribute('aria-busy', 'true');
    if (!dialog.open) dialog.showModal();
    try {
      const response = await fetch(link.href, { signal: request.signal });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const data = await response.json();
      if (current !== sequence) return;
      if (data.laptop_name !== link.dataset.sourceName || !Array.isArray(data.sources) || data.sources.some(source => !source || typeof source !== 'object' || source.laptop_name && source.laptop_name !== data.laptop_name)) throw new Error('Invalid source identity');
      renderSources(data);
    } catch (error) {
      if (error.name !== 'AbortError' && current === sequence) {
        body.replaceChildren(element('p', 'Không thể tải nguồn dữ liệu đúng máy. Vui lòng thử lại.', 'source-notice source-error'));
        const retry = element('button', 'Thử lại', 'btn btn-outline-primary'); retry.type = 'button';
        retry.addEventListener('click', () => openSources(link)); body.append(retry);
      }
    } finally {
      if (current === sequence) body.setAttribute('aria-busy', 'false');
    }
  }
  document.addEventListener('click', e => {
    const link = e.target.closest('[data-source-id]');
    if (!link || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button !== 0) return;
    e.preventDefault(); openSources(link);
  });
})();
