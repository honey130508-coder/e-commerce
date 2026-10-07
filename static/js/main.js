/**
 * ApexStore E-Commerce JavaScript
 * Handles dynamic cart operations, toast alerts, and UI interactions
 */

// Robust CSRF token extractor: checks meta tag, hidden input, then cookies
function getCsrfToken() {
  const metaToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
  if (metaToken && metaToken !== 'None') return metaToken;

  const inputToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
  if (inputToken) return inputToken;

  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === 'csrftoken=') {
        return decodeURIComponent(cookie.substring(10));
      }
    }
  }
  return '';
}

// Toast notification helper
function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  
  let icon = '🛒';
  if (type === 'success') icon = '✅';
  if (type === 'error') icon = '⚠️';
  if (type === 'info') icon = 'ℹ️';

  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
  container.appendChild(toast);

  // Trigger animation
  requestAnimationFrame(() => {
    toast.classList.add('show');
  });

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 3500);
}

// Update navbar cart badge
function updateCartBadge(count) {
  const badge = document.querySelector('.cart-badge');
  if (badge) {
    badge.textContent = count;
    badge.style.transform = 'scale(1.3)';
    setTimeout(() => {
      badge.style.transform = 'scale(1)';
    }, 200);
  }
}

// Initialize listeners on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss alerts
  document.querySelectorAll('.alert-close').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const alert = e.target.closest('.alert');
      if (alert) {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 250);
      }
    });
  });

  // AJAX Quick Add to Cart (from Product Cards)
  document.querySelectorAll('.btn-add-cart-ajax').forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();
      const url = button.dataset.url;
      const originalText = button.innerHTML;
      button.disabled = true;
      button.innerHTML = '<span>Adding...</span>';

      try {
        const formData = new FormData();
        formData.append('quantity', '1');

        const token = getCsrfToken();
        const headers = {
          'X-Requested-With': 'XMLHttpRequest'
        };
        if (token) {
          headers['X-CSRFToken'] = token;
        }

        const response = await fetch(url, {
          method: 'POST',
          headers: headers,
          body: formData
        });

        if (!response.ok) {
          let errorMsg = 'Could not add item to cart.';
          try {
            const errData = await response.json();
            if (errData && errData.message) errorMsg = errData.message;
          } catch (_) {
            errorMsg = `Server response (${response.status}). Please try again.`;
          }
          showToast(errorMsg, 'error');
          return;
        }

        const data = await response.json();
        if (data.success) {
          updateCartBadge(data.cart_total_items);
          showToast(data.message || 'Item added to your cart!', 'success');
        } else {
          showToast(data.message || 'Could not add item to cart.', 'error');
        }
      } catch (err) {
        console.error('Add to cart error:', err);
        showToast('Something went wrong. Please refresh and try again.', 'error');
      } finally {
        button.disabled = false;
        button.innerHTML = originalText;
      }
    });
  });

  // Detail Page Quantity Controls (+ and -)
  const qtyInput = document.querySelector('#detail-qty-input');
  const qtyMinus = document.querySelector('#btn-qty-minus');
  const qtyPlus = document.querySelector('#btn-qty-plus');

  if (qtyInput && qtyMinus && qtyPlus) {
    const maxStock = parseInt(qtyInput.getAttribute('max') || '99', 10);
    
    qtyMinus.addEventListener('click', () => {
      let val = parseInt(qtyInput.value, 10) || 1;
      if (val > 1) {
        qtyInput.value = val - 1;
      }
    });

    qtyPlus.addEventListener('click', () => {
      let val = parseInt(qtyInput.value, 10) || 1;
      if (val < maxStock) {
        qtyInput.value = val + 1;
      } else {
        showToast(`Only ${maxStock} items available in stock.`, 'info');
      }
    });
  }

  // Cart Page AJAX Quantity Modifiers
  document.querySelectorAll('.cart-qty-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const action = btn.dataset.action;
      const itemId = btn.dataset.itemId;
      const updateUrl = btn.dataset.url;
      const row = document.querySelector(`#cart-row-${itemId}`);
      const qtySpan = row ? row.querySelector('.cart-item-qty') : null;
      const subtotalSpan = row ? row.querySelector('.cart-item-subtotal') : null;

      const formData = new FormData();
      formData.append('action', action);

      try {
        const token = getCsrfToken();
        const headers = {
          'X-Requested-With': 'XMLHttpRequest'
        };
        if (token) headers['X-CSRFToken'] = token;

        const response = await fetch(updateUrl, {
          method: 'POST',
          headers: headers,
          body: formData
        });

        if (!response.ok) {
          showToast('Failed to update cart.', 'error');
          return;
        }

        const data = await response.json();
        if (data.success) {
          updateCartBadge(data.cart_total_items);

          if (data.item_removed) {
            if (row) {
              row.style.opacity = '0';
              setTimeout(() => {
                row.remove();
                if (data.cart_total_items === 0) {
                  window.location.reload();
                }
              }, 250);
            }
          } else {
            if (qtySpan) qtySpan.textContent = data.item_quantity;
            if (subtotalSpan) subtotalSpan.textContent = `$${data.item_subtotal}`;
          }

          // Update summary values
          const subtotalEl = document.querySelector('#summary-subtotal');
          const shippingEl = document.querySelector('#summary-shipping');
          const taxEl = document.querySelector('#summary-tax');
          const grandTotalEl = document.querySelector('#summary-grandtotal');

          if (subtotalEl) subtotalEl.textContent = `$${data.cart_subtotal}`;
          if (shippingEl) shippingEl.textContent = data.shipping === '0.00' ? 'FREE' : `$${data.shipping}`;
          if (taxEl) taxEl.textContent = `$${data.tax}`;
          if (grandTotalEl) grandTotalEl.textContent = `$${data.grand_total}`;
        }
      } catch (err) {
        console.error('Cart update failed:', err);
      }
    });
  });

  // Cart Page AJAX Remove Item
  document.querySelectorAll('.cart-btn-remove-ajax').forEach(btn => {
    btn.addEventListener('click', async () => {
      const itemId = btn.dataset.itemId;
      const removeUrl = btn.dataset.url;
      const row = document.querySelector(`#cart-row-${itemId}`);

      try {
        const token = getCsrfToken();
        const headers = {
          'X-Requested-With': 'XMLHttpRequest'
        };
        if (token) headers['X-CSRFToken'] = token;

        const response = await fetch(removeUrl, {
          method: 'POST',
          headers: headers
        });

        if (!response.ok) {
          showToast('Failed to remove item.', 'error');
          return;
        }

        const data = await response.json();
        if (data.success) {
          updateCartBadge(data.cart_total_items);
          showToast(data.message, 'info');

          if (row) {
            row.style.opacity = '0';
            setTimeout(() => {
              row.remove();
              if (data.cart_total_items === 0) {
                window.location.reload();
              }
            }, 250);
          }

          const subtotalEl = document.querySelector('#summary-subtotal');
          const shippingEl = document.querySelector('#summary-shipping');
          const taxEl = document.querySelector('#summary-tax');
          const grandTotalEl = document.querySelector('#summary-grandtotal');

          if (subtotalEl) subtotalEl.textContent = `$${data.cart_subtotal}`;
          if (shippingEl) shippingEl.textContent = data.shipping === '0.00' ? 'FREE' : `$${data.shipping}`;
          if (taxEl) taxEl.textContent = `$${data.tax}`;
          if (grandTotalEl) grandTotalEl.textContent = `$${data.grand_total}`;
        }
      } catch (err) {
        console.error('Cart remove error:', err);
      }
    });
  });

  // Checkout Payment Selection visual highlighting
  document.querySelectorAll('.payment-option-card').forEach(card => {
    card.addEventListener('click', () => {
      document.querySelectorAll('.payment-option-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      const radio = card.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
    });
  });
});
