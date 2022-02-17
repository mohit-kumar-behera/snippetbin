import {
  sendRequest,
  ENDPOINT_URL,
  addLoader,
  removeLoader,
  wait,
  copyToClipBoard,
} from './module/helper.js';

const deleteBtn = document.getElementById('delete-btn');
const decryptBtn = document.getElementById('decrypt-btn');
const editSnippetForm = document.getElementById('create-snippet-form');
const copyBtn = document.querySelector('.copy-btn');

const deleteSnippetHandler = async function () {
  const proceed_with_deletion = confirm('Are you sure you want to delete?');

  if (!proceed_with_deletion) return;

  const snippet_id = location.pathname.split('/')[2];
  const url = `${ENDPOINT_URL}/api/snippet/delete/${snippet_id}/`;

  const data = { delete: true };

  let response = null;
  try {
    response = await sendRequest(url, data);
  } catch (err) {
    console.error(err);
    alert('Something went wrong');
  }

  if (!response.success) return alert(response.data.error);

  // succesfully deleted
  window.location.replace(response.redirect_url);
};

const addHandlerToDecryptBtn = async function () {
  const snippetBox = document.getElementById('snippet');
  const decryptInput = document.getElementById('decrypt-input');

  if (!decryptInput.value) return;

  const data = {
    data: snippetBox.textContent,
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

  snippetBox.innerHTML = '';
  snippetBox.insertAdjacentHTML('afterbegin', response.data.snippet);
};

const handleEditSnippetForm = async function (data) {
  let formData = { ...data };
  if (!formData['renew-expiration']) return;
  addLoader(editSnippetForm);

  const snippet_id = location.pathname.split('/')[2];
  const url = `${ENDPOINT_URL}/api/snippet/edit/${snippet_id}/`;

  let response = null;
  try {
    response = await sendRequest(url, formData);
  } catch (err) {
    console.error(error);
    alert('Something went wrong');
  } finally {
    await wait(0.7);
    removeLoader(editSnippetForm, '<span>UPDATE EXPIRY</span>');
  }

  if (!response.success) return alert(response.data.error);

  editSnippetForm.insertAdjacentHTML(
    'beforeend',
    '<p class="mt-4 short-message"><strong class="text-success">Expiration Date was added successfully</strong></p>'
  );

  await wait(2);
  editSnippetForm.querySelector('.short-message').remove();
};

// EVENT LISTENERS
copyBtn.addEventListener('click', () => {
  const elem = document.querySelector('.url-text');
  const flag = copyToClipBoard(elem.value);
  flag && elem.select();
});
decryptBtn && decryptBtn.addEventListener('click', addHandlerToDecryptBtn);
deleteBtn.addEventListener('click', deleteSnippetHandler);
editSnippetForm.addEventListener('submit', e => {
  e.preventDefault();

  const snippetDataArr = [...new FormData(e.target)];
  const snippetData = Object.fromEntries(snippetDataArr);

  handleEditSnippetForm(snippetData);
});
