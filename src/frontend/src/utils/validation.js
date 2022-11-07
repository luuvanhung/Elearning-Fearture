const validateEmail = (email) => {
  const re = /^[a-z][a-z0-9_\\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}$/gm;
  return re.test(String(email).toLowerCase());
};

const validatePhone = (phone) => {
  const re = /^[\\+]?[(]?[0-9]{3}[)]?[-\s\\.]?[0-9]{3}[-\s\\.]?[0-9]{4,6}$/im;
  return re.test(phone);
};

const checkOwner = (userId, tokenInfo) => {
  return userId === tokenInfo.sub;
};

const checkHasScope = (scope, tokenInfo) => {
  return tokenInfo["scope"].indexOf(scope) !== -1;
};

module.exports = {
  validateEmail,
  validatePhone,
  checkOwner,
  checkHasScope,
};
