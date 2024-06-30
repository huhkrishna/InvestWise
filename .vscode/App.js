import React, { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Home from './Home';
import CreateAccount from "./components/CreateAccount";
import CreditMoney from "./components/CreditMoney";
import TransferMoney from "./components/TransferMoney";
import WithdrawMoney from "./components/WithdrawMoney";
import CheckBalance from "./components/CheckBalance";
import InvestmentCalculator from "./components/InvestmentCalculator";
import logo from './images/logo.png'; // Replace with the correct path to your logo image
import "./App.css";

function App() {
  useEffect(() => {
    const placeholderText = "What are you looking for?";
    const searchInput = document.querySelector(".search-bar");
    let currentText = "";
    let i = 0;

    function typeEffect() {
      if (i < placeholderText.length) {
        currentText += placeholderText.charAt(i);
        searchInput.setAttribute("placeholder", currentText);
        i++;
        setTimeout(typeEffect, 150);
      } else {
        setTimeout(() => {
          i = 0;
          currentText = "";
          searchInput.setAttribute("placeholder", currentText);
          setTimeout(typeEffect, 500);
        }, 2000);
      }
    }

    typeEffect();
  }, []);

  return (
    <Router>
      <div className="navbar">
        <div className="navbar-brand">
          <Link to="/">
            <img src={logo} alt="Bank of Baroda" className="logo" />
          </Link>
        </div>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/create-account">Create Account</Link>
          <Link to="/credit-money">Credit Money</Link>
          <Link to="/transfer-money">Transfer Money</Link>
          <Link to="/withdraw-money">Withdraw Money</Link>
          <Link to="/check-balance">Check Balance</Link>
          <Link to="/investment-calculator">Investment Calculator</Link>
        </nav>
      </div>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create-account" element={<CreateAccount />} />
          <Route path="/credit-money" element={<CreditMoney />} />
          <Route path="/transfer-money" element={<TransferMoney />} />
          <Route path="/withdraw-money" element={<WithdrawMoney />} />
          <Route path="/check-balance" element={<CheckBalance />} />
          <Route path="/investment-calculator" element={<InvestmentCalculator />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
