import React, { useState } from "react";
import axios from 'axios';
import './Login.css';

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  function validateForm() {
    return username.length > 0 && password.length > 0;
  }

  function handleSubmit(event) {
    event.preventDefault();
    const data = new FormData();
    data.append('username', username);
    data.append('password', password);

    axios.post(
      'http://127.0.0.1:8000/chatbot/login',
      data,
      {headers: {"content-type": "multipart/form-data"}}
    ).then((response) => {
      if (response.status === 200) {
          const state = response.data.state;
          if (state === 'success') {
            sessionStorage.setItem('user', response.data.user);
            window.location.reload();
          } else {
            window.location.reload();
          }
      }
    }).catch(function (error) {
      console.log(error);
    });

  }

  return (
    <div className='login-container'>
      <div className="main-div">
        <h2 style={{textAlign: "center"}}>Chat Login</h2>

        <input placeholder="Username..." id="email_field" onChange={(e) => setUsername(e.target.value)} />
        <input type="password" placeholder="Password..." id="password_field" onChange={(e) => setPassword(e.target.value)} />

        <button onClick={handleSubmit} disabled={!validateForm}>Sign In</button>
      </div>
    </div>
  );
}
