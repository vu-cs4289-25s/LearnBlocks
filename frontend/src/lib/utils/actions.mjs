export const tryRegister = async (data) => {
  if (!data.terms) return new Error('Terms not accepted');
  if (!data.password) return new Error('Password required ');
  if (data.password.length < 8) return new Error('Password too short');
  if (data.password !== data.repeatPassword)
    return new Error('Passwords do not match');

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
      method: 'POST',
      body: JSON.stringify(payload),
      headers: { 'content-type': 'application/json' },
    });
    if (res.status === 400) {
      const json = await res.json();
      console.log(json);
      const error = json[Object.keys(json)[0]];
      throw new Error(`${error}`);
    } else if (!res.ok) {
      throw new Error(`${res.status}: Failed to create new user`);
    }
    const json = await res.json();
    return json;
  } catch (err) {
    return err;
  }
};

export const tryLogin = async (data) => {
  if (!data.username) return new Error('Username Required');
  if (!data.password) return new Error('Password Required');
  const payload = { ...data };
  try {
    const token_res = await fetch(`${import.meta.env.VITE_CLOUD}/login/`, {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: { 'content-type': 'application/json' },
    });
    if (!token_res.ok) throw new Error(`${token_res.status}: Failed To Login`);
    const token_json = await token_res.json();
    const user_res = await fetch(`${import.meta.env.VITE_CLOUD}/whoami/`, {
      headers: { Authorization: `Token ${token_json.token}`},
    });
    const user = await user_res.json()
    user.token = token_json.token
    console.log(user)
    return user;
  } catch (err) {
    return new Error(`Failed To Connect To Server: ${err}`);
  }
};

export const tryGetProjects = async (authUser) => {
  try {
    const res = await fetchLB(authUser, `${import.meta.env.VITE_CLOUD}/projects/`);
    const json = await res.json();
    return json;
  } catch (err) {
    return new Error(`Failed to get Projects List: ${err}`);
  }
};

export const tryGetCatalog = async (authUser) => {
  try {
    const res = await fetchLB(authUser, `${import.meta.env.VITE_CLOUD}/courses/`);
    const json = await res.json();
    console.log(json)
    return json;
  } catch (err) {
    return new Error(`Failed to get Catalog List: ${err}`);
  }
};

export const tryLogout = async (authUser) => {
  try {
   const res = await fetchLB(authUser,`${import.meta.env.VITE_CLOUD}/logout/`, {
      method: "POST",
    });
    if (!res.ok) throw new Error(`${res.status}: Failed To Logout`);
  } catch (err) {
    return new Error(`Failed to Logout: ${err}`);
  }
};

export const tryListCourses = async (authUser) => {
  try {
    const res = await fetchLB(authUser, `${import.meta.env.VITE_CLOUD}/users/${authUser.username}/?include=course_enrollments`);
    const json = await res.json();
    console.log(json)
    return json.course_enrollments;
  } catch (err) {
    return new Error(`Failed to get Courses List: ${err}`);
  }
};

export const tryGetCourse = async (authUser, courseId) => {
  try {
    const res = await fetchLB(authUser, `${import.meta.env.VITE_CLOUD}/courses/${courseId}/`);
    const json = await res.json();
    console.log(json)
    return json;
  } catch (err) {
    return new Error(`Failed to get Courses List: ${err}`);
  }
};

export const tryListModules = async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_CLOUD}/api/module/`);
    const json = await res.json();
    return json;
  } catch (err) {
    return new Error(`Failed to get Modules List: ${err}`);
  }
};

export const tryGetModule = async (authUser, module_id) => {
  try {
    const res = await fetchLB(authUser, `${import.meta.env.VITE_CLOUD}/modules/${module_id}/`);
    const json = await res.json();
    const blob_res = await fetch(json.file)
    json.blob = await blob_res.text()
    return json;
  } catch (err) {
    return new Error(`Failed to get Module : ${err}`);
  }
};


export const tryJoinClass = async (classCode, authUser) => {
  try {
    const res = await fetchLB(
      authUser,
      `${import.meta.env.VITE_CLOUD}/classes/join/${classCode}/`,
      { method: 'POST' },
    );
    const json = await res.json();
    return json;
  } catch (err) {
    return new Error(`Failed to Join Class: ${err}`);
  }
};

export const fetchLB = async (authUser, input, init = {}) => {
  const headers = new Headers(init.headers || {});

  if (authUser && authUser.token) {
    headers.set('Authorization', `Token ${authUser.token}`);
  }

  const updatedInit = {
    ...init,
    headers,
  };

  const promise = fetch(input, updatedInit);

  return promise;
};

export const fetchUser = async(authUser,username)=>{
  try {
    const res = await fetchLB(authUser,`${import.meta.env.VITE_CLOUD}/users/${username}`) 
    const json = await res.json()
    return json
   }
   catch(err) {
     return new Error(`Failed to get User: ${err}`)    
   }  
}
