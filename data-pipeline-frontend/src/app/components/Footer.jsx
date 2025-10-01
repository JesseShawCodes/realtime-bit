"use client"
import { React } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faGithub,
  faInstagram, faLinkedin, faXTwitter,
} from '@fortawesome/free-brands-svg-icons';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';

function Footer() {
  return (
    <div className="bg-gradient-my-gradient-footer">
      <footer className="container py-3 my-4" role="contentinfo">
        <div className="d-flex align-items-center justify-content-lg-between w-100">
          <div className="mb-3 mb-md-0">© 2025 {process.env.NEXT_PUBLIC_NAME}</div>
        </div>
      </footer>
    </div>
  );
}

export default Footer;
