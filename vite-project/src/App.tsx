import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [errorCount, setErrorCount] = useState<number | null>(null);
  const [errorMessages, setErrorMessages] = useState<string[]>([]);
  const [isPaused, setIsPaused] = useState(false);
  const [progress, setProgress] = useState<number | null>(null);

  useEffect(() => {
    // Function to fetch initial progress data and update the button text
    const fetchInitialProgress = () => {
      fetch('http://localhost:8000/api/toggle', {
        method: 'GET',
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Progress request failed');
          }
        })
        .then((progressData) => {
          setIsPaused(!progressData.is_sending);
          setProgress(progressData.is_sending ? (progressData.emails_sent / progressData.total_emails) * 100 : null);
        })
        .catch((error) => {
          console.error('Progress request error:', error);
        });
    };

    // Fetch initial progress data when the component mounts
    fetchInitialProgress();

    // Start polling for progress every 4 seconds
    const intervalId = setInterval(() => {
      fetchInitialProgress();
    }, 4000);

    return () => {
      // Cleanup function to stop polling on component unmount
      clearInterval(intervalId);
    };
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
      setErrorCount(null);
      setErrorMessages([]);
    }
  };

  const handleUpload = () => {
    if (file) {
      const formData = new FormData();
      formData.append('csv_file', file);

      setUploading(true);

      fetch('http://localhost:8000/api/upload_csv', {
        method: 'POST',
        body: formData,
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            return response.json();
          }
        })
        .then((data) => {
          if (data && data.errors && data.errors.length > 0) {
            data.errors.forEach((error) => {
              setErrorCount((prevCount) => (prevCount !== null ? prevCount + 1 : 1));
              setErrorMessages((prevMessages) => [...prevMessages, error]);
            });
          } else {
            alert('CSV file upload started successfully.');
          }
        })
        .catch((error) => {
          alert('An unexpected error occurred: ' + error.message);
          setErrorCount(1);
          setErrorMessages([`An unexpected error occurred: ${error.message}`]);
        })
        .finally(() => {
          setUploading(false);
        });
    }
  };

  const handleDismissError = (index: number) => {
    setErrorMessages((prevMessages) => prevMessages.filter((_, i) => i !== index));
    setErrorCount((prevCount) => (prevCount !== null ? prevCount - 1 : null));
  };

  const handleDismissAllErrors = () => {
    setErrorMessages([]);
    setErrorCount(null);
  };

  const handleToggle = () => {
    fetch('http://localhost:8000/api/toggle', {
      method: 'POST',
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Toggle request failed');
        }
      })
      .then((data) => {
        setIsPaused(data.paused);
      })
      .catch((error) => {
        console.error('Toggle request error:', error);
      });
  };

  return (
    <div className="container d-flex flex-column align-items-center justify-content-center" style={{ height: '100vh' }}>
      <div className="card mb-3">
        <div className="card-body text-center">
          <h1 className="mb-4">Upload File</h1>
          <form id="uploadForm" encType="multipart/form-data">
            <div className="mb-3">
              <label htmlFor="file" className="form-label visually-hidden">
                Select a file
              </label>
              <div className="mb-4">
                <input
                  type="file"
                  className="form-control visually-hidden"
                  id="fileInput"
                  name="file"
                  onChange={handleFileChange}
                />
                <label htmlFor="fileInput" style={{ cursor: 'pointer' }}>
                  {/* Your file input label/icon */}
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="56"
                    height="56"
                    fill="none"
                    viewBox="0 0 56 56"
                    color="#405771"
                  >
                    <path
                      stroke="#405771"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="5"
                      d="M38 28 28 18m0 0L18 28m10-10v23c0 3.477 0 5.215 1.376 7.161.915 1.294 3.547 2.89 5.117 3.102 2.362.32 3.26-.148 5.053-1.083C47.543 46.009 53 37.642 53 28 53 14.193 41.807 3 28 3S3 14.193 3 28c0 9.254 5.027 17.333 12.5 21.656"
                    ></path>
                  </svg>
                </label>
              </div>
            </div>
            <div className="mb-3">
              <button
                type="button"
                onClick={handleUpload}
                className="btn btn-primary mx-auto d-block"
                disabled={uploading}
              >
                {uploading ? 'Uploading...' : 'Upload'}
              </button>
            </div>
          </form>

          {errorCount !== null && (
            <div className="mb-3">
              <p>{`Received ${errorCount > 10 ? 'more than 10' : errorCount} error${
                errorCount !== 1 ? 's' : ''
              }:`}</p>
              {errorCount <= 10 &&
                errorMessages.map((error, index) => (
                  <div
                    key={index}
                    className="border shadow p-3 mb-2 bg-white rounded"
                    style={{ borderColor: 'red' }}
                  >
                    <p className="card-text">{error}</p>
                    <button
                      type="button"
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDismissError(index)}
                    >
                      Close
                    </button>
                    <div style={{ borderTop: '1px solid red' }}></div>
                  </div>
                ))}
              {errorCount > 10 && <p>We had {errorCount} errors. Please check your file.</p>}
              {errorCount > 0 && (
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={handleDismissAllErrors}
                >
                  Close All Errors
                </button>
              )}
            </div>
          )}

        </div>
      </div>

      <div className="mb-3" style={{ width: '100%' }}>
        <hr style={{ borderTop: '2px solid #405771', width: '100%' }} /> {/* Line above the button */}

        <h2 style={{ marginTop: '10px', marginBottom: '10px' }}>Sending Email Process</h2> {/* Larger and centered header */}

        <button
          type="button"
          onClick={handleToggle}
          className="btn btn-secondary mx-auto d-block mt-3"
        >
          {isPaused ? 'Resume' : 'Pause'}
        </button>

        <div className="mt-3">
          {progress !== null && (
            <div className="progress">
              <div
                className="progress-bar"
                role="progressbar"
                style={{ width: `${progress}%` }}
                aria-valuenow={progress}
                aria-valuemin={0}
                aria-valuemax={100}
              ></div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
