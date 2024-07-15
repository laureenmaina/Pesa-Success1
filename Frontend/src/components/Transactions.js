import React, { useState, useEffect } from 'react';

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [newTransaction, setNewTransaction] = useState({
    user_id: '',
    amount: '',
    type: ''
  });
  const [error, setError] = useState(null);

  const fetchTransactions = async () => {
    try {
      const response = await fetch('http://localhost:5000/transactions');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setTransactions(data);
    } catch (error) {
      setError(error.message);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewTransaction((prevTransaction) => ({
      ...prevTransaction,
      [name]: value
    }));
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/transactions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newTransaction)
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to create transaction');
      }
      setNewTransaction({
        user_id: '',
        amount: '',
        type: ''
      });
      fetchTransactions();
    } catch (error) {
      setError(error.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:5000/transactions/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to delete transaction');
      }
      fetchTransactions();
    } catch (error) {
      setError(error.message);
    }
  };

  const handleUpdate = async (id) => {
    try {
      const response = await fetch(`http://localhost:5000/transactions/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newTransaction)
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to update transaction');
      }
      setNewTransaction({
        user_id: '',
        amount: '',
        type: ''
      });
      fetchTransactions();
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div>
   
      <h2>Add a New Transaction</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          name="user_id"
          value={newTransaction.user_id}
          onChange={handleChange}
          placeholder="User ID"
          required
        />
        <input
          type="number"
          name="amount"
          value={newTransaction.amount}
          onChange={handleChange}
          placeholder="Amount"
          required
        />
        <input
          type="text"
          name="type"
          value={newTransaction.type}
          onChange={handleChange}
          placeholder="Type (e.g., DEPOSIT, WITHDRAWAL)"
          required
        />
        <button type="submit">Add Transaction</button>
      </form>
      <h1>My Transactions</h1>
      {/* <button onClick={fetchTransactions}>Fetch Transactions</button> */}
      {error && <p>{error}</p>}
      <ul>
        {transactions.map((transaction) => (
          <li key={transaction.id}>
            {transaction.user_id} - {transaction.amount} - {transaction.type}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Transactions;
