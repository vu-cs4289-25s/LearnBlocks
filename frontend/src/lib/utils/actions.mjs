export const tryRegister = async (data) => {
  if (!data.terms) return new Error("Terms not accepted");
  if (data.password !== data.repeatPassword)
    return new Error("Passwords did not match");
  if (!data.password) return new Error("Password required ");
  const payload = {
    username: data.username,
    email: data.email,
    password: data.password,
    first_name: data.first_name,
    last_name: data.last_name,
    role: data.type,
  };

  try {
    const res = await fetch(`${import.meta.env.VITE_CLOUD}/users/`, {
      method: "POST",
      body: JSON.stringify(payload),
      headers: { "content-type": "application/json" },
    });

    if (!res.ok) throw new Error(`${res.status}: Failed to create new user`);

    const json = await res.json();
    return json;
  } catch (err) {
    return err;
  }
};

export const tryLogin = async (data) => {
  if (!data.username) return new Error("Username Required");
  if (!data.password) return new Error("Password Required");
  const payload = { ...data };
  try {
    const res = await fetch(`${import.meta.env.VITE_CLOUD}/login/`, {
      method: "POST",
      body: JSON.stringify(payload),
      headers: { "content-type": "application/json" },
    });
    if (!res.ok) throw new Error(`${res.status}: Failed To Login`);
    const json = await res.json();
    return json;
  } catch (err) {
    return new Error(`Failed To Connect To Server: ${err}`);
  }
};

export const tryLogout = async () => {
  try {
   const res = await fetch(`${import.meta.env.VITE_CLOUD}/api/session/reset/`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error(`${res.status}: Failed To Logout`);
  } catch (err) {
    return new Error(`Failed To Connect To Server: ${err}`);
  }
};

export const tryGetProjects = async () => {
  try {
   const res = await fetch(`${import.meta.env.VITE_CLOUD}/api/project/`) 
   const json = await res.json()
   return json
  }
  catch(err) {
    return new Error(`Failed to get Projects List: ${err}`)    
  }
}

export const tryGetCourses = async () => {
  try {
   const res = await fetch(`${import.meta.env.VITE_CLOUD}/api/course/`) 
   const json = await res.json()
   return json
  }
  catch(err) {
    return new Error(`Failed to get Courses List: ${err}`)    
  }
}

export const tryGetModules = async () => {
  try {
   const res = await fetch(`${import.meta.env.VITE_CLOUD}/api/module/`) 
   const json = await res.json()
   return json
  }
  catch(err) {
    return new Error(`Failed to get Modules List: ${err}`)    
  }
}

export const tryJoinClass = async (classCode,authUser) =>{
  //console.log(classCode);
  //console.log(authUser);
  try{
    const res = await fetchLB(authUser,`${import.meta.env.VITE_CLOUD}/classes/join/${classCode}/`,{method:"POST"});
    const json = await res.json()
    return json;
  }
  catch(err){
    return new Error(`Failed to Join Class: ${err}`);
  }
}

export const fetchLB = async (authUser, input, init = {}) => {
  // Create a new Headers object with the headers passed in init (if any)
  const headers = new Headers(init.headers || {});

  //console.log(authUser);

  // If authUser exists and has a token, append it to the Authorization header.
  if (authUser && authUser.token) {
    headers.set('Authorization', `Token ${authUser.token}`);
  }

  // Merge the headers back into the fetch options.
  const updatedInit = {
    ...init,
    headers,
  };

  try {
    const response = await fetch(input, updatedInit);

    // If the response is not OK, extract the error message and throw an error.
    if (!response.ok) {
      const errorMessage = await response.text();
      throw new Error(`Fetch error: ${response.status} - ${errorMessage}`);
    }

    return response;
  } catch (error) {
    // Propagate the error to the caller for further handling.
    throw error;
  }
};