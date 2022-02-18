import {
  sendRequest,
  ENDPOINT_URL,
  copyToClipBoard,
  wait,
  buildSpanTag,
} from './module/helper.js';

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

const buildEditButton = function (url) {
  return `
  <div class="snippet-action-div text-center mt-5">
    <a href="${url.original_url}edit" class="btn btn-primary w-50" style="font-size:1.1rem"><i class="fa fa-pencil mr-3"></i>EDIT</a>
  </div>
  `;
};

const buildSnippetDetailMarkup = function (is_other_user, data) {
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
        <p>
          <a href="${data.urls.original_url}">${data.urls.original_url}</a>
        </p>
      </div>
      <div>
        <span class="font-weight-bold">Shorten URL</span>
        <p>
          <a href="${data.urls.shorten_url}">${data.urls.shorten_url}</a>
          <button class="btn btn-info ml-3 copy-btn" data-val="${
            data.urls.shorten_url
          }"><i class="fa fa-clipboard"></i></button>
        </p>
      </div>
    </div>
  </div>

  <div class="url-wrapper border">
    <h5 class="font-weight-bolder mb-4">Expiration Details</h5>
    <div class="url-div">
      <div>
        ${
          data.has_expiry
            ? data.expiration_date
              ? buildSpanTag(2, data.expiration_date)
              : buildSpanTag(1, data.created_at)
            : buildSpanTag(0)
        }
      </div>
    </div>
  </div>

  ${is_other_user ? '' : buildEditButton(data.urls)}

  <div class="snippet-action-div text-center mt-5">
    <a href="/snippet/${
      data.id
    }/statistics/" class="btn btn-warning" style="font-size:1.1rem; width: 65%"><i class="fa fa-bar-chart mr-3"></i>STATISTICS</a>
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
  const is_other_user = data.is_other_user;
  const res_data = data.data;

  const markup = buildSnippetDetailMarkup(is_other_user, res_data);
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
    console.error(err);
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

  showContent(response);

  if (response.data.is_encrypted) {
    const decryptBtn = document.getElementById('decrypt-btn');
    decryptBtn.addEventListener('click', addHandlerToDecryptBtn);
  }

  const copyBtn = document.querySelector('.copy-btn');
  copyBtn.addEventListener('click', async e => {
    const elem = e.currentTarget;
    copyToClipBoard(elem.dataset.val);

    elem.innerHTML = '<i class="fa fa-check"></i>';
    await wait(1);
    elem.innerHTML = '<i class="fa fa-clipboard"></i>';
  });
};

fetchSnippetDetail();
