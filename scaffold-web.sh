#!/bin/bash

# Create Next.js app with specified configuration
npx create-next-app@14 web --typescript --eslint --tailwind --src-dir --import-alias "@/*"

# Change directory to web and start development server
cd web
npm run dev 