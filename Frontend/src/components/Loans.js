import React, { useState, useEffect } from 'react';

function Loans() {
  const [loans, setLoans] = useState([]);
  const [newLoan, setNewLoan] = useState({
    id:'',
    borrowed_amount: '',
    borrow_date: '',
    interest_rate: 12.5,
    target_date: '',
    trustee: '',
    trustee_phone_number: '',
    user_id: ''
  });
  const [error, setError] = useState(null);

  const fetchLoans = async () => {
    try {
      const response = await fetch('http://localhost:5000/loans');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setLoans(data);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewLoan((prevLoan) => ({
      ...prevLoan,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/loans', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newLoan)
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to create loan');
      }
      setNewLoan({
        id:'',
        borrowed_amount: '',
        borrow_date: '',
        interest_rate: '',
        target_date: '',
        trustee: '',
        trustee_phone_number: '',
        user_id: ''
      });
      fetchLoans(); 
    } catch (error) {
      setError(error.message);
    }
  };

  useEffect(() => {
    fetchLoans();
  }, []);

  return (
    <div>
    
      <h2>Add a New Loan</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="borrowed_amount"
          value={newLoan.borrowed_amount}
          onChange={handleChange}
          placeholder="Amount"
          required
        />
        <input
          type="date"
          name="borrow_date"
          placeholder="borrow_date"
          value={newLoan.borrow_date}
          onChange={handleChange}
          required
        />
        <input
          type="float"
          name="interest_rate"
          value={newLoan.interest_rate}
          onChange={handleChange}
          placeholder="Interest Rate"
          required
        />
        <input
          type="date"
          name="target_date"
          value={newLoan.target_date}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="trustee"
          value={newLoan.trustee}
          onChange={handleChange}
          placeholder="Trustee"
          required
        />
        <input
          type="text"
          name="trustee_phone_number"
          value={newLoan.trustee_phone_number}
          onChange={handleChange}
          placeholder="Trustee Phone Number"
          required
        />
        <input
          type="number"
          name="user_id"
          value={newLoan.user_id}
          onChange={handleChange}
          placeholder="User ID"
          required
        />
        <button type="submit">Add Loan</button>
      </form>
      <h1>My Loans</h1>
      {/* <button onClick={fetchLoans}>Fetch Loans</button> */}
      {error && <p>{error}</p>}
      <ul>
        {loans.map((loan) => (
          <li key={loan.id}>
            
            {loan.id}- {loan.borrowed_amount} - {loan.borrow_date} - {loan.interest_rate}% - {loan.target_date}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Loans;
