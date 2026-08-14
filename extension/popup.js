let currentBook = null;

document.addEventListener('DOMContentLoaded', () => {
  cargarLibroActual();

  document.getElementById('btn-refresh').addEventListener('click', cargarLibroActual);
  document.getElementById('btn-payhip').addEventListener('click', autocompletarPayhip);
  document.getElementById('btn-hotmart').addEventListener('click', autocompletarHotmart);
});

async function cargarLibroActual() {
  const infoDiv = document.getElementById('book-info');
  const btnPayhip = document.getElementById('btn-payhip');
  const btnHotmart = document.getElementById('btn-hotmart');
  const statusDiv = document.getElementById('status');

  statusDiv.className = '';
  statusDiv.textContent = '';
  infoDiv.innerHTML = '<div class="card-title">Conectando al Panel...</div>';

  try {
    const res = await fetch('http://localhost:5100/api/ebooks/current');
    if (!res.ok) {
      throw new Error('Sin libro preparado');
    }

    const data = await res.json();
    if (data.status === 'ok' && data.libro) {
      currentBook = data.libro;
      const tituloFull = currentBook.subtitulo ? `${currentBook.titulo}: ${currentBook.subtitulo}` : currentBook.titulo;
      const precio = currentBook.precio_usd || 20.00;

      infoDiv.innerHTML = `
        <div class="card-title">Libro Listo para Publicar</div>
        <div class="book-title">${tituloFull}</div>
        <div class="book-price">$${precio} USD</div>
      `;

      btnPayhip.disabled = false;
      btnHotmart.disabled = false;
    } else {
      throw new Error('Respuesta inválida');
    }
  } catch (err) {
    currentBook = null;
    infoDiv.innerHTML = `
      <div class="card-title" style="color:#ef4444;">Sin libro preparado</div>
      <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">
        1. Abrí el Panel Editorial (localhost:5100)<br>
        2. Hacé clic en <b>"📝 3. PREPARAR EXTENSIÓN"</b> en tu libro
      </div>
    `;
    btnPayhip.disabled = true;
    btnHotmart.disabled = true;
  }
}

async function autocompletarPayhip() {
  if (!currentBook) return;
  const statusDiv = document.getElementById('status');

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url.includes('payhip.com')) {
    statusDiv.className = 'warning';
    statusDiv.textContent = '⚠️ Primero abrí la pestaña de Payhip';
    return;
  }

  const tituloFull = currentBook.subtitulo ? `${currentBook.titulo}: ${currentBook.subtitulo}` : currentBook.titulo;
  const precio = String(currentBook.precio_usd || 20.00);
  const descripcion = currentBook.resumen_corto || currentBook.descripcion || `Descubrí ${tituloFull}, la guía completa creada por Nicolás Noguera.`;

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: (t, p, d) => {
      let completados = 0;
      
      // Título
      const titleSelectors = ['input[name="title"]', '#product-title', 'input[placeholder*="title" i]'];
      for (const sel of titleSelectors) {
        const el = document.querySelector(sel);
        if (el) {
          el.value = t;
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          completados++;
          break;
        }
      }

      // Precio
      const priceSelectors = ['input[name="price"]', '#product-price', 'input[placeholder*="price" i]'];
      for (const sel of priceSelectors) {
        const el = document.querySelector(sel);
        if (el) {
          el.value = p;
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          completados++;
          break;
        }
      }

      // Descripción (Textarea o Rich Text Editor Quill / Summernote / contenteditable)
      const descSelectors = ['.ql-editor', '.note-editable', 'div[contenteditable="true"]', 'textarea[name="description"]', '#product-description', 'textarea'];
      for (const sel of descSelectors) {
        const el = document.querySelector(sel);
        if (el) {
          if (el.isContentEditable || el.tagName === 'DIV') {
            el.innerHTML = `<p>${d}</p>`;
          } else {
            el.value = d;
          }
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          completados++;
          break;
        }
      }

      if (completados > 0) {
        alert('🎉 ¡Payhip autocompletado con éxito!\n\n• Título\n• Precio ($' + p + ' USD)\n• Descripción\n\nArrastrá el manuscrito .docx y la portada .jpg que se abrieron en el Explorador de Windows.');
      } else {
        alert('⚠️ No se encontraron los campos en esta página. Asegurate de estar en el formulario de "Agregar Producto Digital".');
      }
    },
    args: [tituloFull, precio, descripcion]
  });

  statusDiv.className = 'success';
  statusDiv.textContent = '✅ ¡Campos enviados a Payhip!';
}

async function autocompletarHotmart() {
  if (!currentBook) return;
  const statusDiv = document.getElementById('status');

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url.includes('hotmart.com')) {
    statusDiv.className = 'warning';
    statusDiv.textContent = '⚠️ Primero abrí la pestaña de Hotmart';
    return;
  }

  const tituloFull = currentBook.subtitulo ? `${currentBook.titulo}: ${currentBook.subtitulo}` : currentBook.titulo;
  const descripcion = currentBook.resumen_corto || currentBook.descripcion || `Descubrí ${tituloFull}, la guía completa creada por Nicolás Noguera.`;

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: (t, d) => {
      let completados = 0;
      
      // Nombre
      const nameSelectors = ['input[name="name"]', '#product-name', 'input[placeholder*="name" i]', 'input[placeholder*="nombre" i]', 'input[placeholder*="nome" i]'];
      for (const sel of nameSelectors) {
        const el = document.querySelector(sel);
        if (el) {
          el.value = t;
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          completados++;
          break;
        }
      }

      // Descripción
      const descSelectors = ['textarea[name="description"]', 'textarea[placeholder*="descri" i]', '.ql-editor', 'textarea'];
      for (const sel of descSelectors) {
        const el = document.querySelector(sel);
        if (el) {
          if (el.isContentEditable || el.tagName === 'DIV') {
            el.innerHTML = `<p>${d}</p>`;
          } else {
            el.value = d;
          }
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          completados++;
          break;
        }
      }

      if (completados > 0) {
        alert('🎉 ¡Nombre y descripción autocompletados en Hotmart!\n\nContinuá completando los pasos de categoría y precio.');
      } else {
        alert('⚠️ No se encontró el campo de nombre. Asegurate de estar en el primer paso de "Crear Producto".');
      }
    },
    args: [tituloFull, descripcion]
  });

  statusDiv.className = 'success';
  statusDiv.textContent = '✅ ¡Campos enviados a Hotmart!';
}
