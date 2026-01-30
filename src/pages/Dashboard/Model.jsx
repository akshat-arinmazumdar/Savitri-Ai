import { useState, useRef } from 'react'

const Model = () => {
    const [status, setStatus] = useState("Idle")
    const [logs, setLogs] = useState(["Waiting for file upload...", "> System ready."])
    const fileInputRef = useRef(null)

    const handleUploadClick = () => {
        fileInputRef.current.click()
    }

    const handleFileChange = async (event) => {
        const file = event.target.files[0]
        if (!file) return

        if (file.type !== "application/pdf") {
            addLog("❌ Error: Only PDF files are allowed.")
            return
        }

        setStatus("Uploading...")
        addLog(`📂 Uploading: ${file.name}...`)

        const formData = new FormData()
        formData.append("file", file)

        try {
            const response = await fetch("http://localhost:8001/api/upload", {
                method: "POST",
                body: formData,
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || "Upload failed")
            }

            const data = await response.json()
            addLog("✅ Upload successful!")
            addLog(`📄 Server File ID: ${data.filename}`)
            setStatus("Processing")

            // Allow user to proceed to topic extraction (future step)
            // fetchTopics(data.filename) 

        } catch (error) {
            console.error("Upload error:", error)
            setStatus("Error")
            addLog(`❌ Upload Failed: ${error.message}`)
        }
    }

    const addLog = (message) => {
        setLogs(prev => [...prev, message])
    }

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
                <p>Ready to convert your notes into podcasts.</p>

                <div className="main-layout">
                    {/* Left Side: Input & Playlist */}
                    <div className="workspace-container">
                        <div className="upload-box" onClick={handleUploadClick}>
                            <div className="plus-icon">+</div>
                            <span>Upload PDF Page</span>
                            <input
                                type="file"
                                ref={fileInputRef}
                                style={{ display: "none" }}
                                accept=".pdf"
                                onChange={handleFileChange}
                            />
                        </div>

                        <div className="playlist-section">
                            <h3>Generated Audio Playlist</h3>
                            <div className="playlist-container">
                                {/* Placeholder items */}
                                <div className="playlist-item">
                                    <span className="play-icon">▶</span>
                                    <div className="track-info">
                                        <span className="track-title">Physics Chapter 1 - Motion</span>
                                        <span className="track-duration">12:34</span>
                                    </div>
                                </div>
                                <div className="playlist-item">
                                    <span className="play-icon">▶</span>
                                    <div className="track-info">
                                        <span className="track-title">History Notes - WW2</span>
                                        <span className="track-duration">08:45</span>
                                    </div>
                                </div>
                                <div className="playlist-item">
                                    <span className="play-icon">▶</span>
                                    <div className="track-info">
                                        <span className="track-title">Chemistry - Bonding</span>
                                        <span className="track-duration">15:20</span>
                                    </div>
                                </div>
                                <div className="playlist-item">
                                    <span className="play-icon">▶</span>
                                    <div className="track-info">
                                        <span className="track-title">Biology - Cells</span>
                                        <span className="track-duration">10:15</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Side: Output Panel */}
                    <div className="output-panel">
                        <div className="output-header">
                            <h3>Processing Output</h3>
                            <span className="status-badge">{status}</span>
                        </div>
                        <div className="output-console">
                            <p className="console-text">
                                {logs.map((log, index) => (
                                    <span key={index}>{log}<br /></span>
                                ))}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Model
