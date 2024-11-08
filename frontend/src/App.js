import "./App.css";
import React, { useEffect, useState } from "react";
import Login from "./form/Login";
import Forgot from "./form/Forgot";
import Register from "./form/Register";
import Home from "./Home";

function App() {
  const [page, setPage] = useState("login");
  const [token, setToken] = useState();

  useEffect(() => {
    const auth = localStorage.getItem("auth_token");
    setToken(auth);
  }, [token]);

  const choosePage = () => {
    if (page === "login") {
      return <Login setPage={setPage} />;
    }
    if (page === "register") {
      return <Register setPage={setPage} />;
    }
    if (page === "forgot") {
      return <Forgot setPage={setPage} />;
    }
  };

  const pages = () => {
    if (token == null) {
      return (
        <div className="min-h-screen bg-gradient-to-r from-cyan-500 to-blue-500 flex justify-center items-center">
          <div className="py-12 px-12 bg-white rounded-2xl showdow-xl z-20">
            {choosePage()}
          </div>
        </div>
      );
    } else {
      return <Home/>;
    }
  };
  return <React.Fragment>{pages()}</React.Fragment>;
}

export default App;
