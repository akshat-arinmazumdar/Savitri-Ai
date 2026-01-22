const Model = () => {
    return (
        <div className="dashboard-container">
            <nav className="dashboard-nav">
                <h1>Savitri-Ai Engine</h1>
                <div className="user-profile">
                    <span>User</span>
                </div>
            </nav>
            <div className="dashboard-content">
                <h2>Model Dashboard</h2>
                <p>Ready to convert your notes into podcasts.</p>

                <div className="workspace-container">
                    <div className="upload-box">
                        <div className="plus-icon">+</div>
                        <span>Upload PDF Page</span>
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
            </div>
        </div>
    )
}

export default Model
