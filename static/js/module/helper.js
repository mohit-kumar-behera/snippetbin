export const ENDPOINT_URL = `${location.protocol}//${location.host}`;

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