'use strict';

import {
  makeRandomID,
  isValidURL,
  getCookie,
  ENDPOINT_URL,
  wait,
} from './module/helper.js';

const form = document.getElementById('create-snippet-form');
const formSubmitBtn = document.querySelector('.form-submit');
const encryptionCheckBox = document.getElementById('encryption');
const encryptionInputField = document.querySelector('.encryption-key-div');

const addLoader = function (elem) {
  elem.querySelector('.spinner').innerHTML = '';
  elem
    .querySelector('.spinner')
    .insertAdjacentHTML(
      'beforeend',
      `<div class="spinner-border spinner-border-sm text-light ml-2 my-auto"></div>`
    );
};

const removeLoader = function (elem) {
  elem.querySelector('.spinner').innerHTML = '';
};

const sendDataToServer = async function (data) {
  const url = `${ENDPOINT_URL}/api/snippet/create/`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    return result;
  } catch (err) {
    throw err;
  }
};

const handleCreateSnippetForm = async function (data) {
  addLoader(formSubmitBtn);
  let formData = { ...data };

  let snippet = formData['snippet'];
  const encryptionKey = formData['encryption-key'];

  if (isValidURL(snippet)) formData = { ...formData, is_url: true };

  if (encryptionKey) formData = { ...formData, isEncrypted: true };

  let response = null;
  try {
    response = await sendDataToServer(formData);
  } catch (err) {
    console.error(error);
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

// const encryptDecryptFunction = async function (
//   data,
//   key,
//   type = ENCRYPTION_TYPE.encrypt
// ) {
//   try {
//     const url = `https://classify-web.herokuapp.com/api/${type}`;
//     const jsonData = JSON.stringify({ data, key });

//     let response = await fetch(url, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json;charset=utf-8',
//       },
//       body: jsonData,
//     });

//     const result = await response.json();

//     return result;
//   } catch (error) {
//     console.error(error);
//   }
// };

// const checkAndEncryptData = async function (data, key) {
//   if (!key) [false, data];

//   const { result: encryptedData } = await encryptDecryptFunction(
//     data,
//     key,
//     ENCRYPTION_TYPE.encrypt
//   );

//   return [true, encryptedData];
// };
