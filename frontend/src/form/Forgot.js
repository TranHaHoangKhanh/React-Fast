/* eslint-disable default-case */
/* eslint-disable no-unused-vars */
import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";

export default function Forgot(props) {
  const [forgotForm, setForgotForm] = useState({
    email: "",
    new_password: "",
  });

  const onChangeForm = (label, event) => {
    switch (label) {
      case "email":
        setForgotForm({ ...forgotForm, email: event.target.value });
        break;
      case "new_password":
        setForgotForm({ ...forgotForm, new_password: event.target.value });
        break;
    }
  };

  //  submit handler
  const onSubmitHandler = async (event) => {
    event.preventDefault();
    console.log(forgotForm);

    // call api forgot password
    await axios
    .post("http://localhost:8000/auth/forgot-password", forgotForm)
    .then((res) => {
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
          Fotgot your password?
        </h1>
        <p className="w-80 text-center text-sm mb-8 font-semibold text-gray-600 tracking-wide cursor-pointer mx-auto">
          Now update your password account!
        </p>
      </div>
      <form onSubmit={onSubmitHandler}>
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Email"
            className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-blue-400"
            onChange={(event) => {
              onChangeForm("email", event);
            }}
          />
          <input
            type="password"
            placeholder="New Password"
            className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-blue-400"
            onChange={(event) => {
              onChangeForm("new_password", event);
            }}
          />
        </div>
        <div className="text-center mt-6">
          <button
            type="submit"
            className="py-3 w-64 text-xl text-white bg-blue-400 round-2xl hover:bg-blue-300 active:bg-blue-500 outline-none"
          >
            Update Password
          </button>
          <p className="mt-r text-sm">
            Already Have An Account?{" "}
            <Link
              to="/?signin"
              onClick={() => {
                props.setPage("login");
              }}
            >
              <span className="underline cursor-pointer">Sign In</span>
            </Link>
          </p>
        </div>
      </form>
    </React.Fragment>
  );
}
