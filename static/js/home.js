const snippetsWrapper = document.querySelector('.snippets-wrapper');

const buildSnippetCard = function (snippet) {
  return `
  <div class="snippet-card">
    <div class="card-left-content">
      <div class="upper-content">
        <a href="${snippet.urls.original_url}" class="snippet-title">${snippet.title}</a>
      </div>
      <div class="lower-content">
        <span>${snippet.user.username}</span>
        <span>${snippet.datetime}</span>
      </div>
    </div>
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
