/* eslint-disable default-case */
import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
export default function Login(props) {
  const [loginForm, setLoginform] = useState({
    username: "",
    password: "",
  });

  const onChangeForm = (label, event) => {
    switch (label) {
      case "username":
        setLoginform({ ...loginForm, username: event.target.value });
        break;
      case "password":
        setLoginform({ ...loginForm, password: event.target.value });
        break;
    }
  };

  const onSubmitHandler = async (event) => {
    event.preventDefault();
    console.log(loginForm);
    // call api login
    await axios
      .post("http://localhost:8000/auth/login", loginForm)
      .then((res) => {
        console.log(res);
        // Save token to local storage
        localStorage.setItem("auth_token", res.data.result.access_token);
        localStorage.setItem("auth_token_type", res.data.result.token_type);

        // add successfully notification
        toast.success(res.data.detail);
        // reoload page after successful login
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      })
      .catch((err) => {
        // add error notification
        console.log(err);
        toast.error(err.response.data.detail);
      });
  };
  return (
    <React.Fragment>
      <div>
        <h1 className="text-3xl font-bold text-center mb-4 cursor-pointer">
          Welcome to React App
        </h1>
        <p className="w-80 text-center text-sm mb-8 font-semibold text-gray-600 tracking-wide cursor-pointer mx-auto">
          Please login to your account!
        </p>
      </div>
      <form onSubmit={onSubmitHandler}>
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-blue-400"
            onChange={(event) => {
              onChangeForm("username", event);
            }}
          />
          <input
            type="password"
            placeholder="Password"
            className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-blue-400"
            onChange={(event) => {
              onChangeForm("password", event);
            }}
          />
        </div>
        <div className="text-center mt-6">
          <button
            type="submit"
            className="py-3 w-64 text-xl text-white bg-blue-400 round-2xl hover:bg-blue-300 active:bg-blue-500 outline-none"
          >
            Sign In
          </button>
          <p className="mt-r text-sm">
            You don"t have an account?{" "}
            <Link
              to="/?register"
              onClick={() => {
                props.setPage("register");
              }}
            >
              <span className="underline cursor-pointer">Register</span>
            </Link>{" "}
            or{" "}
            <Link
              to="/?forgot"
              onClick={() => {
                props.setPage("forgot");
              }}
            >
              <span className="underline cursor-pointer">Forgot Password?</span>
            </Link>
          </p>
        </div>
      </form>
    </React.Fragment>
  );
}
