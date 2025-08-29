import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [feedbackList, setFeedbackList] = useState([]);
  const [stats, setStats] = useState(null);
  const [text, setText] = useState('');
  const [product, setProduct] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Fetch initial data on component mount
  useEffect(() => {
    fetchFeedback();
    fetchStats();
  }, []);

  const fetchFeedback = async () => {
    try {
      const response = await fetch('/api/feedback');
      const data = await response.json();
      setFeedbackList(data);
    } catch (error) {
      console.error("Error fetching feedback:", error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text) return;
    setIsLoading(true);

    try {
      await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, product }),
      });
      // Clear form and refresh data
      setText('');
      setProduct('');
      fetchFeedback();
      fetchStats();
    } catch (error) {
      console.error("Error submitting feedback:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Multilingual Customer Feedback Analyzer 🗣️</h1>
      </header>

      <main>
        <div className="form-container">
          <h2>Submit New Feedback</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={product}
              onChange={(e) => setProduct(e.target.value)}
              placeholder="Product Name (optional)"
            />
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter your feedback here... (any language)"
              required
            ></textarea>
            <button type="submit" disabled={isLoading}>
              {isLoading ? 'Analyzing...' : 'Submit Feedback'}
            </button>
          </form>
        </div>

        <div className="dashboard">
          <div className="stats-container">
            <h2>Sentiment Dashboard</h2>
            {stats ? (
              <div className="stats-grid">
                <div className="stat-card">
                  <h3>Total Reviews</h3>
                  <p>{stats.total_feedback}</p>
                </div>
                <div className="stat-card positive">
                  <h3>Positive</h3>
                  <p>{stats.positive_percentage}%</p>
                </div>
                <div className="stat-card negative">
                  <h3>Negative</h3>
                  <p>{stats.negative_percentage}%</p>
                </div>
                <div className="stat-card neutral">
                  <h3>Neutral</h3>
                  <p>{stats.neutral_percentage}%</p>
                </div>
              </div>
            ) : (
              <p>Loading stats...</p>
            )}
          </div>

          <div className="feedback-list">
            <h2>Recent Feedback</h2>
            <table>
              <thead>
                <tr>
                  <th>Original Text</th>
                  <th>Language</th>
                  <th>Translated Text</th>
                  <th>Sentiment</th>
                  <th>Product</th>
                </tr>
              </thead>
              <tbody>
                {feedbackList.map((item) => (
                  <tr key={item.id} className={`sentiment-${item.sentiment}`}>
                    <td>{item.original_text}</td>
                    <td>{item.language}</td>
                    <td>{item.translated_text}</td>
                    <td>{item.sentiment}</td>
                    <td>{item.product || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;