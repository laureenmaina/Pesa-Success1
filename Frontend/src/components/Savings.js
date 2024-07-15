import React, { useState, useEffect } from 'react';

function Savings() {
  const [savings, setSavings] = useState([]);
  const [newSaving, setNewSaving] = useState({
    amount: '',
    target_date: '',
    user_id: ''
  });
  const [error, setError] = useState(null);

  const fetchSavings = async () => {
    try {
      const response = await fetch('http://localhost:5000/savings');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setSavings(data);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewSaving((prevSaving) => ({
      ...prevSaving,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/savings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newSaving)
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to create saving');
      }
      setNewSaving({
        amount: '',
        target_date: '',
        user_id: ''
      });
      fetchSavings(); // Refresh the list of savings after adding a new one
    } catch (error) {
      setError(error.message);
    }
  };

  useEffect(() => {
    fetchSavings();
  }, []);

  return (
    <div>
    
      <h2>Add a New Saving</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          name="amount"
          value={newSaving.amount}
          onChange={handleChange}
          placeholder="Amount"
          required
        />
        <input
          type="date"
          name="target_date"
          value={newSaving.target_date}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="user_id"
          value={newSaving.user_id}
          onChange={handleChange}
          placeholder="User ID"
          required
        />
        <button type="submit">Add Savings</button>
        <button type="submit">Withdraw from Savings</button>
      </form>
      <h1>My Savings</h1>
      {error && <p>{error}</p>}
      <ul>
        {savings.map((saving) => (
          <li key={saving.id}>
           {saving.id}- {saving.amount} - {saving.target_date}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Savings;
