import React, { useState } from 'react';
import './App.css';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import logo from './assets/img/logo.png'; // Replace with your logo file path

function App() {
  const [symptoms, setSymptoms] = useState('');
  const [prediction, setPrediction] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/', { symptoms });
      setPrediction(response.data.prediction);
      setResponse(response.data.response);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleClear = () => {
    setSymptoms('');
    setPrediction('');
    setResponse('');
  };

  return (
  
      
      <div className="container">
        <div className='containerlogo'>
        <img src={logo} alt="Logo" className="logo" />
        <h1>Dolphy</h1>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="containersm">
            <label htmlFor="symptoms">Enter Symptoms: </label>
            <input
              type="text"
              id="symptoms"
              name="symptoms"
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              placeholder="Type a symptom,"
            />
            <button type="submit">Check Disease</button>
            <button type="button" className='btn' onClick={handleClear}>Clear</button>
          </div>
        </form>
        {prediction && (
          <div id="prediction">
            <h2>Predicted Disease: {prediction}</h2>
            {response && (
              <div>
                <h2>Precautions:</h2>
                {response.trim() !== '' ? (
                  <div className="precautions-container">
                    <ReactMarkdown>{response}</ReactMarkdown>
                  </div>
                ) : (
                  <p>No precautions available.</p>
                )}
              </div>
            )}
          </div>
        )}
        {!prediction && (
          <div id="prediction">
            <p className='notav'>No prediction available. Please enter symptoms and submit.</p>
          </div>
        )}
      </div>

  );
}

export default App;
