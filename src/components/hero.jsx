import Navbar from './navbar';
import { useNavigate } from 'react-router-dom';

const Hero = () => {
    const navigate = useNavigate();

    return (
        <section className="hero-container">
            <Navbar />
            <div className="hero-content">
                <h1 className="hero-title">Savitri-Ai</h1>
                <p className="hero-subtitle">From Concepts to Confidence</p>
                <button className="hero-button" onClick={() => navigate('/model')}>Get Started</button>
            </div>
        </section>
    )
}

export default Hero
