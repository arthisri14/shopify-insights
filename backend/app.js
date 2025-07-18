import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [websiteUrl, setWebsiteUrl] = useState('');
  const [brandData, setBrandData] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setBrandData(null);
    setError(null);

    try {
      const response = await axios.post('http://127.0.0.1:8000/insights/extract_brand_insights', {
        website_url: websiteUrl
      });
      setBrandData(response.data.brand_data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Brand Insights Extractor</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Shopify Store URL"
          value={websiteUrl}
          onChange={(e) => setWebsiteUrl(e.target.value)}
          style={{ padding: '0.5rem', width: '300px' }}
        />
        <button type="submit" style={{ padding: '0.5rem 1rem', marginLeft: '1rem' }}>
          Extract
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>⚠️ {error}</p>}

      {brandData && (
        <div style={{ marginTop: '2rem' }}>
          <h2>Product Catalog</h2>
          <ul>
            {brandData.product_catalog.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
          <p>
            <strong>Privacy Policy:</strong>{' '}
            <a href={brandData.privacy_policy_link} target="_blank" rel="noopener noreferrer">
              {brandData.privacy_policy_link}
            </a>
          </p>
          <p>
            <strong>About Us:</strong>{' '}
            <a href={brandData.about_us_link} target="_blank" rel="noopener noreferrer">
              {brandData.about_us_link}
            </a>
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
