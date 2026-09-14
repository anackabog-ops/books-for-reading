const $ = id => document.getElementById(id);
let data, manifest = {}, topic = 'all', queue = [], history = [], cursor = -1, current = null;
let audio = null, speaking = false, playbackToken = 0, imageToken = 0, toastTimer;
let dbPromise, imageURL = null;
const storageKey = 'anacka-conversations-v1';
let saved = {favorites: [], review: [], answers: {}};
try {
  const value = JSON.parse(localStorage.getItem(storageKey) || 'null');
  if (value && Array.isArray(value.favorites) && Array.isArray(value.review) && typeof value.answers === 'object' && value.answers !== null) saved = value;
} catch { /* Keep a usable session when storage is blocked. */ }
function notify(message) {
  $('toast').textContent = message; $('toast').hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => $('toast').hidden = true, 4000);
}
function persist() {
  try { localStorage.setItem(storageKey, JSON.stringify(saved)); }
  catch { notify('Браузер не сохранил изменения. Они доступны до закрытия страницы.'); }
}
function shuffled(items) {
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [out[i], out[j]] = [out[j], out[i]]; }
  return out;
}
function pool() {
  return data.questions.filter(q => (topic === 'all' || q.topic === topic) && ($('level').value === 'all' || q.level === $('level').value) && ($('collection').value === 'all' || saved[$('collection').value].includes(q.id)));
}
function sprite(t) {
  const [x,y,w,h] = t.region;
  const node = document.createElement('div'); node.className = 'sprite'; node.style.aspectRatio = `${w} / ${h}`;
  const img = document.createElement('img'); img.src = 'assets/stickers.webp'; img.alt = ''; img.draggable = false;
  img.style.cssText = `width:${1536/w*100}%;height:${1024/h*100}%;left:${-x/w*100}%;top:${-y/h*100}%`;
  node.append(img); return node;
}
function renderTopics() {
  $('topics').replaceChildren();
  [{id:'all',ru:'Все темы',lt:'Visos temos'}, ...data.topics].forEach(t => {
    const button = document.createElement('button'); button.className = 'topic'; button.dataset.topic = t.id;
    button.setAttribute('aria-pressed', String(topic === t.id));
    const thumb = document.createElement('span'); thumb.setAttribute('aria-hidden', 'true');
    if (t.id === 'all') { thumb.className = 'all-icon'; thumb.textContent = '▤'; }
    else { thumb.className = 'topic-thumb'; thumb.append(sprite(t)); }
    const words = document.createElement('span'); words.className = 'topic-words'; words.textContent = t.ru;
    const lt = document.createElement('small'); lt.lang = 'lt'; lt.textContent = t.lt; words.append(lt);
    const count = document.createElement('span'); count.className = 'topic-count'; count.textContent = t.id === 'all' ? '100' : '10';
    button.append(thumb,words,count);
    button.onclick = () => { topic = t.id; renderTopics(); reset(); };
    $('topics').append(button);
  });
}
function reset() {
  stopAudio(); history = []; cursor = -1; queue = shuffled(pool()); current = null;
  if (!queue.length) { renderEmpty(); return; }
  next();
}
function next() {
  if (cursor < history.length - 1) cursor++;
  else if (queue.length) { history.push(queue.pop()); cursor++; }
  else { reset(); notify('Новый круг: колода перемешана.'); return; }
  current = history[cursor]; render();
}
function renderEmpty() {
  imageToken++; stopAudio(); current = null;
  $('card').hidden = true; $('empty').hidden = false;
  $('next').disabled = true; $('previous').disabled = true; $('images-open').disabled = true;
  $('progress-text').textContent = '0 вопросов'; $('progress').value = 0; $('progress').max = 1;
  $('deck-note').textContent = 'Выбери другую тему, уровень или коллекцию.';
}
function render() {
  stopAudio(); $('card').hidden = false; $('empty').hidden = true;
  $('next').disabled = false; $('images-open').disabled = false;
  const t = data.topics.find(t => t.id === current.topic);
  $('topic-label').textContent = `${t.lt} · ${t.ru}`;
  $('question-level').textContent = current.level; $('question-id').textContent = `№ ${Number(current.id.slice(1))}`;
  $('question').textContent = current.lt; $('translation').textContent = current.ru;
  $('hint-lt').textContent = current.hint; $('hint-ru').textContent = current.hintRu;
  $('translation').hidden = true; $('translate').setAttribute('aria-expanded','false'); $('translate').textContent = 'Показать перевод';
  $('hint').hidden = true; $('hint-toggle').setAttribute('aria-expanded','false'); $('hint-toggle').lastElementChild.textContent = '＋';
  document.querySelector('.answer').open = false; $('answer').value = saved.answers[current.id] || '';
  updateMarks(); updateNavigation(); updateAudio(); renderImage();
  $('card').classList.remove('dealt'); void $('card').offsetWidth; $('card').classList.add('dealt');
}
function updateMarks() {
  const favorite = saved.favorites.includes(current.id), review = saved.review.includes(current.id);
  $('favorite').textContent = favorite ? '★' : '☆'; $('favorite').setAttribute('aria-pressed', String(favorite));
  $('favorite').setAttribute('aria-label', favorite ? 'Убрать из избранного' : 'В избранное');
  $('review').setAttribute('aria-pressed',String(review)); $('review').textContent = review ? '✓ Отложено для повторения' : '＋ Повторить позже';
}
function updateNavigation() {
  const total = history.length + queue.length;
  $('previous').disabled = cursor <= 0;
  $('progress-text').textContent = `${cursor + 1} / ${total}`;
  $('progress').max = total; $('progress').value = history.length;
  $('seen').textContent = `Открыто ${history.length} из ${total}`;
  const finished = cursor === history.length - 1 && !queue.length;
  $('next').textContent = finished ? 'Новый круг ↻' : 'Следующий вопрос →';
  $('deck-note').textContent = finished ? 'Все вопросы этой колоды открыты. Можно начать новый круг.' : 'Карточки не повторяются, пока не закончится колода.';
}
function toggleMark(name) {
  const id = current.id, exists = saved[name].includes(id);
  saved[name] = exists ? saved[name].filter(x => x !== id) : [...saved[name],id]; persist();
  if (exists && $('collection').value === name) {
    // Remove only this card, preserving the remaining shuffled order and history.
    history = history.filter(q => q.id !== id); queue = queue.filter(q => q.id !== id);
    if (!history.length && !queue.length) { renderEmpty(); return; }
    cursor = Math.min(cursor, history.length - 1);
    if (cursor < 0) next(); else { current = history[cursor]; render(); }
  } else updateMarks();
}
function voice() { return window.speechSynthesis?.getVoices().find(v => /^lt(?:-|_)?/i.test(v.lang)); }
function audioPath() {
  const entry = current && manifest[current.id];
  return entry && entry.text === current.lt && /^assets\/audio\/q\d{3}-[a-f0-9]+\.mp3$/.test(entry.file) ? entry.file : null;
}
function updateAudio() {
  if (!current) return;
  const hasFile = Boolean(audioPath()), hasVoice = Boolean(voice());
  $('listen').disabled = !hasFile && !hasVoice; $('speed').disabled = !hasFile && !hasVoice;
  $('listen').textContent = speaking ? '■ Остановить' : '▷ Послушать';
  $('audio-status').textContent = hasFile ? 'Запись Azure · литовский' : hasVoice ? 'Литовский голос устройства' : 'Запись ещё не добавлена. На устройстве нет литовского голоса.';
}
function stopAudio() {
  playbackToken++; if (audio) { audio.pause(); audio = null; }
  if (window.speechSynthesis) window.speechSynthesis.cancel(); speaking = false;
  if (current) updateAudio();
}
async function play() {
  if (speaking) { stopAudio(); return; }
  stopAudio(); const token = playbackToken; const path = audioPath();
  speaking = true; updateAudio();
  const done = () => { if (token === playbackToken) { speaking = false; updateAudio(); } };
  if (path) {
    audio = new Audio(path); audio.playbackRate = Number($('speed').value); audio.onended = done;
    audio.onerror = () => { if (token !== playbackToken) return; done(); $('audio-status').textContent = 'Не удалось загрузить запись. Проверь соединение и повтори.'; };
    try { await audio.play(); } catch { if (token === playbackToken) { done(); $('audio-status').textContent = 'Браузер не запустил звук. Нажми «Послушать» ещё раз.'; } }
  } else {
    const selected = voice(); if (!selected) { done(); return; }
    const utterance = new SpeechSynthesisUtterance(current.lt); utterance.lang = 'lt-LT'; utterance.voice = selected; utterance.rate = Number($('speed').value);
    utterance.onend = done; utterance.onerror = event => { if (token !== playbackToken) return; done(); if (event.error !== 'canceled' && event.error !== 'interrupted') $('audio-status').textContent = 'Голос устройства недоступен. Попробуй другой браузер.'; };
    window.speechSynthesis.speak(utterance);
  }
}
function database() {
  if (!dbPromise) dbPromise = new Promise((resolve,reject) => {
    const request = indexedDB.open('anacka-conversation-images',1);
    request.onupgradeneeded = () => request.result.createObjectStore('images');
    request.onsuccess = () => resolve(request.result); request.onerror = () => reject(request.error);
  });
  return dbPromise;
}
async function imageStore(operation,key,value) {
  const db = await database();
  return new Promise((resolve,reject) => {
    const tx = db.transaction('images',operation === 'get' ? 'readonly' : 'readwrite');
    const store = tx.objectStore('images'); const request = operation === 'put' ? store.put(value,key) : store[operation](key);
    tx.oncomplete = () => resolve(request.result); tx.onerror = () => reject(tx.error); tx.onabort = () => reject(tx.error);
  });
}
async function renderImage() {
  const token = ++imageToken, q = current, t = data.topics.find(t => t.id === q.topic);
  if (imageURL) { URL.revokeObjectURL(imageURL); imageURL = null; }
  $('illustration').replaceChildren(sprite(t));
  try {
    const image = await imageStore('get',q.id) || await imageStore('get',`topic:${q.topic}`);
    if (token !== imageToken || !image) return;
    imageURL = URL.createObjectURL(image); const img = document.createElement('img'); img.src = imageURL; img.alt = ''; img.className = 'custom-image';
    $('illustration').replaceChildren(img);
  } catch { /* Default art still works if IndexedDB is unavailable. */ }
}
function targetKey() { return $('image-target').value === 'question' ? current.id : `topic:${current.topic}`; }
$('translate').onclick = () => { const open = $('translation').hidden; $('translation').hidden = !open; $('translate').setAttribute('aria-expanded',String(open)); $('translate').textContent = open ? 'Скрыть перевод' : 'Показать перевод'; };
$('hint-toggle').onclick = () => { const open = $('hint').hidden; $('hint').hidden = !open; $('hint-toggle').setAttribute('aria-expanded',String(open)); $('hint-toggle').lastElementChild.textContent = open ? '−' : '＋'; };
$('next').onclick = next;
$('previous').onclick = () => { if (cursor > 0) { cursor--; current = history[cursor]; render(); } };
$('shuffle').onclick = () => { reset(); notify('Колода перемешана.'); };
$('level').onchange = reset; $('collection').onchange = reset;
$('show-all').onclick = () => { topic = 'all'; $('level').value = 'all'; $('collection').value = 'all'; renderTopics(); reset(); };
$('favorite').onclick = () => toggleMark('favorites'); $('review').onclick = () => toggleMark('review');
$('answer').oninput = () => { saved.answers[current.id] = $('answer').value; persist(); };
$('listen').onclick = play; $('speed').onchange = () => { if (speaking) stopAudio(); };
window.speechSynthesis?.addEventListener('voiceschanged',updateAudio);
window.addEventListener('pagehide',stopAudio);
$('images-open').onclick = () => { $('image-feedback').textContent = ''; $('images-dialog').showModal(); };
$('image-file').onchange = async () => {
  const file = $('image-file').files[0]; if (!file) return;
  if (!['image/png','image/jpeg','image/webp'].includes(file.type) || file.size > 8*1024*1024) { $('image-feedback').textContent = 'Выбери PNG, JPG или WebP размером до 8 МБ.'; return; }
  const key = targetKey();
  try {
    const bitmap = await createImageBitmap(file); bitmap.close();
    await imageStore('put',key,file); await renderImage(); $('image-feedback').textContent = 'Картинка сохранена в этом браузере.';
  } catch { $('image-feedback').textContent = 'Не удалось сохранить картинку. Проверь файл и разрешение браузера на хранение данных.'; }
  $('image-file').value = '';
};
$('image-remove').onclick = async () => {
  try { await imageStore('delete',targetKey()); await renderImage(); $('image-feedback').textContent = 'Своя картинка для выбранного места удалена.'; }
  catch { $('image-feedback').textContent = 'Не удалось изменить сохранённые картинки.'; }
};
async function start() {
  try {
    const results = await Promise.all([fetch('questions.json').then(r => { if (!r.ok) throw new Error(); return r.json(); }), fetch('audio.json').then(r => r.ok ? r.json() : {}).catch(() => ({}))]);
    data = results[0]; manifest = results[1];
    if (!Array.isArray(data.questions) || data.questions.length !== 100) throw new Error();
    $('loading').hidden = true; $('workspace').hidden = false; renderTopics(); reset();
  } catch { $('loading').textContent = 'Не удалось открыть вопросы. Обнови страницу или проверь соединение.'; }
}
start();
