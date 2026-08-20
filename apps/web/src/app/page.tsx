'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

export default function LandingPage() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };
    const handleResize = () => {
      const aspect = window.innerWidth / window.innerHeight;
      if (aspect > 1.1) {
        setIsOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <>
      <style
        dangerouslySetInnerHTML={{
          __html: `
        :root {
          --ink: #fafafa;
          --muted: #a7a6a6;
          --nav: #b6b5b5;
          --strip: #8b8a8a;
          --pill: #ffffff;
          --pill-ink: #050505;
          --bg: #050505;

          /* Reference canvas: 1487 x 1058 */
          --u: calc(100vh / 1058);
          --uw: calc(100vw / 1487);
          --h: clamp(var(--u), calc(var(--u) * 0.65 + var(--uw) * 0.35), calc(var(--u) * 1.16));
        }

        @supports (height: 100dvh) {
          :root {
            --u: calc(100dvh / 1058);
          }
        }

        @media (max-aspect-ratio: 11/10) {
          :root {
            --m: min(100vw / 430, 1.34px);
            --u: var(--m);
            --h: var(--m);
          }
        }

        @media (min-width: 600px) and (max-aspect-ratio: 11/10) {
          :root {
            --m: min(100vw / 860, 100vh / 760, 1.25px);
            --u: var(--m);
            --h: var(--m);
          }
        }

        .stage {
          position: relative;
          width: 100vw;
          height: 100vh;
          height: 100dvh;
          overflow: hidden;
          background-color: var(--bg);
        }

        .plate {
          position: absolute;
          inset: 0;
          overflow: hidden;
          pointer-events: none;
          z-index: 1;
        }

        .plate-video {
          position: absolute;
          left: 50%;
          top: calc(1 * var(--u));
          width: calc(1492 * var(--u));
          height: calc(1054 * var(--u));
          transform: translateX(calc(-50% - calc(0.5 * var(--u))));
          object-fit: cover;
          pointer-events: none;
        }

        .plate::after {
          content: '';
          position: absolute;
          inset: 0;
          pointer-events: none;
          background-image:
            linear-gradient(to bottom,
              rgba(5,5,5,0) 78.8%,
              rgba(5,5,5,.23) 79.6%,
              rgba(5,5,5,.45) 81.4%,
              rgba(5,5,5,.75) 83.3%,
              rgba(5,5,5,.84) 85.2%,
              rgba(5,5,5,.888) 88%,
              rgba(5,5,5,.905) 91%,
              rgba(5,5,5,.96) 95%,
              #050505 100%
            ),
            linear-gradient(to right,
              #050505 calc(50% - 746 * var(--u)),
              transparent calc(50% - 676 * var(--u)),
              transparent calc(50% + 676 * var(--u)),
              #050505 calc(50% + 746 * var(--u))
            );
        }

        .topbar {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: calc(105 * var(--u));
          z-index: 10;
          pointer-events: none;
        }

        .brand {
          position: absolute;
          left: calc(75 * var(--u));
          top: calc(27 * var(--u));
          width: calc(31.5 * var(--u));
          height: calc(48.5 * var(--u));
          display: block;
          pointer-events: auto;
          animation: rise 0.8s cubic-bezier(.22, 1, .36, 1) both;
        }

        .brand svg {
          width: 100%;
          height: 100%;
          display: block;
        }

        .links {
          position: absolute;
          left: 50%;
          top: calc(51 * var(--u));
          transform: translate(-50%, -50%);
          display: flex;
          align-items: center;
          gap: calc(25 * var(--u));
          pointer-events: auto;
          animation: riseNav 0.8s cubic-bezier(.22, 1, .36, 1) both;
        }

        .links a {
          font-size: calc(19.0 * var(--u));
          font-weight: 400;
          color: var(--nav);
          transition: color 0.2s ease;
          white-space: nowrap;
          letter-spacing: -0.01em;
        }

        .links a:hover {
          color: var(--ink);
        }

        .pill {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          background: var(--pill);
          color: var(--pill-ink);
          border-radius: 999px;
          font-family: inherit;
          font-weight: 500;
          text-decoration: none;
          cursor: pointer;
          pointer-events: auto;
          transition: opacity 0.2s ease, transform 0.2s ease;
        }

        .pill:hover {
          opacity: 0.92;
          transform: scale(1.015);
        }

        .pill:active {
          transform: scale(0.985);
        }

        .pill-nav {
          position: absolute;
          right: calc(75.4 * var(--u));
          top: calc(27 * var(--u));
          width: calc(175 * var(--u));
          height: calc(49 * var(--u));
          font-size: calc(20.6 * var(--u));
          animation: rise 0.8s cubic-bezier(.22, 1, .36, 1) both;
        }

        .pill-nav span, .pill-cta span {
          transform: translateY(calc(1 * var(--u)));
          display: inline-block;
        }

        .burger {
          display: none;
        }

        .hero {
          position: absolute;
          inset: 0;
          z-index: 5;
          pointer-events: none;
        }

        .headline {
          position: absolute;
          left: calc(75.5 * var(--u));
          top: calc(230.5 * var(--u));
          font-size: calc(71.6 * var(--h));
          line-height: calc(80.5 * var(--h));
          font-weight: 400;
          letter-spacing: calc(0.3 * var(--h));
          color: var(--ink);
          white-space: nowrap;
          margin: 0;
          pointer-events: auto;
          animation: rise 0.9s cubic-bezier(.22, 1, .36, 1) 0.06s both;
        }

        .headline span {
          display: block;
        }

        .sub {
          position: absolute;
          left: calc(75.5 * var(--u));
          top: calc(230.5 * var(--u) + 189.0 * var(--h));
          font-size: calc(20.7 * var(--h));
          line-height: calc(23.5 * var(--h));
          font-weight: 400;
          word-spacing: calc(1.8 * var(--h));
          color: var(--muted);
          margin: 0;
          pointer-events: auto;
          animation: rise 0.9s cubic-bezier(.22, 1, .36, 1) 0.14s both;
        }

        .sub span {
          display: block;
          white-space: nowrap;
        }

        .actions {
          position: absolute;
          left: calc(74.9 * var(--u));
          top: calc(230.5 * var(--u) + 264.5 * var(--h));
          display: flex;
          align-items: center;
          gap: calc(45 * var(--h));
          pointer-events: auto;
          animation: rise 0.9s cubic-bezier(.22, 1, .36, 1) 0.22s both;
        }

        .pill-cta {
          width: calc(175.6 * var(--h));
          height: calc(50 * var(--h));
          font-size: calc(20.6 * var(--h));
        }

        .ghost {
          font-size: calc(20.6 * var(--h));
          font-weight: 500;
          letter-spacing: calc(0.12 * var(--h));
          color: #ffffff;
          white-space: nowrap;
          transition: opacity 0.2s ease;
          cursor: pointer;
        }

        .ghost:hover {
          opacity: 0.8;
        }

        .logos {
          position: absolute;
          width: calc(741 * var(--u));
          left: 50%;
          top: 0;
          height: calc(1058 * var(--u));
          transform: translateX(calc(-50% + 20 * var(--u)));
          color: var(--strip);
          pointer-events: none;
          z-index: 6;
        }

        .lg {
          position: absolute;
          display: flex;
          align-items: center;
          pointer-events: auto;
          opacity: 0.85;
          transition: opacity 0.2s ease;
          animation: fade 1.1s cubic-bezier(.22, 1, .36, 1) 0.34s both;
        }

        .lg:hover {
          opacity: 1;
        }

        .lg-word {
          font-family: 'IpsumMark', 'Manrope', sans-serif;
          font-weight: 700;
          color: currentColor;
          letter-spacing: -0.02em;
          line-height: 1;
        }

        .lg1 {
          left: calc(-0.5 * var(--u));
          top: calc(994.7 * var(--u));
        }
        .lg1 svg {
          width: calc(30.5 * var(--u));
          height: calc(31 * var(--u));
          margin-right: calc(6.5 * var(--u));
        }
        .lg1 .lg-word {
          font-size: calc(18.1 * var(--u));
          transform: translateY(calc(1.5 * var(--u)));
        }

        .lg2 {
          left: calc(206.5 * var(--u));
          top: calc(995.7 * var(--u));
        }
        .lg2 svg {
          width: calc(24.5 * var(--u));
          height: calc(30 * var(--u));
          margin-right: calc(6.5 * var(--u));
        }
        .lg2 .lg-word {
          font-size: calc(18.5 * var(--u));
          transform: translateY(calc(1.5 * var(--u)));
        }
        .lg2 .dot {
          display: inline-block;
          width: 0.22em;
          height: 0.22em;
          background-color: currentColor;
          border-radius: 50%;
          vertical-align: 0.62em;
          margin-left: 0.08em;
        }

        .lg3 {
          left: calc(416.5 * var(--u));
          top: calc(996.7 * var(--u));
        }
        .lg3 svg {
          width: calc(28.5 * var(--u));
          height: calc(28 * var(--u));
          margin-right: calc(6.5 * var(--u));
        }
        .lg3 .lg-word {
          font-size: calc(16.15 * var(--u));
          transform: translateY(calc(1.5 * var(--u)));
        }

        .lg4 {
          left: calc(620.5 * var(--u));
          top: calc(998.7 * var(--u));
        }
        .lg4 svg {
          width: calc(28.5 * var(--u));
          height: calc(25.5 * var(--u));
          margin-right: calc(8.5 * var(--u));
        }
        .lg4 .lg-word {
          font-size: calc(15.3 * var(--u));
          transform: translateY(calc(1.5 * var(--u)));
        }

        @keyframes rise {
          from {
            opacity: 0;
            transform: translateY(calc(14 * var(--u)));
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes riseNav {
          from {
            opacity: 0;
            transform: translate(-50%, calc(-50% + calc(14 * var(--u))));
          }
          to {
            opacity: 1;
            transform: translate(-50%, -50%);
          }
        }

        @keyframes fade {
          from { opacity: 0; }
          to { opacity: 0.85; }
        }

        @media (max-aspect-ratio: 11/10) {
          .stage {
            height: auto;
            min-height: 100vh;
            min-height: 100dvh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: calc(24 * var(--m)) calc(20 * var(--m)) calc(32 * var(--m));
          }

          .plate {
            position: fixed;
            inset: 0;
          }

          .plate-video {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            transform: none;
            object-fit: cover;
            object-position: 43% center;
          }

          .plate::after {
            background-image:
              linear-gradient(to right,
                rgba(5,5,5,.86),
                rgba(5,5,5,.66) 42%,
                rgba(5,5,5,.20) 78%,
                rgba(5,5,5,.10) 100%
              ),
              linear-gradient(to bottom,
                rgba(5,5,5,.72) 0%,
                rgba(5,5,5,.34) 24%,
                rgba(5,5,5,.34) 56%,
                rgba(5,5,5,.80) 82%,
                rgba(5,5,5,.97) 94%,
                #050505 100%
              );
          }

          .topbar {
            position: relative;
            height: auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            pointer-events: auto;
          }

          .brand {
            position: static;
            width: calc(26 * var(--m));
            height: calc(40 * var(--m));
          }

          .links, .pill-nav {
            display: none;
          }

          .burger {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: calc(52 * var(--m));
            height: calc(36 * var(--m));
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.14);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            pointer-events: auto;
            z-index: 100;
            gap: calc(5 * var(--m));
          }

          .burger i {
            display: block;
            width: calc(20 * var(--m));
            height: 1.5px;
            background: var(--ink);
            transition: transform 0.3s cubic-bezier(.22, 1, .36, 1), opacity 0.2s ease;
          }

          .stage.is-open .burger i:nth-child(1) {
            transform: translateY(calc(3.25 * var(--m))) rotate(45deg);
          }
          .stage.is-open .burger i:nth-child(2) {
            transform: translateY(calc(-3.25 * var(--m))) rotate(-45deg);
          }

          .hero {
            position: relative;
            inset: auto;
            margin-top: calc(80 * var(--m));
            margin-bottom: calc(60 * var(--m));
            display: flex;
            flex-direction: column;
            pointer-events: auto;
          }

          .headline {
            position: static;
            font-size: calc(38 * var(--m));
            line-height: calc(44 * var(--m));
            letter-spacing: -0.01em;
            white-space: normal;
          }

          .headline span {
            display: inline;
          }

          .sub {
            position: static;
            margin-top: calc(20 * var(--m));
            font-size: calc(15 * var(--m));
            line-height: calc(22 * var(--m));
            word-spacing: normal;
          }

          .sub span {
            display: inline;
            white-space: normal;
          }

          .actions {
            position: static;
            margin-top: calc(28 * var(--m));
            flex-direction: column;
            align-items: flex-start;
            gap: calc(16 * var(--m));
          }

          .pill-cta {
            width: 100%;
            max-width: calc(280 * var(--m));
            height: calc(46 * var(--m));
            font-size: calc(16 * var(--m));
          }

          .ghost {
            font-size: calc(16 * var(--m));
            padding-left: calc(4 * var(--m));
          }

          .logos {
            position: relative;
            width: 100%;
            height: auto;
            left: auto;
            top: auto;
            transform: none;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: calc(20 * var(--m)) calc(24 * var(--m));
            pointer-events: auto;
            padding-top: calc(20 * var(--m));
          }

          .lg {
            position: static;
          }

          .lg1 svg, .lg2 svg, .lg3 svg, .lg4 svg {
            width: calc(22 * var(--m));
            height: calc(22 * var(--m));
            margin-right: calc(6 * var(--m));
          }

          .lg1 .lg-word, .lg2 .lg-word, .lg3 .lg-word, .lg4 .lg-word {
            font-size: calc(14 * var(--m));
            transform: none;
          }

          .menu {
            position: fixed;
            inset: 0;
            background: rgba(5, 5, 5, 0.96);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            z-index: 90;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.42s cubic-bezier(.22, 1, .36, 1), visibility 0.42s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: calc(90 * var(--m)) calc(24 * var(--m)) calc(40 * var(--m));
          }

          .stage.is-open .menu {
            opacity: 1;
            visibility: visible;
          }

          .menu-eyebrow {
            font-size: calc(12 * var(--m));
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--muted);
            margin-bottom: calc(24 * var(--m));
          }

          .menu-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: calc(18 * var(--m));
          }

          .menu-list a {
            font-size: calc(28 * var(--m));
            font-weight: 400;
            color: var(--ink);
            display: flex;
            align-items: center;
            justify-content: space-between;
          }

          .menu-list a::after {
            content: '→';
            font-size: 0.75em;
            color: var(--muted);
          }

          .menu-foot {
            display: flex;
            flex-direction: column;
            gap: calc(14 * var(--m));
            margin-top: calc(32 * var(--m));
          }

          .menu-foot .pill {
            width: 100%;
            height: calc(48 * var(--m));
            font-size: calc(16 * var(--m));
          }

          .menu-foot .ghost {
            text-align: center;
            padding: calc(8 * var(--m)) 0;
          }
        }

        @media (min-width: 600px) and (max-aspect-ratio: 11/10) {
          .plate-video {
            object-position: 44% center;
          }

          .plate::after {
            background-image:
              linear-gradient(to right,
                rgba(5,5,5,.84),
                rgba(5,5,5,.60) 42%,
                rgba(5,5,5,.16) 78%,
                rgba(5,5,5,.06) 100%
              ),
              linear-gradient(to bottom,
                rgba(5,5,5,.66) 0%,
                rgba(5,5,5,.28) 24%,
                rgba(5,5,5,.30) 56%,
                rgba(5,5,5,.78) 82%,
                rgba(5,5,5,.96) 94%,
                #050505 100%
              );
          }

          .headline {
            font-size: calc(46 * var(--m));
            line-height: calc(54 * var(--m));
          }

          .headline span {
            display: block;
          }

          .sub span {
            display: block;
          }

          .actions {
            flex-direction: row;
            align-items: center;
          }

          .logos {
            grid-template-columns: repeat(4, 1fr);
          }
        }
      `,
        }}
      />

      <div className={`stage ${isOpen ? 'is-open' : ''}`}>
        {/* BACKGROUND CLOUDFRONT VIDEO */}
        <div className="plate">
          <video
            className="plate-video"
            autoPlay
            muted
            loop
            playsInline
            preload="auto"
            aria-hidden="true"
          >
            <source
              src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260808_112712_da9d53df-6d27-4b12-bdf6-aa9dc2622bdf.mp4"
              type="video/mp4"
            />
          </video>
        </div>

        {/* TOPBAR */}
        <header className="topbar">
          {/* BRAND S-BOLT SVG */}
          <Link href="/" className="brand" aria-label="Home">
            <svg viewBox="0 0 31.5 48.5" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="bg1" x1="8" y1="0" x2="34.1" y2="28.9" gradientUnits="userSpaceOnUse">
                  <stop offset="0" stopColor="#9e9e9e" />
                  <stop offset="0.28" stopColor="#a6a6a6" />
                  <stop offset="0.34" stopColor="#a3a3a3" />
                  <stop offset="0.40" stopColor="#3a3a3a" />
                  <stop offset="0.55" stopColor="#414141" />
                  <stop offset="0.60" stopColor="#7a7a7a" />
                  <stop offset="0.68" stopColor="#8e8e8e" />
                  <stop offset="0.80" stopColor="#a9a9a9" />
                  <stop offset="0.95" stopColor="#c4c4c4" />
                  <stop offset="1" stopColor="#cccccc" />
                </linearGradient>
              </defs>
              <path
                d="M21.5 0 L21.5 19.5 L31.5 19.5 L31.5 29 L10 48.5 L10 28.5 L0.5 28.5 L0.5 18.5 Z"
                fill="url(#bg1)"
              />
              <rect x="0.5" y="18.5" width="9" height="10" fill="#fdfdfd" />
              <rect x="22" y="19.5" width="9.5" height="9.5" fill="#fdfdfd" />
            </svg>
          </Link>

          {/* PRIMARY NAV LINKS */}
          <nav className="links" aria-label="Primary">
            <a href="#about">About</a>
            <a href="#features">Features</a>
            <a href="#faq">FAQ</a>
            <a href="#contact">Contact</a>
          </nav>

          {/* HEADER CTA PILL */}
          <Link href="/login" className="pill pill-nav">
            <span>Get Started</span>
          </Link>

          {/* MOBILE BURGER BUTTON */}
          <button
            className="burger"
            onClick={() => setIsOpen(!isOpen)}
            aria-label={isOpen ? 'Close Menu' : 'Open Menu'}
            aria-expanded={isOpen}
            aria-controls="menu"
          >
            <i />
            <i />
          </button>
        </header>

        {/* MOBILE MENU OVERLAY */}
        <nav className="menu" id="menu" aria-hidden={!isOpen}>
          <div className="menu-inner">
            <p className="menu-eyebrow">Menu</p>
            <ul className="menu-list">
              <li>
                <a href="#about" onClick={() => setIsOpen(false)}>About</a>
              </li>
              <li>
                <a href="#features" onClick={() => setIsOpen(false)}>Features</a>
              </li>
              <li>
                <a href="#faq" onClick={() => setIsOpen(false)}>FAQ</a>
              </li>
              <li>
                <a href="#contact" onClick={() => setIsOpen(false)}>Contact</a>
              </li>
            </ul>
          </div>
          <div className="menu-foot">
            <Link href="/login" className="pill" onClick={() => setIsOpen(false)}>
              <span>Get Started</span>
            </Link>
            <a href="#architecture" className="ghost" onClick={() => setIsOpen(false)}>
              View Architecture
            </a>
          </div>
        </nav>

        {/* HERO CONTENT */}
        <main className="hero">
          <h1 className="headline">
            <span>The Next Layer</span>
            <span>of Intelligence</span>
          </h1>
          <p className="sub">
            <span>A unified infrastructure platform to help teams build,</span>
            <span>ship, and scale AI systems with confidence.</span>
          </p>
          <div className="actions">
            <Link href="/login" className="pill pill-cta">
              <span>Get Started</span>
            </Link>
            <a href="#architecture" className="ghost">
              View Architecture
            </a>
          </div>
        </main>

        {/* PARTNER LOGOS STRIP */}
        <div className="logos">
          {/* LG 1 */}
          <div className="lg lg1">
            <svg viewBox="0 0 30 31" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M0 0H30V31H0V0ZM19.5 15.6C22.3167 15.6 24.6 13.3167 24.6 10.5C24.6 7.68335 22.3167 5.4 19.5 5.4C16.6833 5.4 14.4 7.68335 14.4 10.5C14.4 13.3167 16.6833 15.6 19.5 15.6Z"
                fill="currentColor"
              />
            </svg>
            <span className="lg-word">logoipsum</span>
          </div>

          {/* LG 2 */}
          <div className="lg lg2">
            <svg viewBox="0 0 25 30" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M0 0H7.5V30H0V0Z" fill="currentColor" />
              <path
                d="M12.5 0C19.4036 0 25 5.59644 25 12.5C25 19.4036 19.4036 25 12.5 25V18.75C15.9518 18.75 18.75 15.9518 18.75 12.5C18.75 9.04822 15.9518 6.25 12.5 6.25V0Z"
                fill="currentColor"
              />
            </svg>
            <span className="lg-word">
              logoipsum<span className="dot" />
            </span>
          </div>

          {/* LG 3 */}
          <div className="lg lg3">
            <svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="14" cy="14" r="12.35" stroke="currentColor" strokeWidth="3.1" />
              <path
                d="M14 4.8C8.91898 4.8 4.8 8.91898 4.8 14C4.8 17.5 7.2 20.5 10.5 21.8"
                stroke="currentColor"
                strokeWidth="3.1"
                strokeLinecap="round"
              />
              <path
                d="M14 23.2C19.081 23.2 23.2 19.081 23.2 14C23.2 10.5 20.8 7.5 17.5 6.2"
                stroke="currentColor"
                strokeWidth="3.1"
                strokeLinecap="round"
              />
            </svg>
            <span className="lg-word">logoipsum</span>
          </div>

          {/* LG 4 */}
          <div className="lg lg4">
            <svg viewBox="0 0 28 25.5" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M0 8.5C4.66667 3 9.33333 0 14 0C18.6667 0 23.3333 3 28 8.5H0Z" fill="currentColor" />
              <path
                d="M0 16.5C4.66667 13.5 9.33333 13.5 14 16.5C18.6667 19.5 23.3333 19.5 28 16.5"
                stroke="currentColor"
                strokeWidth="3.05"
                strokeLinecap="round"
              />
              <path
                d="M0 23.5C4.66667 20.5 9.33333 20.5 14 23.5C18.6667 26.5 23.3333 26.5 28 23.5"
                stroke="currentColor"
                strokeWidth="3.05"
                strokeLinecap="round"
              />
            </svg>
            <span className="lg-word">logoipsum</span>
          </div>
        </div>
      </div>
    </>
  );
}
