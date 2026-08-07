// app.js - Catálogo Oficial de Libros de Nicolás Noguera

const BOOKS_DATA = [
  {
    id: "de-cero-a-negocio-con-ia",
    titulo: "De Cero a Negocio con IA",
    subtitulo: "Cómo lanzar y ejecutar tu emprendimiento en 90 días",
    categoria: "emprendimiento",
    categoria_label: "IA & Emprendimiento",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/de-cero-a-negocio-con-ia/portada.jpg",
    resumen: "La guía definitiva de 90 días para validar, construir y escalar tu negocio utilizando inteligencia artificial sin gastar capital ni saber programar.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/productos/de-cero-a-negocio-con-ia",
    link_int: "https://payhip.com/b/DpFWs"
  },
  {
    id: "el-algoritmo-personal",
    titulo: "El Algoritmo Personal",
    subtitulo: "Rediseñá tus hábitos, dominá tu enfoque y ejecutá con claridad",
    categoria: "productividad",
    categoria_label: "Desarrollo Personal",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/el-algoritmo-personal/portada.jpg",
    resumen: "El sistema definitivo para eliminar la procrastinación, auditar tu entorno y construir consistencia ininterrumpida sin depender de la motivación efímera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "oni-no-ketsuryu-volumen-1",
    titulo: "Oni no Ketsuryū — Vol. 1",
    subtitulo: "La Noche de las Hojas Rotas",
    categoria: "tecnologia",
    categoria_label: "Manga Dark Fantasy",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/oni-no-ketsuryu-volumen-1/portada.jpg",
    resumen: "Ren forja una katana de cristal negro tras la masacre de su aldea. 15 ilustraciones exclusivas en 8k por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "oni-no-ketsuryu-volumen-2",
    titulo: "Oni no Ketsuryū — Vol. 2",
    subtitulo: "El Examen de la Montaña Sombría",
    categoria: "tecnologia",
    categoria_label: "Manga Dark Fantasy",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/oni-no-ketsuryu-volumen-2/portada.jpg",
    resumen: "La prueba final entre la niebla del monte Fujikane. 15 ilustraciones exclusivas en 8k por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "oni-no-ketsuryu-volumen-3",
    titulo: "Oni no Ketsuryū — Vol. 3",
    subtitulo: "El Tren de las Sombras",
    categoria: "tecnologia",
    categoria_label: "Manga Dark Fantasy",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/oni-no-ketsuryu-volumen-3/portada.jpg",
    resumen: "La batalla sobre rieles a alta velocidad contra la horda demoníaca. 15 ilustraciones exclusivas en 8k por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "oni-no-ketsuryu-volumen-4",
    titulo: "Oni no Ketsuryū — Vol. 4",
    subtitulo: "El Distrito de los Espejos y la Mariposa de la Sombra",
    categoria: "tecnologia",
    categoria_label: "Manga Dark Fantasy",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/oni-no-ketsuryu-volumen-4/portada.jpg",
    resumen: "La infiltración en el Distrito de las Luces y la batalla contra el Quinto Lunar Rojo. 15 ilustraciones exclusivas por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "oni-no-ketsuryu-volumen-5",
    titulo: "Oni no Ketsuryū — Vol. 5",
    subtitulo: "La Aldea de los Herreros Olvidados",
    categoria: "tecnologia",
    categoria_label: "Manga Dark Fantasy",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/oni-no-ketsuryu-volumen-5/portada.jpg",
    resumen: "La forja de la Katana del Sol de la era Sengoku y el milagro histórico bajo la luz del sol. 15 ilustraciones exclusivas por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "oni-no-ketsuryu-volumen-6",
    titulo: "Oni no Ketsuryū — Vol. 6",
    subtitulo: "Las Catacumbas del Olvido",
    categoria: "tecnologia",
    categoria_label: "Manga Dark Fantasy",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/oni-no-ketsuryu-volumen-6/portada.jpg",
    resumen: "El secreto de la Marca del Sol, la batalla contra el Primer Lunar en las catacumbas y el inicio del Castillo Infinito. 15 ilustraciones exclusivas por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "oni-no-ketsuryu-volumen-7",
    titulo: "Oni no Ketsuryū — Vol. 7",
    subtitulo: "El Asedio al Castillo Infinito",
    categoria: "tecnologia",
    categoria_label: "Manga Dark Fantasy",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/oni-no-ketsuryu-volumen-7/portada.jpg",
    resumen: "La infiltración en la fortaleza dimensional, la batalla de venenos de Kanae contra Doma y el inicio del clímax. 15 ilustraciones exclusivas por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "oni-no-ketsuryu-volumen-8",
    titulo: "Oni no Ketsuryū — Vol. 8",
    subtitulo: "El Juicio de los Tres Lunares Superiores",
    categoria: "tecnologia",
    categoria_label: "Manga Dark Fantasy",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/oni-no-ketsuryu-volumen-8/portada.jpg",
    resumen: "La redención de Akaza, el choque de las Hojas Rojas contra Kokushibo y el ascenso del castillo hacia la superficie. 15 ilustraciones exclusivas por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "kuro-no-kineki-volumen-1",
    titulo: "Kuro no Kineki — Vol. 1",
    subtitulo: "El Precio del Primer Paso",
    categoria: "tecnologia",
    categoria_label: "Manga Steampunk",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/kuro-no-kineki-volumen-1/portada.jpg",
    resumen: "Para recordar quién eres, primero debes olvidar lo que más amabas. El primer volumen oficial de la serie steampunk por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "kuro-no-kineki-volumen-2",
    titulo: "Kuro no Kineki — Vol. 2",
    subtitulo: "La Trinidad de las Tres Dagas",
    categoria: "tecnologia",
    categoria_label: "Manga Steampunk",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/kuro-no-kineki-volumen-2/portada.jpg",
    resumen: "El apasionante desenlace de la batalla por Aetheria. La trinidad de las tres dagas y el descenso de la Ciudad Flotante por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  },
  {
    id: "kuro-no-kineki-volumen-3",
    titulo: "Kuro no Kineki — Vol. 3",
    subtitulo: "El Continente de Plata",
    categoria: "tecnologia",
    categoria_label: "Manga Steampunk",
    precio_usd: 20.00,
    precio_ars: 26000,
    portada: "libros/kuro-no-kineki-volumen-3/portada.jpg",
    resumen: "El desenlace definitivo de la épica trilogía steampunk. El viaje al Continente de Plata y el Lienzo Blanco por Nicolás Noguera.",
    link_arg: "https://nicolasnogueraeditorial.mitiendanube.com/",
    link_int: "https://payhip.com/NicolasNogueraEditorial"
  }
];

function renderBooks(filterCategory = 'all', searchQuery = '') {
  const container = document.getElementById('booksGrid');
  if (!container) return;

  const filtered = BOOKS_DATA.filter(book => {
    const matchesCategory = filterCategory === 'all' || book.categoria === filterCategory;
    const matchesSearch = !searchQuery || 
      book.titulo.toLowerCase().includes(searchQuery.toLowerCase()) || 
      book.subtitulo.toLowerCase().includes(searchQuery.toLowerCase()) ||
      book.resumen.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  if (filtered.length === 0) {
    container.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding: 40px; color: #9ca3af;">No se encontraron libros en esta categoría.</div>';
    return;
  }

  container.innerHTML = filtered.map(book => `
    <div class="book-card">
      <div class="cover-wrap" style="height: 280px; overflow: hidden; position: relative; background: #1e293b;">
        <img src="${book.portada}" alt="${book.titulo}" style="width: 100%; height: 100%; object-fit: cover;">
        <span style="position: absolute; top: 12px; right: 12px; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); color: #fff; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">${book.categoria_label}</span>
      </div>
      <div class="book-body" style="padding: 20px; flex: 1; display: flex; flex-direction: column;">
        <h3 style="font-size: 1.25rem; font-family: 'Outfit', sans-serif; margin-bottom: 4px; color: #fff;">${book.titulo}</h3>
        <h4 style="font-size: 0.9rem; font-weight: 500; color: #f97316; margin-bottom: 10px;">${book.subtitulo}</h4>
        <p style="font-size: 0.85rem; color: #9ca3af; margin-bottom: 16px; flex: 1;">${book.resumen}</p>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08);">
          <span style="font-size: 1.3rem; font-weight: 800; color: #38bdf8;">$${book.precio_usd.toFixed(2)} USD</span>
          <span style="font-size: 0.95rem; font-weight: 700; color: #10b981;">$${book.precio_ars.toLocaleString('es-AR')} ARS</span>
        </div>

        <div style="display: flex; flex-direction: column; gap: 8px;">
          <a href="${book.link_arg}" target="_blank" style="background: linear-gradient(135deg, #10b981, #059669); color: #fff; text-decoration: none; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; font-size: 0.85rem;">
            🇦🇷 Comprar en Pesos
          </a>
          <a href="${book.link_int}" target="_blank" style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff; text-decoration: none; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; font-size: 0.85rem;">
            🌎 Comprar en Dólares
          </a>
        </div>
      </div>
    </div>
  `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
  renderBooks();

  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      renderBooks('all', e.target.value);
    });
  }

  const categoryButtons = document.querySelectorAll('.cat-btn');
  categoryButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      categoryButtons.forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      const category = e.target.dataset.category || 'all';
      renderBooks(category, searchInput ? searchInput.value : '');
    });
  });
});
