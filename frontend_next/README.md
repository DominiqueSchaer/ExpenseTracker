This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Environment variables

Create a `.env.local` file in `frontend/` with:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:4000
```

If you see a warning about the workspace root when running dev, it's safe to ignore; we've pinned Turbopack root in `next.config.ts`.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## Deploying to Vercel

1. Push your code to a GitHub/GitLab/Bitbucket repository.
2. Go to [Vercel](https://vercel.com/import) and import your frontend project.
3. In Vercel dashboard, set the environment variable `NEXT_PUBLIC_API_BASE_URL` to your backend's public URL.
4. Deploy!

For more details, see [Vercel Next.js documentation](https://vercel.com/docs/frameworks/nextjs).

## How to Push to Vercel

1. Commit and push your code to a GitHub, GitLab, or Bitbucket repository.
2. Go to [https://vercel.com/import](https://vercel.com/import) and import your repository.
3. During setup, set the environment variable `NEXT_PUBLIC_API_BASE_URL` to your backend's public URL.
4. Click "Deploy". Vercel will build and host your app automatically.
5. After deployment, your app will be available at the provided Vercel URL.

## How to Push to Git

1. Initialize a git repository if you haven't already:
   ```bash
   git init
   ```
2. Add all files:
   ```bash
   git add .
   ```
3. Commit your changes:
   ```bash
   git commit -m "Initial commit"
   ```
4. Create a new repository on GitHub, GitLab, or Bitbucket.
5. Add the remote (replace `<REMOTE_URL>` with your repo URL):
   ```bash
   git remote add origin <REMOTE_URL>
   ```
6. Push your code:
   ```bash
   git push -u origin main
   ```
