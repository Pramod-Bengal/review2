import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Mail,
  Globe,
  Code,
  Video,
  Palette,
  Sparkles,
  ExternalLink,
  ArrowRight,
  Send,
  Check,
  Menu,
  X,
  Layers,
  Cpu
} from 'lucide-react'

import pramodAvatar from './assets/pramod_avatar.png'
import akashAvatar from './assets/akash_avatar.png'
import designProject from './assets/design_project.png'
import videoProject from './assets/video_project.png'
import heroImg from './assets/hero.png'
import './App.css'

const GithubIcon = (props) => (
  <svg
    viewBox="0 0 24 24"
    width="20"
    height="20"
    stroke="currentColor"
    strokeWidth="2"
    fill="none"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
    <path d="M9 18c-4.51 2-5-2-7-2" />
  </svg>
)

function App() {
  const [activeTab, setActiveTab] = useState('all')
  const [formSubmitted, setFormSubmitted] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  })

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (formData.name && formData.email && formData.message) {
      setFormSubmitted(true)
      setTimeout(() => {
        setFormSubmitted(false)
        setFormData({ name: '', email: '', message: '' })
      }, 3500)
    }
  }

  const projects = [
    {
      id: 1,
      title: "AI Financial & Web Intelligence Hub",
      category: "development",
      description: "A secure FastAPI + React executive intelligence dashboard that scrapes websites and uses Gemini models to analyze profit, loss, and customer acquisition channels.",
      image: heroImg,
      tags: ["FastAPI", "React", "Gemini AI", "Web Scraping"],
      link: "#"
    },
    {
      id: 2,
      title: "Creative Branding & Visual Systems",
      category: "design",
      description: "Premium user interfaces, typography guidelines, and complete branding identity systems tailored for modern digital applications.",
      image: designProject,
      tags: ["UI/UX Design", "Figma", "Branding", "Illustrator"],
      link: "#"
    },
    {
      id: 3,
      title: "Cinematic Editing & Motion Graphics",
      category: "video",
      description: "Dynamic video campaigns, precise color grading, sound design, and custom logo reveals built for corporate clients and startup promotions.",
      image: videoProject,
      tags: ["Premiere Pro", "After Effects", "Color Grading", "VFX"],
      link: "#"
    }
  ]

  const filteredProjects = activeTab === 'all' 
    ? projects 
    : projects.filter(p => p.category === activeTab)

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15 }
    }
  }

  const itemVariants = {
    hidden: { y: 30, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: { type: "spring", stiffness: 100, damping: 15 }
    }
  }

  return (
    <div className="portfolio-app">
      {/* Background decoration */}
      <div className="bg-glow bg-glow-1"></div>
      <div className="bg-glow bg-glow-2"></div>
      <div className="grid-overlay"></div>

      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-container">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="logo-area"
          >
            <span className="logo-gradient">PA</span>
            <span className="logo-text">Architects of Digital</span>
          </motion.div>

          <div className="nav-linksdesktop">
            <a href="#about">The Duo</a>
            <a href="#projects">Our Work</a>
            <a href="#skills">Capabilities</a>
            <a href="#contact" className="nav-cta-btn">Let's Connect</a>
          </div>

          <button className="mobile-menu-toggle" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mobile-nav-links"
            >
              <a href="#about" onClick={() => setMobileMenuOpen(false)}>The Duo</a>
              <a href="#projects" onClick={() => setMobileMenuOpen(false)}>Our Work</a>
              <a href="#skills" onClick={() => setMobileMenuOpen(false)}>Capabilities</a>
              <a href="#contact" className="mobile-cta-btn" onClick={() => setMobileMenuOpen(false)}>Let's Connect</a>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="hero-badge"
          >
            <Sparkles size={14} className="accent-color" />
            <span>Developer & Designer Synergy</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.1 }}
            className="hero-title"
          >
            We Architect <span className="text-gradient">Experiences</span>,<br />
            Create <span className="text-gradient-alt">Designs</span> & Edit <span className="text-gradient-third">Stories</span>.
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="hero-description"
          >
            A dynamic developer-designer power duo delivering high-end full-stack applications, interactive UI/UX designs, and cinematic video editing.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="hero-ctas"
          >
            <a href="#projects" className="btn-primary">
              Explore Our Work <ArrowRight size={16} />
            </a>
            <a href="#contact" className="btn-secondary">
              Get in Touch
            </a>
          </motion.div>
        </div>

        {/* Floating visual representation */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.85 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.4 }}
          className="hero-visual"
        >
          <div className="hero-frame">
            <img src={heroImg} alt="AI Dashboard mockup" className="hero-mockup-img" />
            <div className="hero-frame-glow"></div>
          </div>
        </motion.div>
      </section>

      {/* About Section - The Duo */}
      <section id="about" className="about-section">
        <div className="section-header">
          <h2>Meet the Duo</h2>
          <p>Two minds combining engineering rigor with artistic flair to build digital dominance.</p>
        </div>

        <motion.div 
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="duo-grid"
        >
          {/* Pramod Card */}
          <motion.div variants={itemVariants} className="profile-card profile-card-left">
            <div className="profile-image-wrap">
              <img src={pramodAvatar} alt="Pramod Benagal" className="profile-avatar" />
              <div className="profile-glow shadow-purple"></div>
            </div>
            <div className="profile-info">
              <span className="profile-role">Web Architect</span>
              <h3>Pramod Benagal</h3>
              <p>Specializes in crafting scalable backend architectures, high-performance web systems, and complex AI APIs.</p>
              
              <div className="profile-skills-quick">
                <span>FastAPI</span>
                <span>React.js</span>
                <span>Node.js</span>
                <span>AI Agent Integration</span>
              </div>

              <div className="profile-socials">
                <a href="https://github.com/Pramod-Bengal" target="_blank" rel="noopener noreferrer"><GithubIcon /></a>
                <a href="mailto:pramodbenagal@gmail.com"><Mail size={18} /></a>
              </div>
            </div>
          </motion.div>

          {/* Akash Card */}
          <motion.div variants={itemVariants} className="profile-card profile-card-right">
            <div className="profile-image-wrap">
              <img src={akashAvatar} alt="Akash" className="profile-avatar" />
              <div className="profile-glow shadow-cyan"></div>
            </div>
            <div className="profile-info">
              <span className="profile-role">Creative Designer</span>
              <h3>Akash</h3>
              <p>Translates visions into jaw-dropping graphic designs, pixel-perfect user interfaces, and premium motion videos.</p>
              
              <div className="profile-skills-quick">
                <span>UI/UX</span>
                <span>Figma</span>
                <span>Premiere Pro</span>
                <span>After Effects</span>
              </div>

              <div className="profile-socials">
                <a href="#" target="_blank" rel="noopener noreferrer"><Globe size={18} /></a>
                <a href="mailto:akash@example.com"><Mail size={18} /></a>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </section>

      {/* Projects Section */}
      <section id="projects" className="projects-section">
        <div className="section-header">
          <h2>Featured Creations</h2>
          <p>Explore a selection of our latest development, design, and video editing masterpieces.</p>
        </div>

        {/* Tab filters */}
        <div className="tabs-container">
          <button 
            className={`tab-btn ${activeTab === 'all' ? 'active' : ''}`}
            onClick={() => setActiveTab('all')}
          >
            All Work
          </button>
          <button 
            className={`tab-btn ${activeTab === 'development' ? 'active' : ''}`}
            onClick={() => setActiveTab('development')}
          >
            <Code size={14} /> Coding
          </button>
          <button 
            className={`tab-btn ${activeTab === 'design' ? 'active' : ''}`}
            onClick={() => setActiveTab('design')}
          >
            <Palette size={14} /> Design
          </button>
          <button 
            className={`tab-btn ${activeTab === 'video' ? 'active' : ''}`}
            onClick={() => setActiveTab('video')}
          >
            <Video size={14} /> Video Editing
          </button>
        </div>

        {/* Projects Grid */}
        <motion.div 
          layout
          className="projects-grid"
        >
          <AnimatePresence mode="popLayout">
            {filteredProjects.map((project) => (
              <motion.div
                layout
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.4 }}
                key={project.id}
                className="project-card"
              >
                <div className="project-image-wrap">
                  <img src={project.image} alt={project.title} className="project-image" />
                  <div className="project-overlay">
                    <a href={project.link} className="project-link-btn">
                      <ExternalLink size={18} />
                    </a>
                  </div>
                </div>
                <div className="project-details">
                  <span className="project-category">{project.tags.join(' • ')}</span>
                  <h4>{project.title}</h4>
                  <p>{project.description}</p>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>
      </section>

      {/* Capabilities / Skills Section */}
      <section id="skills" className="skills-section">
        <div className="section-header">
          <h2>Capabilities Grid</h2>
          <p>Our stack is curated for fast deliveries, high-end visual designs, and bulletproof infrastructure.</p>
        </div>

        <div className="capabilities-grid">
          <div className="capability-box card-purple">
            <div className="capability-icon"><Code size={20} /></div>
            <h5>Web & API Architectures</h5>
            <p>Developing ultra-fast REST & WebSockets APIs with FastAPI, backend logic in Node.js, and robust microservices.</p>
          </div>
          <div className="capability-box card-cyan">
            <div className="capability-icon"><Palette size={20} /></div>
            <h5>Interactive UI/UX Design</h5>
            <p>Creating interactive Figma prototypes, dynamic web designs, sleek dark themes, and optimized layout design systems.</p>
          </div>
          <div className="capability-box card-magenta">
            <div className="capability-icon"><Video size={20} /></div>
            <h5>Post-Production & FX</h5>
            <p>Cinematic cut editing, custom color grading, sound modeling, title sequences, and immersive visual FX setups.</p>
          </div>
          <div className="capability-box card-orange">
            <div className="capability-icon"><Cpu size={20} /></div>
            <h5>Generative AI Agents</h5>
            <p>Configuring Large Language Models (LLM) agents, prompt routing engines, automated web scraping models, and intelligent chat flows.</p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact-section">
        <div className="contact-card-wrapper">
          <div className="contact-card-info">
            <span className="info-badge">Join forces</span>
            <h3>Ready to scale your next project?</h3>
            <p>Whether it is full-scale web development, custom assets, UI design, or premium media editing - we have you covered.</p>
            
            <div className="contact-quick-list">
              <div className="contact-item">
                <Mail size={16} className="text-gradient-icon" />
                <span>pramodbenagal@gmail.com</span>
              </div>
              <div className="contact-item">
                <Check size={16} className="text-gradient-icon" />
                <span>Available for contract & remote roles</span>
              </div>
            </div>
          </div>

          <div className="contact-card-form">
            <AnimatePresence mode="wait">
              {!formSubmitted ? (
                <motion.form 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  onSubmit={handleSubmit}
                  className="contact-form"
                >
                  <div className="input-group">
                    <label htmlFor="name">Name</label>
                    <input 
                      type="text" 
                      id="name" 
                      name="name" 
                      value={formData.name} 
                      onChange={handleInputChange} 
                      placeholder="Your Name" 
                      required 
                    />
                  </div>
                  <div className="input-group">
                    <label htmlFor="email">Email</label>
                    <input 
                      type="email" 
                      id="email" 
                      name="email" 
                      value={formData.email} 
                      onChange={handleInputChange} 
                      placeholder="email@example.com" 
                      required 
                    />
                  </div>
                  <div className="input-group">
                    <label htmlFor="message">Message</label>
                    <textarea 
                      id="message" 
                      name="message" 
                      value={formData.message} 
                      onChange={handleInputChange} 
                      placeholder="Tell us about your project..." 
                      rows="4" 
                      required
                    ></textarea>
                  </div>
                  <button type="submit" className="submit-btn">
                    Send Message <Send size={14} />
                  </button>
                </motion.form>
              ) : (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="form-success-state"
                >
                  <Check size={48} className="success-icon" />
                  <h4>Message Sent Successfully!</h4>
                  <p>Thank you. We will get back to you shortly.</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <p>&copy; {new Date().getFullYear()} Pramod & Akash. All rights reserved.</p>
        <div className="footer-links">
          <a href="https://github.com/Pramod-Bengal" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="#about">The Duo</a>
          <a href="#projects">Work</a>
        </div>
      </footer>
    </div>
  )
}

export default App
