const snippetsWrapper = document.querySelector('.snippets-wrapper');

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

const showContent = function (data) {
  const markup = buildSnippetsMarkup(data);
  snippetsWrapper.innerHTML = '';
  snippetsWrapper.insertAdjacentHTML('afterbegin', markup);
};

const fetchSnippetList = async function () {
  const url = `/api/snippet`;

  let response = null;
  try {
    const res = await fetch(url);
    response = await res.json();
  } catch (err) {
    showError('Sorry, Something went wrong');
  }

  showContent(response.data);
};

fetchSnippetList();
