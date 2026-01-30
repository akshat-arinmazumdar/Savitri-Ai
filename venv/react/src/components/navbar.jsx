const Navbar = () => {
    const scrollToSection = (sectionId) => {
        const element = document.getElementById(sectionId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    return (
        <nav className="navbar">
            <ul className="nav-list">
                <li><a href="#hero" className="nav-link" onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}>Home</a></li>
                <li><a href="#about" className="nav-link" onClick={(e) => { e.preventDefault(); scrollToSection('about'); }}>About</a></li>
                <li><a href="#contact" className="nav-link" onClick={(e) => { e.preventDefault(); scrollToSection('contact'); }}>Contact</a></li>
            </ul>
        </nav>
    )
}

export default Navbar