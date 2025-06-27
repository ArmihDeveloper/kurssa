/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // You might want to configure a proxy to your backend API later
  // async rewrites() {
  //   return [
  //     {
  //       source: '/api/:path*',
  //       destination: 'http://localhost:5000/api/:path*', // Adjust if your backend runs elsewhere
  //     },
  //   ]
  // },
};

module.exports = nextConfig;
