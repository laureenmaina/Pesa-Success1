import React, { useEffect, useState } from 'react';
import './styles/Home.css';

const greeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good Morning';
  if (hour < 18) return 'Good Afternoon';
  return 'Good Evening';
};

const capitalizeFirstLetter = (string) => {
  return string?.charAt(0).toUpperCase() + string?.slice(1) || '-';
};

function Home({ user }) {
  const [summary, setSummary] = useState({
    
    totalBalance: 0,
    totalSavings: 0,
    totalSubscriptions: 0,
    outstandingLoan: 0,
    recentTransaction: { type: '-', amount: 0 }
  });

  // To edit path
  useEffect(() => {
    if (user) {
      fetch(`/api/user-summary?userId=${user.id}`)
        .then(response => response.json())
        .then(data => setSummary(data))
        .catch(error => console.error("Error fetching summary:", error));
    }
  }, [user]);

  console.log("Rendering Home with user:", user);

  if (user) {
    return (
      <div className="home-container">
        <h2>{greeting()}, {capitalizeFirstLetter(user.username)}</h2>
        <div className="cards-container">
          <div className="card">
          <h3>Account Balance</h3>
            <p>{summary.totalBalance}</p>
            <h3>Total Savings</h3>
            <p>{summary.totalSavings}</p>
           
          </div>
          <div className="card">
            <h3>Account Summary</h3>
            <p>Total Subscriptions: {summary.totalSubscriptions}</p>
            <p>Outstanding Loan: {summary.outstandingLoan}</p>
            <p>Recent Transaction: {summary.recentTransaction.type} - {summary.recentTransaction.amount}</p>
          </div>
        </div>
      </div>
    );
  } else {
    return (
      <div className="welcome-container">
        <h1 id='salutations'>Hello! Please Login or Sign Up to access your account</h1>
        <div className="welcome-card">
          <ul>
            <li>At Pesa Bank, we prioritize your financial well-being with unparalleled security, personalized services, and cutting-edge technology.</li>
            <li>Enjoy the convenience of our user-friendly online platform and 24/7 customer support.</li>
            <li>Our comprehensive financial products and competitive rates ensure you get the best value, while our commitment to transparency and community-focused initiatives fosters trust and positive impact.</li>
            <li>Join us today and experience a secure and prosperous future with a trusted partner dedicated to your success.</li>
          </ul>
        </div>
      </div>
    );
  }
}

export default Home;
