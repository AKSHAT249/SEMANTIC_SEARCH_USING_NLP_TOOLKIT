// import React, { useState } from 'react';
// import axios from 'axios';
// import './App.css';

// function App() {
//   const [query, setQuery] = useState('');  // To store the user's search query
//   const [results, setResults] = useState([]);  // To store the search results
//   const [loading, setLoading] = useState(false);  // To manage loading state
//   const [error, setError] = useState('');  // To store any error messages

//   // Function to handle search
//   const handleSearch = async () => {
//     if (query.trim() === '') {
//       setError('Query cannot be empty.');
//       return;
//     }

//     setLoading(true);  // Set loading to true before making the API call
//     setError('');  // Reset error message

//     try {
//       const response = await axios.get('http://127.0.0.1:8000/api/search/', {
//         params: { query },  // Pass query as a parameter to the backend
//       });

//       const data = Object.entries(response.data);
      

//       setResults(data);  // Update the results state with the data received from the backend
//     } catch (err) {
//       console.error("Error fetching results:", err);
//       setError("Failed to fetch results. Please try again.");
//     } finally {
//       setLoading(false);  // Stop the loading state after the API call
//     }
//   };

//   return (
//     <div className="App">
//       <h1>Semantic Search System</h1>

//       <div className="search-container">
//         <input
//           type="text"
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//           placeholder="Enter your search query..."
//         />
//         <button onClick={handleSearch}>Search</button>
//       </div>

//       {loading && <p>Loading...</p>}

//       {error && <p className="error">{error}</p>}

//       <div className="results-container">
//         {results.length > 0 ? (
//           <ul>
//             <li>{results[0][1]}</li>
//           </ul>
//         ) : (
//           !loading && <p>No results found.</p>
//         )}
//       </div>
//     </div>
//   );
// }

// export default App;



import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');  // Store the user's search query
  const [results, setResults] = useState([]);  // Store the search results
  const [loading, setLoading] = useState(false);  // Manage loading state
  const [error, setError] = useState('');  // Store error messages

  // Function to handle search
  const handleSearch = async () => {
    if (query.trim() === '') {
      setError('Query cannot be empty.');
      return;
    }

    setLoading(true);  // Show loading state
    setError('');  // Reset error message

    try {
      const response = await axios.get('http://127.0.0.1:8000/api/search/', {
        params: { query },  // Send query to backend
      });

      const data = Object.entries(response.data);
      setResults(data);  // Store the received data
    } catch (err) {
      console.error("Error fetching results:", err);
      setError("Failed to fetch results. Please try again.");
    } finally {
      setLoading(false);  // Stop loading state
    }
  };

  return (
    <div className="App">
      <header>
        <h1>Semantic Search System</h1>
        <p>Enter a search query to find the most relevant document.</p>
      </header>

      <div className="search-container">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}  // Update the query state
          placeholder="Enter your search query..."
          className="search-input"
        />
        <button onClick={handleSearch} className="search-button">Search</button>
      </div>

      {loading && <div className="loading-spinner"></div>}  {/* Show spinner during loading */}
      {error && <p className="error-message">{error}</p>}  {/* Show error if any */}

      <div className="results-container">
        {results.length > 0 ? (
          <ul>
            {results.map((result, index) => (
              <li key={index} className="result-item">
                <h3>{result[0]}</h3>
                <p>{result[1]}</p>
              </li>
            ))}
          </ul>
        ) : (
          !loading && <p>No results found.</p>
        )}
      </div>
    </div>
  );
}

export default App;
