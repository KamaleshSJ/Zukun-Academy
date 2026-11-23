(function () {
  const embedScript = document.currentScript;
  const scriptUrl = new URL(embedScript.src, window.location.href);
  const baseUrl = new URL('../', scriptUrl);
  const widgetUrl = new URL(embedScript.dataset.chatUrl || 'widget.html', baseUrl);
  const logoUrl = new URL('assets/zukun-logo.png', baseUrl);
  const style = document.createElement('style');
  style.textContent = `
    #zukun-chat-launcher { position: fixed; right: 24px; bottom: 24px; z-index: 2147483647; display: grid; width: 64px; height: 64px; place-items: center; padding: 0; border: 3px solid #fff; border-radius: 50%; background: linear-gradient(135deg,#3218df,#b000e7); box-shadow: 0 8px 28px #26133e4a; cursor: pointer; transition: transform .16s ease, box-shadow .16s ease; }
    #zukun-chat-launcher:hover { transform: translateY(-2px); box-shadow: 0 12px 32px #26133e5c; }
    #zukun-chat-launcher img { display: block; width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }
    #zukun-chat-panel { position: fixed; right: 24px; bottom: 100px; z-index: 2147483646; width: min(390px, calc(100vw - 32px)); height: min(650px, calc(100vh - 124px)); height: min(650px, calc(100dvh - 124px)); overflow: hidden; border: 0; border-radius: 21px; background: transparent; box-shadow: 0 18px 60px #24113f40; }
    #zukun-chat-panel[hidden] { display: none; }
    #zukun-chat-panel iframe { display: block; width: 100%; height: 100%; border: 0; border-radius: inherit; background: #fff; }
    @media (max-width: 520px) { #zukun-chat-launcher { right: 16px; bottom: 16px; width: 58px; height: 58px; } #zukun-chat-panel { inset: 8px; width: auto; height: auto; border-radius: 18px; } }
    @media (prefers-reduced-motion: reduce) { #zukun-chat-launcher { transition: none; } }
  `;
  document.head.appendChild(style);

  const launcher = document.createElement('button');
  launcher.id = 'zukun-chat-launcher';
  launcher.type = 'button';
  launcher.setAttribute('aria-label', 'Open Zukun Academy chat');
  launcher.setAttribute('aria-expanded', 'false');
  launcher.setAttribute('aria-haspopup', 'dialog');
  launcher.title = 'Chat with Zukun Academy';
  const logo = document.createElement('img');
  logo.src = logoUrl.href;
  logo.alt = '';
  launcher.appendChild(logo);

  const panel = document.createElement('div');
  panel.id = 'zukun-chat-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'Chat with Zukun Academy');
  panel.hidden = true;
  const frame = document.createElement('iframe');
  frame.title = 'Zukun Academy student assistant';
  frame.src = widgetUrl.href;
  frame.loading = 'lazy';
  panel.appendChild(frame);
  document.body.append(launcher, panel);

  function setOpen(open) {
    panel.hidden = !open;
    launcher.hidden = open;
    launcher.setAttribute('aria-expanded', String(open));
    launcher.setAttribute('aria-label', open ? 'Close Zukun Academy chat' : 'Open Zukun Academy chat');
    try { window.sessionStorage.setItem('zukun-chat-open', String(open)); } catch (_) {}
    if (open) frame.focus();
  }

  launcher.addEventListener('click', () => setOpen(panel.hidden));
  window.addEventListener('message', event => {
    if (event.source === frame.contentWindow && event.origin === widgetUrl.origin && event.data?.type === 'zukun-widget-close') setOpen(false);
  });
  window.ZukunAcademyChat = { open: () => setOpen(true), close: () => setOpen(false), toggle: () => setOpen(panel.hidden) };
  try { if (window.sessionStorage.getItem('zukun-chat-open') === 'true') setOpen(true); } catch (_) {}
})();
