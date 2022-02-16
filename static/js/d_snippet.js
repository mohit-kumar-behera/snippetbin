import { sendRequest, ENDPOINT_URL } from './module/helper.js';

const snippetDetailWrapper = document.querySelector('.snippet-detail-div');

const buildDecryptInputElem = function () {
  return `
  <div class="input-group w-50">
    <input type="text" class="form-control decrypt-input" placeholder="Password Key" id="decrypt-input">
    <div class="input-group-append">
      <button class="input-group-text btn decrypt-btn" id="decrypt-btn">Decrypt</button>
    </div>
  </div>
  `;
};

const buildSnippetDetailMarkup = function (data) {
  return `
  <div class="snippet-card">
    <div class="card-left-content">
      <div class="upper-content">
        <h5 class="snippet-title">${data.title}</h5>
      </div>
      <div class="lower-content">
        <small>${data.user.username}</small>
        <small>${data.datetime}</small>
      </div>
    </div>
  </div>

  <div class="snippet-box">
    <h5 class="font-weight-bolder mb-4">Snippet</h5>
    <pre class="text-light">${data.snippet}</pre>
  </div>

  ${data.is_encrypted ? buildDecryptInputElem() : ''}

  <div class="url-wrapper border">
    <h5 class="font-weight-bolder mb-4">URLS</h5>
    <div class="url-div">
      <div>
        <span class="font-weight-bold">Original URL</span>
        <a href="${data.urls.original_url}">${data.urls.original_url}</a>
      </div>
      <div>
        <span class="font-weight-bold">Shorten URL</span>
        <a href="${data.urls.shorten_url}">${data.urls.shorten_url}</a>
      </div>
    </div>
  </div>
  `;
};

const buildErrorMarkup = function (err) {
  return `
  <div class="error">
    <i class="fa fa-exclamation-triangle"></i>
    <h4 class="error-message">${err}</h4>
  </div>
  `;
};

const showError = function (err) {
  const markup = buildErrorMarkup(err);
  snippetDetailWrapper.innerHTML = '';
  snippetDetailWrapper.insertAdjacentHTML('afterbegin', markup);
};

const showContent = function (data) {
  const markup = buildSnippetDetailMarkup(data);
  snippetDetailWrapper.innerHTML = '';
  snippetDetailWrapper.insertAdjacentHTML('afterbegin', markup);
};

const addHandlerToDecryptBtn = async function () {
  const snippetBox = document.querySelector('.snippet-box');
  const snippetBoxPreTag = snippetBox.querySelector('pre');
  const decryptInput = document.getElementById('decrypt-input');

  if (!decryptInput.value) return;

  const data = {
    data: snippetBoxPreTag.textContent,
    key: decryptInput.value,
  };

  const url = `${ENDPOINT_URL}/api/snippet/decrypt/`;
  let response = null;
  try {
    response = await sendRequest(url, data);
  } catch (err) {
    console.error(error);
    alert('Something went wrong');
  }

  if (!response.success) return alert(response.data.error);

  snippetBoxPreTag.innerHTML = '';
  snippetBoxPreTag.insertAdjacentHTML('afterbegin', response.data.snippet);
};

const fetchSnippetDetail = async function () {
  const snippet_id = location.pathname.split('/')[2];
  const url = `/api/snippet/v/${snippet_id}`;

  let response = null;
  try {
    const res = await fetch(url);
    response = await res.json();
  } catch (err) {
    showError('Sorry, Something went wrong');
  }

  if (!response.success) return showError(response.data.error);

  showContent(response.data);

  if (response.data.is_encrypted) {
    const decryptBtn = document.getElementById('decrypt-btn');
    decryptBtn.addEventListener('click', addHandlerToDecryptBtn);
  }
};

fetchSnippetDetail();
