'use client';

import React from 'react';
import styles from './landing.module.css';

export function PartnerLogos() {
  return (
    <div className={styles.logos}>
      {/* LG 1 */}
      <div className={`${styles.lg} ${styles.lg1}`}>
        <svg viewBox="0 0 30 31" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M0 0H30V31H0V0ZM19.5 15.6C22.3167 15.6 24.6 13.3167 24.6 10.5C24.6 7.68335 22.3167 5.4 19.5 5.4C16.6833 5.4 14.4 7.68335 14.4 10.5C14.4 13.3167 16.6833 15.6 19.5 15.6Z"
            fill="currentColor"
          />
        </svg>
        <span className={styles.lgWord}>logoipsum</span>
      </div>

      {/* LG 2 */}
      <div className={`${styles.lg} ${styles.lg2}`}>
        <svg viewBox="0 0 25 30" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M0 0H7.5V30H0V0Z" fill="currentColor" />
          <path
            d="M12.5 0C19.4036 0 25 5.59644 25 12.5C25 19.4036 19.4036 25 12.5 25V18.75C15.9518 18.75 18.75 15.9518 18.75 12.5C18.75 9.04822 15.9518 6.25 12.5 6.25V0Z"
            fill="currentColor"
          />
        </svg>
        <span className={styles.lgWord}>
          logoipsum<span className={styles.dot} />
        </span>
      </div>

      {/* LG 3 */}
      <div className={`${styles.lg} ${styles.lg3}`}>
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
        <span className={styles.lgWord}>logoipsum</span>
      </div>

      {/* LG 4 */}
      <div className={`${styles.lg} ${styles.lg4}`}>
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
        <span className={styles.lgWord}>logoipsum</span>
      </div>
    </div>
  );
}
