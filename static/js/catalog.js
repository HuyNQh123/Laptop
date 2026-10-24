(() => {
  'use strict';
  const form = document.querySelector('#catalog-form');
  if (!form || !window.fetch || !window.DOMParser) return;
  const results = document.querySelector('.catalog-results');
  const error = document.querySelector('#catalog-error');
  let controller, timer, generation = 0;
  function urlFromForm() {
    const url = new URL(form.action);
    for (const [key, value] of new FormData(form)) if (value !== '') url.searchParams.set(key, value);
    return url;
  }
  async function refresh(url, paginate = false) {
    clearTimeout(timer);
    controller?.abort();
    controller = new AbortController();
    const current = ++generation;
    results.setAttribute('aria-busy', 'true');
    error.hidden = true;
    try {
      const response = await fetch(url, { signal: controller.signal });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const html = new DOMParser().parseFromString(await response.text(), 'text/html');
      if (current !== generation) return;
      for (const id of ['catalog-content', 'result-count', 'result-range']) {
        const replacement = html.getElementById(id);
        if (!replacement) throw new Error('Missing results');
        const target = document.getElementById(id);
        if (id === 'catalog-content') target.replaceChildren(...replacement.childNodes);
        else target.textContent = replacement.textContent;
      }
      history.pushState({}, '', url);
      window.dispatchEvent(new Event('catalog:updated'));
      if (paginate) {
        document.querySelector('#result-count').scrollIntoView({ block: 'start' });
        const first = document.querySelector('#catalog-content a');
        first?.focus({ preventScroll: true });
      }
    } catch (e) {
      if (e.name !== 'AbortError' && current === generation) {
        error.textContent = 'Không thể tải kết quả. ';
        const retry = document.createElement('a');
        retry.href = url; retry.textContent = 'Mở trang kết quả để thử lại';
        error.append(retry); error.hidden = false;
      }
    } finally {
      if (current === generation) results.removeAttribute('aria-busy');
    }
  }
  form.addEventListener('submit', e => { e.preventDefault(); refresh(urlFromForm()); });
  form.addEventListener('change', e => { if (e.target.matches('select')) refresh(urlFromForm()); });
  document.querySelector('#q').addEventListener('input', () => {
    clearTimeout(timer); controller?.abort(); generation++;
    timer = setTimeout(() => refresh(urlFromForm()), 350);
  });
  document.addEventListener('click', e => {
    const link = e.target.closest('[data-page-link]');
    if (!link || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button !== 0) return;
    e.preventDefault();
    // A filter request may still be pending: use the current form, not stale link filters.
    const url = urlFromForm();
    url.searchParams.set('page', new URL(link.href).searchParams.get('page') || '1');
    refresh(url, true);
  });
  window.addEventListener('popstate', () => location.reload());
})();
