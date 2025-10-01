"use client"
import { React } from 'react';
import Link from 'next/link';
import NavLink from './NavLink';
import Image from 'next/image';

function NavBar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark" role="navigation">
      <div className="container">
        <Link href="/" className="navbar-brand">
          {process.env.NEXT_PUBLIC_NAME}
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <NavLink name="Resume" link="/resume" />
            <NavLink name="Projects" link="/portfolio" />
            <NavLink name="About" link="/about" />
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
