import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Silence workspace root warning by pinning the root to this app
  experimental: {
    turbo: {
      root: __dirname,
    },
  },
};

export default nextConfig;
