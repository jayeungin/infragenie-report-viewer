import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [reports, setReports] = useState([]);
    const [message, setMessage] = useState('');

    const API_BASE_URL = '/api'; // Use a relative path for OpenShift Route

    useEffect(() => {
        fetchReports();
    }, []);

    const fetchReports = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/reports`);
            const data = await response.json();
            setReports(data);
        } catch (error) {
            setMessage('Could not fetch reports.');
        }
    };

    const onFileChange = event => {
        setSelectedFile(event.target.files[0]);
    };

    const onFileUpload = async () => {
        if (!selectedFile) {
            setMessage('Please select a file first!');
            return;
        }
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch(`${API_BASE_URL}/upload`, {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            setMessage(data.message || data.error);
            document.getElementById("file-input").value = "";
            fetchReports();
        } catch (error) {
            setMessage('File upload failed.');
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Report Viewer</h1>
                <p>Upload reports to OpenShift Data Foundation</p>
                <div>
                    <input id="file-input" type="file" onChange={onFileChange} />
                    <button onClick={onFileUpload}>Upload</button>
                </div>
                {message && <p className="message">{message}</p>}
            </header>
            <main className="App-main">
                <h2>Available Reports</h2>
                {reports.length > 0 ? (
                    <ul>
                        {reports.map((report, index) => (
                            <li key={index}>
                                <a href={report.url} target="_blank" rel="noopener noreferrer">
                                    {report.name}
                                </a>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No reports found in ODF bucket.</p>
                )}
            </main>
        </div>
    );
}

export default App;