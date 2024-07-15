import React from 'react';
import { NavLink } from 'react-router-dom';
import './styles/DashNavBar.css';

function DashNavBar() {
  return (
    <nav className="dash-nav-bar">
      <ul>
        <li>
          <NavLink to="/transactions" activeClassName="active-link">
            My Transactions
          </NavLink>
        </li>
        <li>
          <NavLink to="/loans" activeClassName="active-link">
            My Loans
          </NavLink>
        </li>
        <li>
          <NavLink to="/subscriptions" activeClassName="active-link">
            My Subscriptions
          </NavLink>
        </li>
        <li>
          <NavLink to="/savings" activeClassName="active-link">
            My Savings
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}

export default DashNavBar;
