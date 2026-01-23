import { useState, useEffect } from 'react';

const Model = () => {
    const [file, setFile] = useState(null);
    const [topics, setTopics] = useState([]);
    const [isProcessing, setIsProcessing] = useState(false);
    const [status, setStatus] = useState('Idle');
    const [logs, setLogs] = useState(['> System ready. Waiting for file upload...']);
    const [audioInstance, setAudioInstance] = useState(null);
    const [playingIndex, setPlayingIndex] = useState(null);

    const addLog = (msg) => setLogs(prev => [...prev, `> ${msg}`]);

    const handleUpload = async (e) => {
        const selectedFile = e.target.files[0];
        if (!selectedFile) return;

        setFile(selectedFile);
        setIsProcessing(true);
        setStatus('Uploading...');
        addLog(`Uploading ${selectedFile.name}...`);

        // Stop any current audio
        if (audioInstance) {
            audioInstance.pause();
            setAudioInstance(null);
            setPlayingIndex(null);
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const uploadRes = await fetch('http://localhost:8000/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!uploadRes.ok) throw new Error('Upload failed');

            setStatus('Analyzing...');
            addLog('PDF Uploaded. Extracting topics...');

            const topicsRes = await fetch(`http://localhost:8000/api/topics?filename=${selectedFile.name}`);
            const topicsData = await topicsRes.json();

            setTopics(topicsData.topics.map(t => ({
                title: t,
                filename: sanitizeFilename(t),
                status: 'pending'
            })));

            setStatus('Ready');
            addLog(`Found ${topicsData.topics.length} topics. Ready to learn!`);
        } catch (err) {
            setStatus('Error');
            addLog(`Error: ${err.message}`);
        } finally {
            setIsProcessing(false);
        }
    };

    const sanitizeFilename = (name) => {
        return name.replace(/[^\w\s\.-]/g, '').trim().replace(/\s+/g, '_').toLowerCase().substring(0, 60) + "_v2.mp3";
    };

    const handlePlayTopic = async (index) => {
        // Toggle Logic for same track
        if (playingIndex === index && audioInstance) {
            if (audioInstance.paused) {
                audioInstance.play();
                setStatus('Playing');
                addLog(`Resumed: ${topics[index].title}`);
            } else {
                audioInstance.pause();
                setStatus('Paused');
                addLog(`Paused: ${topics[index].title}`);
            }
            return;
        }

        // Stop old audio if switching tracks
        if (audioInstance) {
            audioInstance.pause();
        }

        const topic = topics[index];
        const updatedTopics = [...topics];

        try {
            if (updatedTopics[index].status !== 'ready') {
                updatedTopics[index].status = 'generating';
                setTopics(updatedTopics);
                setStatus('Generating...');
                addLog(`Generating audio for: ${topic.title}...`);

                const res = await fetch('http://localhost:8000/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic: topic.title, filename: topic.filename })
                });

                if (!res.ok) throw new Error('Generation failed');

                updatedTopics[index].status = 'ready';
                setTopics([...updatedTopics]);
                addLog('Audio ready. Playing...');
            }

            const newAudio = new Audio(`http://localhost:8000/api/voices/${topic.filename}`);
            setAudioInstance(newAudio);
            setPlayingIndex(index);

            newAudio.play();
            setStatus('Playing');

            newAudio.onended = () => {
                setStatus('Ready');
                setPlayingIndex(null);
            };
        } catch (err) {
            addLog(`Error: ${err.message}`);
            setStatus('Error');
        }
    };

    return (
        <div className="dashboard-container">
            <nav className="dashboard-nav">
                <h1>Savitri-Ai</h1>
                <div className="user-profile">
                    <span>User</span>
                </div>
            </nav>
            <div className="dashboard-content">
                <h2>Model Dashboard</h2>
                <p>Convert your notes into lessons with Neerja.</p>

                <div className="main-layout">
                    {/* Left Side: Input & Playlist */}
                    <div className="workspace-container">
                        <label className="upload-box" style={{ cursor: 'pointer' }}>
                            <input type="file" onChange={handleUpload} style={{ display: 'none' }} accept=".pdf" />
                            <div className="plus-icon">{isProcessing ? '⏳' : '+'}</div>
                            <span>{file ? file.name : 'Upload PDF Page'}</span>
                        </label>

                        <div className="playlist-section">
                            <h3>Lesson Playlist</h3>
                            <div className="playlist-container">
                                {topics.length === 0 && <p style={{ padding: '20px', color: '#888' }}>Upload a PDF to see topics.</p>}
                                {topics.map((t, i) => (
                                    <div key={i} className={`playlist-item ${t.status} ${playingIndex === i ? 'playing' : ''}`} onClick={() => handlePlayTopic(i)}>
                                        <span className="play-icon">
                                            {t.status === 'generating' ? '⏳' : (playingIndex === i && status === 'Playing' ? '⏸' : '▶')}
                                        </span>
                                        <div className="track-info">
                                            <span className="track-title">{t.title}</span>
                                            <span className="track-status">{t.status === 'ready' ? 'Ready' : t.status === 'generating' ? 'Generating...' : 'New'}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Right Side: Output Panel */}
                    <div className="output-panel">
                        <div className="output-header">
                            <h3>Processing Output</h3>
                            <span className={`status-badge ${status.toLowerCase()}`}>{status}</span>
                        </div>
                        <div className="output-console">
                            <div className="console-text">
                                {logs.map((log, i) => <div key={i}>{log}</div>)}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <style jsx="true">{`
                .track-status { font-size: 0.8rem; color: #888; margin-top: 4px; display: block; }
                .playlist-item.ready { border-left: 4px solid #4CAF50 !important; }
                .playlist-item.generating { background: rgba(255, 255, 255, 0.05) !important; }
                .status-badge.error { background: #f44336 !important; }
                .status-badge.ready { background: #4CAF50 !important; }
                .status-badge.uploading, .status-badge.analyzing { background: #2196F3 !important; }
            `}</style>
        </div>
    )
}

export default Model
