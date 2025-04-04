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
