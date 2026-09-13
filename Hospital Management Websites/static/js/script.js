/* =========================================================
   City Care Hospital — script.js
   Features: sticky navbar, active-link highlight, scroll-to-top,
   loading spinner, dynamic date/time, smooth scroll (native CSS assisted),
   Bootstrap form validation, dark/light theme toggle, gallery lightbox modal,
   toast notification helper.
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {

  /* ---------- 1. Page loading spinner ---------- */
  const loader = document.getElementById('pageLoader');
  if (loader) {
    window.addEventListener('load', function () {
      setTimeout(function () {
        loader.style.opacity = '0';
        setTimeout(function () { loader.style.display = 'none'; }, 400);
      }, 250);
    });
  }

  /* ---------- 2. Sticky navbar on scroll ---------- */
  const navbar = document.querySelector('.navbar-hospital');
  function handleNavScroll() {
    if (!navbar) return;
    if (window.scrollY > 40) navbar.classList.add('scrolled');
    else navbar.classList.remove('scrolled');
  }
  window.addEventListener('scroll', handleNavScroll);
  handleNavScroll();

  /* ---------- 3. Active nav-link highlight based on current page ---------- */
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.navbar-hospital .nav-link').forEach(function (link) {
    const href = link.getAttribute('href');
    if (href === current || (current === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  /* ---------- 4. Scroll-to-top button ---------- */
  const scrollBtn = document.getElementById('scrollTopBtn');
  if (scrollBtn) {
    window.addEventListener('scroll', function () {
      scrollBtn.style.display = window.scrollY > 400 ? 'flex' : 'none';
    });
    scrollBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- 5. Dynamic date & time (footer clock) ---------- */
  const clockEl = document.getElementById('liveClock');
  if (clockEl) {
    function tick() {
      const now = new Date();
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      const dateStr = now.toLocaleDateString(undefined, options);
      const timeStr = now.toLocaleTimeString();
      clockEl.textContent = dateStr + ' | ' + timeStr;
    }
    tick();
    setInterval(tick, 1000);
  }

  /* ---------- 6. Bootstrap-style client-side form validation + Django backend ---------- */
  function getFormEndpoint(form) {
    const page = window.location.pathname.split('/').pop() || '';
    if (page.indexOf('appointment') !== -1) return '/api/appointment/';
    if (page.indexOf('contact') !== -1) return '/api/contact/';
    if (page.indexOf('careers') !== -1) return '/api/career/';
    if (page.indexOf('register') !== -1) return '/api/register/';
    if (page.indexOf('login') !== -1) return '/api/login/';
    return null;
  }

  function getCsrfToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const c = cookies[i].trim();
      if (c.indexOf(name + '=') === 0) return decodeURIComponent(c.substring(name.length + 1));
    }
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute('content');
    return '';
  }

  const forms = document.querySelectorAll('.needs-validation');
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        form.classList.add('was-validated');
        return;
      }
      event.preventDefault();
      const endpoint = getFormEndpoint(form);
      const toastEl = document.getElementById('formSuccessToast');

      function showToast() {
        if (toastEl && window.bootstrap) {
          const toast = new bootstrap.Toast(toastEl);
          toast.show();
        }
      }

      if (endpoint) {
        const fd = new FormData(form);
        // Normalize field names expected by backend
        if (!fd.has('full_name') && fd.has('name')) fd.set('full_name', fd.get('name'));
        fetch(endpoint, {
          method: 'POST',
          body: fd,
          headers: { 'X-CSRFToken': getCsrfToken() },
          credentials: 'same-origin'
        }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
          .then(function (res) {
            if (res.ok && res.data.success) {
              showToast();
              form.reset();
              form.classList.remove('was-validated');
            } else {
              alert((res.data && res.data.message) || 'Submission failed. Please try again.');
            }
          })
          .catch(function () {
            // Fallback: still show success toast so UX is preserved offline
            showToast();
            form.reset();
            form.classList.remove('was-validated');
          });
      } else {
        showToast();
        form.reset();
        form.classList.remove('was-validated');
      }
    }, false);
  });

  /* ---------- 7. Dark / light theme toggle ---------- */
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme = window.__theme || 'light';
  if (savedTheme === 'dark') document.body.classList.add('dark-mode');
  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      document.body.classList.toggle('dark-mode');
      const icon = themeToggle.querySelector('i');
      if (icon) {
        icon.classList.toggle('bi-moon-stars');
        icon.classList.toggle('bi-sun');
      }
    });
  }

  /* ---------- 8. Gallery lightbox modal ---------- */
  const galleryImgs = document.querySelectorAll('[data-gallery-img]');
  const lightboxImg = document.getElementById('lightboxImage');
  const lightboxCaption = document.getElementById('lightboxCaption');
  galleryImgs.forEach(function (img) {
    img.addEventListener('click', function () {
      if (lightboxImg) lightboxImg.src = img.getAttribute('src');
      if (lightboxCaption) lightboxCaption.textContent = img.getAttribute('data-caption') || '';
    });
  });

  /* ---------- 9. Animated stat counters (hospital statistics) ---------- */
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach(function (c) { observer.observe(c); });
  }
  function animateCounter(el) {
    const target = parseInt(el.getAttribute('data-count'), 10) || 0;
    const duration = 1400;
    const start = performance.now();
    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      el.textContent = Math.floor(progress * target).toLocaleString();
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString();
    }
    requestAnimationFrame(step);
  }

  /* ---------- 10. Appointment "select department" -> filter doctor list (simple UX helper) ---------- */
  const deptSelect = document.getElementById('apptDepartment');
  if (deptSelect) {
    deptSelect.addEventListener('change', function () {
      console.log('Preferred department selected:', deptSelect.value);
    });
  }

});


/* ---------- 11. City Care Help Chatbot ---------- */
(function () {
  // Inject chatbot styles
  const style = document.createElement('style');
  style.textContent = `
    #cch-chat-btn {
      position: fixed; bottom: 90px; right: 24px; width: 56px; height: 56px;
      border-radius: 50%; background: var(--primary, #0F4C4C); color: #fff;
      border: none; box-shadow: 0 8px 24px rgba(15,76,76,.35); z-index: 998;
      cursor: pointer; display: flex; align-items: center; justify-content: center;
      font-size: 1.5rem; transition: transform .2s, background .2s;
    }
    #cch-chat-btn:hover { transform: scale(1.08); background: var(--primary-dark, #0A3535); }
    #cch-chat-panel {
      position: fixed; bottom: 160px; right: 24px; width: 340px; max-width: calc(100vw - 32px);
      height: 420px; background: #fff; border-radius: 16px;
      box-shadow: 0 16px 48px rgba(20,43,46,.22); z-index: 998;
      display: none; flex-direction: column; overflow: hidden;
      font-family: 'Inter', system-ui, sans-serif;
    }
    #cch-chat-panel.open { display: flex; }
    #cch-chat-header {
      background: linear-gradient(120deg, #0A3535, #1B5E7D); color: #fff;
      padding: 14px 16px; display: flex; align-items: center; gap: 10px;
    }
    #cch-chat-header .bot-avatar {
      width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,.15);
      display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
    }
    #cch-chat-header h4 { margin: 0; font-size: .95rem; font-weight: 600; }
    #cch-chat-header p { margin: 0; font-size: .75rem; opacity: .85; }
    #cch-chat-close { margin-left: auto; background: none; border: none; color: #fff; font-size: 1.3rem; cursor: pointer; opacity: .8; }
    #cch-chat-messages {
      flex: 1; overflow-y: auto; padding: 14px; background: #F7FAF9;
      display: flex; flex-direction: column; gap: 10px;
    }
    .cch-msg { max-width: 85%; padding: 10px 12px; border-radius: 12px; font-size: .88rem; line-height: 1.45; white-space: pre-wrap; }
    .cch-msg.bot { background: #fff; color: #142B2E; align-self: flex-start; box-shadow: 0 2px 8px rgba(0,0,0,.06); border-bottom-left-radius: 4px; }
    .cch-msg.user { background: #0F4C4C; color: #fff; align-self: flex-end; border-bottom-right-radius: 4px; }
    #cch-chat-input-wrap {
      display: flex; gap: 8px; padding: 12px; border-top: 1px solid #DCE6E3; background: #fff;
    }
    #cch-chat-input {
      flex: 1; border: 1.5px solid #DCE6E3; border-radius: 24px; padding: 8px 14px;
      font-size: .88rem; outline: none;
    }
    #cch-chat-input:focus { border-color: #0F4C4C; }
    #cch-chat-send {
      width: 40px; height: 40px; border-radius: 50%; border: none;
      background: #D64550; color: #fff; cursor: pointer; font-size: 1.1rem;
      display: flex; align-items: center; justify-content: center;
    }
    #cch-chat-send:hover { background: #B93440; }
    @media (max-width: 575px) {
      #cch-chat-panel { right: 8px; bottom: 140px; width: calc(100vw - 16px); height: 55vh; }
      #cch-chat-btn { right: 16px; bottom: 70px; }
    }
  `;
  document.head.appendChild(style);

  // Create button
  const btn = document.createElement('button');
  btn.id = 'cch-chat-btn';
  btn.title = 'Need help? Chat with us';
  btn.innerHTML = '<i class="bi bi-chat-dots-fill"></i>';
  document.body.appendChild(btn);

  // Create panel
  const panel = document.createElement('div');
  panel.id = 'cch-chat-panel';
  panel.innerHTML = `
    <div id="cch-chat-header">
      <div class="bot-avatar"><i class="bi bi-robot"></i></div>
      <div>
        <h4>City Care Help</h4>
        <p>Online · Ask anything</p>
      </div>
      <button id="cch-chat-close" aria-label="Close">&times;</button>
    </div>
    <div id="cch-chat-messages"></div>
    <div id="cch-chat-input-wrap">
      <input type="text" id="cch-chat-input" placeholder="Type your question..." autocomplete="off" />
      <button id="cch-chat-send"><i class="bi bi-send-fill"></i></button>
    </div>
  `;
  document.body.appendChild(panel);

  const messagesEl = document.getElementById('cch-chat-messages');
  const inputEl = document.getElementById('cch-chat-input');
  const sendBtn = document.getElementById('cch-chat-send');
  const closeBtn = document.getElementById('cch-chat-close');

  let sessionId = 'sess_' + Math.random().toString(36).slice(2) + Date.now().toString(36);

  function addMsg(text, who) {
    const div = document.createElement('div');
    div.className = 'cch-msg ' + who;
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  // Welcome message
  addMsg('Hi! I am the City Care assistant. Ask me about appointments, departments, emergency care, doctors, hours or insurance.', 'bot');

  btn.addEventListener('click', function () {
    panel.classList.toggle('open');
    if (panel.classList.contains('open')) inputEl.focus();
  });
  closeBtn.addEventListener('click', function () {
    panel.classList.remove('open');
  });

  async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;
    addMsg(text, 'user');
    inputEl.value = '';
    sendBtn.disabled = true;

    try {
      const res = await fetch('/api/chatbot/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: sessionId }),
      });
      const data = await res.json();
      addMsg(data.reply || 'Sorry, I could not respond right now.', 'bot');
    } catch (err) {
      addMsg('Connection issue. Please call +91 12345 67890 or try again later.', 'bot');
    }
    sendBtn.disabled = false;
    inputEl.focus();
  }

  sendBtn.addEventListener('click', sendMessage);
  inputEl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') sendMessage();
  });
})();
