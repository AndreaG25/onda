const genericText = (text) => {
   if (validator.isEmpty(text)) {
      return false;
   }
   return true;
};

const validateRegistration = (email, password, username, date, fullname) => {
   let errors = []
   let validate_email = checkEmail(email)
   if(validate_email[0] == false){
    errors.push(validate_email[1]);
   }

   let validate_username = checkUsername(username)
   if(validate_username[0] == false){
    errors.push(validate_username[1]);
   }

   let validate_password = checkPassword(password)
   if(validate_password[0] == false){
    errors.push(validate_password[1]);
   }   

   let validate_date = checkDate(date)
   if(validate_date[0] == false){
    errors.push(validate_date[1]);
   }

   let validate_fullname = checkFullName(fullname)
   if(validate_fullname[0] == false){
    errors.push(validate_fullname[1]);
   }

   if(errors.length == 0){
    return [true]
   }else{
    console.log(errors)
    return [false, errors]
   }
};
  

const validateUpdateData = (date, fullname) => {
    let errors = []

   let validate_date = checkDate(date)
   if(validate_date[0] == false){
    errors.push(validate_date[1]);
   }

   let validate_fullname = checkFullName(fullname)
   if(validate_fullname[0] == false){
    errors.push(validate_fullname[1]);
   }

   if(errors.length == 0){
    return [true]
   }else{
    console.log(errors)
    return [false, errors]
   }
}

const checkUsername = (username) => {
    if (!validator.isLength(username, { min: 4 })) {
        return [false, "Lo username deve avere almeno 4 caratteri"]
    }
    
    if (validator.isAlphanumeric(username) && validator.isLowercase(username) && !validator.contains(username, ' ')) {
        console.log('username ok')
    } else {
        return [false, "La stringa contiene caratteri non validi"]
    }
    return [true]
}

const checkEmail = (email) => {
    if (!validator.isEmail(email)) {
        return [false, "Email non valida"]
    }
    return [true]
}

const checkPassword = (password) => {
    if (!validator.isLength(password, { min: 6 })) {
        return [false, "La password deve essere lunga almeno 6 caratteri"]
    }
    if(password.includes(' ')){
        return [false, "La password non deve contenere spazi vuoti"]
    }
    if(!(isSqlInjectionSafe(password))){
        return [false, "La password non deve contenere caratteri strani"]
    }
    return [true]
}

const checkDate = (date) => {
    if (!(validator.isDate(date, 'YYYY-MM-DD'))) {
        return [false,"La data di nascita non è valida"];
    }
    return [true]
}

const checkFullName = (fullname) => {
    if (!validator.isLength(fullname, { min: 8 })) {
        return [false, "Il nome deve essere lungo almeno 8 caratteri"]
    }
    return [true]
}

const isSqlInjectionSafe = (input) => {
    const dangerousChars = [';', '--', "'", '"', '=', '<', '>', '(', ')', '/*', '*/'];
  
    for (let i = 0; i < dangerousChars.length; i++) {
      if (input.includes(dangerousChars[i])) {
        return false;
      }
    }
  
    return true;
}
  