import React, { useEffect } from 'react';
import './LandingPage.css';

const LandingPage = () => {
    useEffect(() => {
        document.title = "Beautiful Mind | Research at AUB";
    }, []);

    return (
        <div className="landing-page">
            <nav>
                <div className="logo-container">
                    <span className="project-name">Beautiful Mind</span>
                </div>
            </nav>

            <header className="hero">
                <div className="hero-content">
                    <h1>Understanding <br /><span style={{ color: '#60a5fa' }}>Inner Voice</span></h1>
                    <p>The Beautiful Mind project is a pioneering research initiative at Chehab Lab, American University of
                        Beirut. We collect audio journals to unlock insights into mental well-being through advanced analysis.
                    </p>
                    <a href="#about" className="btn">Learn More</a>
                </div>
                <div className="hero-image">
                    <img src="/hero.png" alt="Abstract Brain Visualization" />
                </div>
            </header>

            <section id="about">
                <h2>About the Project</h2>
                <div className="grid">
                    <div className="card">
                        <i className="fas fa-microphone-lines"></i>
                        <h3>Audio Journals</h3>
                        <p>Participants share their daily thoughts and emotions through secure, private voice recordings.</p>
                    </div>
                    <div className="card">
                        <i className="fas fa-chart-line"></i>
                        <h3>Insightful Analysis</h3>
                        <p>We use cutting-edge computational methods to analyze transcribed text and sentiment to better
                            understand mental health.</p>
                    </div>
                    <div className="card">
                        <i className="fas fa-building-columns"></i>
                        <h3>Chehab Lab at AUB</h3>
                        <p>A flagship research initiative within the American University of Beirut (AUB), led by dedicated
                            researchers.</p>
                    </div>
                </div>
            </section>

            <section id="privacy" className="privacy-section">
                <div className="privacy-highlight">
                    <h2>Your Privacy is Our Priority</h2>
                    <p style={{ maxWidth: '800px', margin: '0 auto', color: 'var(--text-muted)', fontSize: '1.1rem' }}>
                        The Beautiful Mind project is built on trust. All collected data is strictly secured and completely
                        anonymized.
                        Your identity is never linked to your recordings, ensuring your journey remains private while
                        contributing to vital research.
                    </p>
                </div>
            </section>

            <section id="contact" className="contact-section">
                <h2>Get in Touch</h2>
                <p style={{ marginBottom: '2rem', color: 'var(--text-muted)' }}>Interested in participating or learning more about our
                    research?</p>
                <a href="mailto:amm90@mail.aub.edu" className="email-link">amm90@mail.aub.edu</a>
                <div style={{ marginTop: '3rem' }}>
                    <p>American University of Beirut</p>
                    <p>Chehab Lab Research Initiative</p>
                </div>
            </section>

            <section id="legal" className="legal-section">
                <h2>Legal Information</h2>
                <div className="legal-grid">
                    <div className="legal-card">
                        <h3>Research Participation</h3>
                        <p>By participating in the Beautiful Mind Project, you contribute to a research initiative at AUB's
                            Chehab Lab. Your participation is voluntary and focused on advancing mental health analytics.</p>
                    </div>
                    <div className="legal-card">
                        <h3>Data Usage & Security</h3>
                        <p>All data is processed using state-of-the-art anonymization techniques to ensure participant privacy and confidentiality. Audio files are stored securely using industry-standard protection measures and are accessible only to authorized research personnel. Audio processing is performed through OpenAI APIs in accordance with applicable data protection standards. We do not sell, trade, or share any individual-level data with third parties under any circumstances.</p>
                    </div>
                    <div className="legal-card">
                        <h3>Medical Disclaimer</h3>
                        <p>This project is for research purposes only. It does not provide medical advice, diagnosis, or
                            treatment. It is not a substitute for professional mental health services or emergency intervention.
                        </p>
                    </div>
                    <div className="legal-card">
                        <h3>Terms of Service</h3>
                        <p>Use of this platform constitutes acceptance of our research protocols. Users must be 18+ or have
                            parental consent. We reserve the right to terminate access if protocols are violated.</p>
                    </div>
                </div>
            </section>

            <footer>
                <div className="footer-links">
                    <a href="#about">About</a>
                    <a href="#privacy">Privacy</a>
                    <a href="#legal">Legal Terms</a>
                    <a href="#contact">Contact</a>
                </div>
                <p>&copy; 2026 Beautiful Mind Project - Chehab Lab, AUB. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default LandingPage;
