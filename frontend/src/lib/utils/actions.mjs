export const tryRegister = async (data) => {
  if (!data.terms) return new Error("Terms not accepted");
  if (data.password !== data.repeatPassword)
    return new Error("Passwords did not match");
  if (!data.password) return new Error("Password required ");
  const payload = {
    first_name: data.first_name,
    last_name: data.last_name,
    username: data.username,
    email: data.email,
    city: "",
    state: "",
    password: data.password,
    role: data.type,
  };

  try {
    const res = await fetch(`${import.meta.env.VITE_CLOUD}/api/user/`, {
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
    const res = await fetch(`${import.meta.env.VITE_CLOUD}/api/session/`, {
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
