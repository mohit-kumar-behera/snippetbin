'use strict';

import {
  makeRandomID,
  isValidURL,
  ENDPOINT_URL,
  wait,
  sendRequest,
  addLoader,
  removeLoader,
} from './module/helper.js';

const form = document.getElementById('create-snippet-form');
const formSubmitBtn = document.querySelector('.form-submit');
const encryptionCheckBox = document.getElementById('encryption');
const encryptionInputField = document.querySelector('.encryption-key-div');

const handleCreateSnippetForm = async function (data) {
  addLoader(formSubmitBtn);
  let formData = { ...data };

  let snippet = formData['snippet'];
  const encryptionKey = formData['encryption-key'];

  if (isValidURL(snippet)) formData = { ...formData, is_url: true };

  if (encryptionKey) formData = { ...formData, isEncrypted: true };

  const url = `${ENDPOINT_URL}/api/snippet/create/`;
  let response = null;
  try {
    response = await sendRequest(url, formData);
  } catch (err) {
    alert('Something went wrong');
  } finally {
    await wait(0.7);
    removeLoader(formSubmitBtn, '<span>CREATE NEW SNIPPET</span>');
  }

  if (!response.success) return alert('Something went wrong');

  window.location.href = response.redirect_url;
};

const handleEncryptionInputField = activate => {
  if (activate) {
    encryptionInputField.querySelector('#encryption-key').value =
      makeRandomID(32);
    encryptionInputField.classList.add('show');
  } else {
    encryptionInputField.querySelector('#encryption-key').value = '';
    encryptionInputField.classList.remove('show');
  }
};

encryptionCheckBox.addEventListener('click', () => {
  if (encryptionCheckBox.checked) handleEncryptionInputField(true);
  else handleEncryptionInputField(false);
});

form.addEventListener('submit', e => {
  e.preventDefault();

  const snippetDataArr = [...new FormData(e.target)];
  const snippetData = Object.fromEntries(snippetDataArr);

  handleCreateSnippetForm(snippetData);
});
