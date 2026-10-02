(() => {
  const endpoint = (form) => `/api/leads/${form.dataset.leadForm}`;
  const text = (form, message, kind) => {
    let node = form.querySelector('.lead-result');
    if (!node) { node = document.createElement('p'); node.className = 'lead-result'; form.append(node); }
    node.textContent = message; node.style.color = kind === 'error' ? '#b42318' : '#087443'; node.setAttribute('role', 'status');
  };
  document.addEventListener('DOMContentLoaded', () => document.querySelectorAll('form[data-lead-form]').forEach((form) => {
    const started = Date.now() / 1000;
    const hp = document.createElement('input');
    hp.name = '_hp'; hp.autocomplete = 'off'; hp.tabIndex = -1; hp.setAttribute('aria-hidden', 'true'); hp.style.cssText = 'position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden';
    form.append(hp);
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const submit = form.querySelector('[type="submit"]'); submit.disabled = true;
      const values = Object.fromEntries(new FormData(form).entries()); values.loaded_at = started;
      if (form.elements.consent) values.consent = form.elements.consent.checked;
      try {
        const response = await fetch(endpoint(form), {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(values)});
        const result = await response.json();
        if (!response.ok) throw result;
        form.reset(); text(form, 'Thanks — we will be in touch within one working day.', 'success');
        window.posthog?.capture?.('lead_form_submitted', {form_type: form.dataset.leadForm, success: true});
      } catch (error) {
        const message = error?.error === 'rate_limited' ? 'Too many attempts. Please try again shortly.' : 'Please check the required fields and try again.';
        text(form, message, 'error'); window.posthog?.capture?.('lead_form_error', {form_type: form.dataset.leadForm, error: error?.error || 'request_failed'});
      } finally { submit.disabled = false; }
    });
  }));
})();
