export const ENDPOINT_URL = `${location.protocol}//${location.host}`;
export const RES_PER_PAGE = 10;
export const months = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'Jun',
  'Jul',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec',
];

export const wait = sec =>
  new Promise(resolve => setTimeout(() => resolve(), sec * 1000));

export const makeRandomID = function (length) {
  let result = '';
  const characters =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const charactersLength = characters.length;

  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }

  return result;
};

export const isValidURL = function (str) {
  var pattern = new RegExp(
    '^(https?:\\/\\/)?' +
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' +
      '((\\d{1,3}\\.){3}\\d{1,3}))' +
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' +
      '(\\?[;&a-z\\d%_.~+=-]*)?' +
      '(\\#[-a-z\\d_]*)?$',
    'i'
  );
  return !!pattern.test(str);
};

export const getCookie = function (cookieName) {
  const unicodeCookies = decodeURIComponent(document.cookie);
  const cookies = unicodeCookies.split(';');

  const cookiesPair = cookies.map(cookie => {
    let [key, value] = cookie.split('=');
    key = key.trim();
    return [key, value];
  });
  const cookiesObj = Object.fromEntries(cookiesPair);

  return cookiesObj[cookieName];
};

export const sendRequest = async function (url, data) {
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

export const addLoader = function (elem) {
  elem.querySelector('.spinner').innerHTML = '';
  elem
    .querySelector('.spinner')
    .insertAdjacentHTML(
      'beforeend',
      `<div class="spinner-border spinner-border-sm text-light ml-2 my-auto"></div>`
    );
};

export const removeLoader = function (elem) {
  elem.querySelector('.spinner').innerHTML = '';
};

export const copyToClipBoard = function (value) {
  if (!value) return false;

  navigator.clipboard?.writeText && navigator.clipboard.writeText(value);

  return true;
};

export const buildSpanTag = function (type, data = null) {
  let text = 'This snippet will never expire';

  const formatDMY = (d, m, y) => `${months[m]} ${d}, ${y}`;
  const formatDMYHMS = (d, m, y, h, min) =>
    `${formatDMY(d, m, y)} | ${h}:${min}`;

  if (type === 1) {
    // expires after 1 day
    const dt = new Date(data);
    const [d, m, y, h, min] = [
      dt.getDate(),
      dt.getMonth(),
      dt.getFullYear(),
      dt.getHours(),
      dt.getMinutes(),
    ];

    text = `This snippet will expire <b>1</b> day after <b>${formatDMYHMS(
      d,
      m,
      y,
      h,
      min
    )}</b>`;
  } else if (type === 2) {
    // expires in given date
    const dt = new Date(data);
    const [d, m, y] = [dt.getDate(), dt.getMonth(), dt.getFullYear()];

    text = `This snippet will expire on <b>${formatDMY(d, m, y)}</b>`;
  }

  return `<span class="text-muted">${text}</span>`;
};
