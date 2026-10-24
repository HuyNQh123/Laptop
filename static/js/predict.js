(() => {
  'use strict';
  const keys = ['cpu_score','gpu_score','ram','storage','screen_size','refresh_rate','weight','battery','rating'];
  const presets = {
    office: [13000,2500,16,512,14,60,1.35,54,4.6],
    dev: [21000,4150,16,512,15.6,120,1.70,70,4.7],
    gaming: [26000,14800,16,512,15.6,144,2.25,70,4.6],
  };
  document.querySelectorAll('[data-preset]').forEach(button => {
    button.addEventListener('click', () => {
      const values = presets[button.dataset.preset];
      if (!values) return;
      keys.forEach((key, index) => { document.getElementById(key).value = values[index]; });
      document.getElementById('cpu_score').focus();
    });
  });
})();
