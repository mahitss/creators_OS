'use client';

import React from 'react';

export function PlateVideo() {
  return (
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
  );
}
