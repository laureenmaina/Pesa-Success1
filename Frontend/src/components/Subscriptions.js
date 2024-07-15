import React, { useState, useEffect } from 'react';

function Subscriptions() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [newSubscription, setNewSubscription] = useState({
    user_id: '',
    service_provider: '',
    amount: '',
    plan: '',
    start_date: '',
    end_date: ''
  });
  const [error, setError] = useState(null);

  const fetchSubscriptions = async () => {
    try {
      const response = await fetch('http://localhost:5000/subscriptions');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setSubscriptions(data);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewSubscription((prevSubscription) => ({
      ...prevSubscription,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/subscriptions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newSubscription)
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to create subscription');
      }
      setNewSubscription({
        user_id: '',
        service_provider: '',
        amount: '',
        plan: '',
        start_date: '',
        end_date: ''
      });
      fetchSubscriptions(); 
    } catch (error) {
      setError(error.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:5000/subscriptions/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to delete subscription');
      }
      fetchSubscriptions();
    } catch (error) {
      setError(error.message);
    }
  };

  useEffect(() => {
    fetchSubscriptions();
  }, []);

  return (
    <div>
     
      <h2>Add a New Subscription</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          name="user_id"
          value={newSubscription.user_id}
          onChange={handleChange}
          placeholder="User ID"
          required
        />
        <input
          type="text"
          name="service_provider"
          value={newSubscription.service_provider}
          onChange={handleChange}
          placeholder="Service Provider"
          required
        />
        <input
          type="number"
          name="amount"
          value={newSubscription.amount}
          onChange={handleChange}
          placeholder="Amount"
          required
        />
        <input
          type="text"
          name="plan"
          value={newSubscription.plan}
          onChange={handleChange}
          placeholder="Plan"
          required
        />
        <input
          type="date"
          name="start_date"
          placeholder='start_date'
          value={newSubscription.start_date}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="end_date"
          value={newSubscription.end_date}
          onChange={handleChange}
          required
        />
        <button type="submit">Add Subscription</button>
      </form>
      <h1>My Subscriptions</h1>
      {error && <p>{error}</p>}
      <ul>
        {subscriptions.map((subscription) => (
          <li key={subscription.id}>
           {subscription.id}- {subscription.service_provider} - {subscription.amount} - {subscription.plan} - {subscription.start_date} - {subscription.end_date}
            <button onClick={() => handleDelete(subscription.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Subscriptions;

