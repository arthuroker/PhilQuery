import React, { useEffect, useState } from 'react';
// import AskQuestionForm from './AskQuestionForm'; // Keep commented if not used yet
import './PhilQueryPanel.css'; // Ensure this points to your updated CSS file

export default function PhilQueryPanel() {
  const [sources, setSources] = useState([]);
  const [answer, setAnswer] = useState(null); // Initialize answer state
  const [isLoadingSources, setIsLoadingSources] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state

  useEffect(() => {
    const fetchSources = async () => {
      setIsLoadingSources(true); // Start loading
      setError(null); // Reset error on new fetch
      try {
        // Ensure the URL is correct for your local setup
        const res = await fetch("http://127.0.0.1:8000/sources");
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        setSources(data);
      } catch (err) {
        console.error("Error fetching sources:", err);
        setError("Failed to load sources. Please try refreshing the page."); // Set error message
        setSources([]); // Clear sources on error
      } finally {
        setIsLoadingSources(false); // Stop loading regardless of outcome
      }
    };

    fetchSources();
  }, []); // Empty dependency array means this runs once on mount

  // Example function to simulate getting an answer (replace with your actual logic)
  const handleAsk = (question) => {
    console.log("Question asked:", question);
    // Simulate API call or AI processing
    // Replace this with your actual fetch/logic to get the answer
    setAnswer({
      answer: `This is a simulated answer to the question: "${question}". The AI would provide a detailed response here, potentially citing sources. Ensure the response preserves formatting like\n\nnewlines and spacing.`,
      // citations: [...] // Add citations if your API provides them
    });
  };


  return (
    <div className="philquery-container">
      <div className="panel-card">
        {/* Panel Header */}
        <header>
          <h1 className="panel-title">🧠 PhilQuery</h1>
          <p className="panel-subtitle">
            AI-assisted philosophy Q&A with contextual citations. Explore ideas
            from foundational texts.
          </p>
        </header>

        {/* Available Sources Section */}
        <section className="source-list" aria-labelledby="sources-heading">
          <h2 id="sources-heading" className="section-heading">
            Available Sources
          </h2>
          {isLoadingSources && <p className="loading-message">Loading sources...</p>}
          {error && <p className="error-message">{error}</p>}
          {!isLoadingSources && !error && sources.length === 0 && (
            <p className="no-sources-message">No sources currently available.</p>
          )}
          {!isLoadingSources && !error && sources.length > 0 && (
            <ul>
              {sources.map((src, idx) => (
                <li key={idx} className="source-item">
                  <span className="source-title">{src.source_title}</span>
                  <span className="source-author"> by {src.author}</span>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* Ask Question Form Section (Uncomment and potentially pass handleAsk) */}
        {/*
        <section className="ask-form-section" aria-labelledby="ask-heading">
          <h2 id="ask-heading" className="section-heading">Ask a Question</h2>
          <AskQuestionForm onAsk={handleAsk} />
        </section>
        */}


        {/* Answer Display Section */}
        {answer && (
          <section className="answer-box" aria-live="polite">
            <h3>Answer:</h3>
            {/* Improved answer rendering: Handles potential object structures */}
            <p>
              {typeof answer === 'string'
                ? answer
                : answer.answer || JSON.stringify(answer, null, 2)}
            </p>
            {/* You might want to add citation rendering here if applicable */}
            {/* {answer.citations && renderCitations(answer.citations)} */}
          </section>
        )}
      </div>
    </div>
  );
}


// function renderCitations(citations) {
//   return (
//     <div className="citations-section">
//       <h4>Citations:</h4>
//       <ul>
//         {citations.map((cite, index) => (
//           <li key={index}>{cite.source_title} - {cite.details}</li>
//         ))}
//       </ul>
//     </div>
//   );
// }