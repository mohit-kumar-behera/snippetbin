import {
  addLoader,
  wait,
  removeLoader,
  RES_PER_PAGE,
  ENDPOINT_URL,
} from './module/helper.js';

const snippetsWrapper = document.querySelector('.snippets-wrapper');
const loadMoreDiv = document.querySelector('.load-more-btn-div');

const buildLoadMoreButton = function () {
  return `
    <button type="button" class="btn btn-primary d-flex justify-content-center load-more-btn" data-setnum="1">
      <span>LOAD MORE SNIPPETS</span>
      <div class="spinner"></div>
    </button>
  `;
};

const buildHourGlassIcon = function () {
  return `
  <div class="card-right-content"><a style="color: #fff"><i class="fa fa-hourglass-end" style="font-size:0.75rem"></i></a></div>
  `;
};

const buildSnippetCard = function (snippet) {
  let has_expired = snippet.has_expired;

  return `
  <div class="snippet-card ${has_expired ? 'fade-down' : ''}">
    <div class="card-left-content">
      <div class="upper-content">
        ${snippet.is_encrypted ? '<i class="fa fa-lock mr-2"></i>' : ''}
        <a href="${snippet.urls.original_url}" class="snippet-title">${
    snippet.title
  }</a>
      </div>
      <div class="lower-content">
        <span>${snippet.user.username}</span>
        <span>${snippet.datetime}</span>
      </div>
    </div>
    ${has_expired ? buildHourGlassIcon() : ''}
  </div>
  `;
};

const buildSnippetsMarkup = function (snippets) {
  return `
    ${snippets.map(snippet => buildSnippetCard(snippet)).join('')}
  `;
};

const fetchList = async function (setnum = 1) {
  const start = (setnum - 1) * RES_PER_PAGE;
  const end = setnum * RES_PER_PAGE;

  let url = new URL(`${ENDPOINT_URL}/api/snippet`);
  let params = { start, end };
  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

  let response = null;
  try {
    const res = await fetch(url.href);
    response = await res.json();
  } catch (err) {
    alert('Sorry, something went wrong');
  }

  return response;
};

const appendContent = function (data) {
  const markup = buildSnippetsMarkup(data);
  snippetsWrapper.insertAdjacentHTML('beforeend', markup);
};

const handlerLoadMoreSnippets = async function (e) {
  const btn = e.currentTarget;
  addLoader(btn);

  let setnum = +btn.dataset.setnum;
  setnum++;

  const response = await fetchList(setnum);

  if (!response.success) return alert('Sorry, Something went wrong');

  btn.setAttribute('data-setnum', setnum);

  const res_data = await response.data;

  if (res_data.length) {
    appendContent(res_data);
    await wait(0.5);
    removeLoader(btn, '<span>LOAD MORE</span>');
  } else {
    await wait(1);
    btn.remove();
  }
};

const showContent = function (data) {
  let markup = '';
  if (!data.length)
    markup = '<h4 class="text-muted">Currently there are no snippets</h4>';
  else markup = buildSnippetsMarkup(data);
  snippetsWrapper.innerHTML = '';
  snippetsWrapper.insertAdjacentHTML('afterbegin', markup);
};

const showLoadMoreBtn = function (data_len) {
  if (data_len < RES_PER_PAGE) return;
  const markup = buildLoadMoreButton();
  loadMoreDiv.innerHTML = '';
  loadMoreDiv.insertAdjacentHTML('afterbegin', markup);

  loadMoreDiv
    .querySelector('.load-more-btn')
    .addEventListener('click', function (e) {
      handlerLoadMoreSnippets(e);
    });
};

const fetchSnippetList = async function () {
  const response = await fetchList();

  showContent(response.data);
  showLoadMoreBtn(response.data.length);
};

fetchSnippetList();
