import { sendRequest, ENDPOINT_URL } from './module/helper.js';

const deleteBtn = document.getElementById('delete-btn');
const decryptBtn = document.getElementById('decrypt-btn');

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
  snippetBox.removeAttribute('disabled');
};

decryptBtn && decryptBtn.addEventListener('click', addHandlerToDecryptBtn);

deleteBtn.addEventListener('click', deleteSnippetHandler);
