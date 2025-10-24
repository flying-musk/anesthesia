# Anesthesia Management System - Frontend

A modern, AI-powered anesthesia management system built with Next.js 14, shadcn/ui, and Tailwind CSS.

## Features

- **Patient Management**: Create, view, and manage patient records with comprehensive medical history
- **AI-Powered Guidelines**: Generate anesthesia guidelines using OpenAI GPT-4 or local LLM (Ollama)
- **Multi-Step Forms**: Intuitive multi-step form for guideline generation
- **Real-time Data**: Powered by React Query for efficient data fetching and caching
- **Beautiful UI**: Modern, responsive design with shadcn/ui components and Tailwind CSS
- **Type Safety**: Full TypeScript support throughout the application
- **Form Validation**: Robust form validation with Zod schemas

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **UI Components**: shadcn/ui
- **Styling**: Tailwind CSS
- **Data Fetching**: TanStack React Query (v5)
- **Form Handling**: React Hook Form
- **Validation**: Zod
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Date Handling**: date-fns

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running (see backend README)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Update `.env.local` with your configuration:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend-next/
├── src/
│   ├── app/                      # Next.js App Router pages
│   │   ├── page.tsx             # Dashboard
│   │   ├── layout.tsx           # Root layout
│   │   ├── patients/            # Patient pages
│   │   │   ├── page.tsx         # Patient list
│   │   │   ├── create/          # Create patient
│   │   │   └── [id]/            # Patient details
│   │   └── guidelines/          # Guideline pages
│   │       ├── page.tsx         # Guidelines list
│   │       ├── generate/        # Generate guideline
│   │       └── [id]/            # Guideline details
│   ├── components/              # React components
│   │   ├── ui/                  # shadcn/ui components
│   │   ├── layout/              # Layout components
│   │   └── providers.tsx        # React Query provider
│   ├── lib/                     # Library code
│   │   ├── api/                 # API client and services
│   │   ├── hooks/               # Custom React hooks
│   │   ├── validators/          # Zod schemas
│   │   └── utils.ts             # Utility functions
│   ├── types/                   # TypeScript types
│   ├── config/                  # Configuration
│   └── i18n/                    # Internationalization
├── public/                      # Static files
└── package.json                 # Dependencies
```

## Key Features

### Dashboard
- Overview of total patients and guidelines
- Quick access cards for common actions
- Recent patients and guidelines lists

### Patient Management
- Complete CRUD operations for patients
- Search and filter functionality
- Detailed patient profiles with medical history, surgery records, and guidelines

### Guideline Generation
- Multi-step wizard interface
- AI-powered generation via FastAPI backend
- Supports both OpenAI and local LLM (Ollama)

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000/api/v1`.

## Customization

### Adding New Components

Use shadcn/ui CLI:

```bash
npx shadcn@latest add [component-name]
```

### Styling

Tailwind CSS is configured. Modify `tailwind.config.ts` for theme customization.

## Troubleshooting

- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend config
- Verify `.env.local` has correct API URL

## License

MIT
