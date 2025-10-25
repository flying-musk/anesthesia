# Migration Guide: Old Frontend → New Frontend

This guide explains the differences between the old React frontend and the new Next.js frontend.

## Directory Structure Comparison

### Old Frontend (`frontend/`)
```
frontend/
└── src/
    ├── App.js                    # Main app with routes
    ├── components/Layout/        # Layout component
    ├── pages/                    # Page components
    ├── services/api.js           # API service
    └── i18n/                     # i18next setup
```

### New Frontend (`frontend-next/`)
```
frontend-next/
└── src/
    ├── app/                      # Next.js App Router pages
    │   ├── page.tsx             # Dashboard (was Dashboard.js)
    │   ├── layout.tsx           # Root layout
    │   ├── patients/            # Patient routes
    │   └── guidelines/          # Guideline routes
    ├── components/
    │   ├── ui/                  # shadcn/ui components
    │   └── layout/              # Layout components
    ├── lib/
    │   ├── api/                 # API services
    │   ├── hooks/               # React Query hooks
    │   └── validators/          # Zod schemas
    └── types/                   # TypeScript types
```

## Technology Differences

| Feature | Old Frontend | New Frontend |
|---------|-------------|--------------|
| **Framework** | Create React App | Next.js 14 |
| **Language** | JavaScript | TypeScript |
| **Routing** | React Router 6 | Next.js App Router |
| **UI Library** | Material-UI (MUI) | shadcn/ui |
| **Styling** | Emotion/MUI | Tailwind CSS |
| **Forms** | React Hook Form + Yup | React Hook Form + Zod |
| **Data Fetching** | React Query 3 | React Query 5 |
| **HTTP Client** | Axios | Axios |
| **i18n** | i18next | next-intl (ready) |

## Page-by-Page Comparison

### Dashboard
**Old**: `frontend/src/pages/Dashboard.js`
**New**: `frontend-next/src/app/page.tsx`

**Changes**:
- MUI Grid → Tailwind grid classes
- MUI Card → shadcn/ui Card
- MUI Typography → HTML with Tailwind classes
- Class components → Functional components with hooks

### Patient List
**Old**: `frontend/src/pages/PatientManagement.js`
**New**: `frontend-next/src/app/patients/page.tsx`

**Changes**:
- MUI Table → shadcn/ui Table
- MUI TextField → shadcn/ui Input
- MUI Button → shadcn/ui Button
- Emotion CSS → Tailwind classes

### Create Patient
**Old**: `frontend/src/pages/CreatePatient.js`
**New**: `frontend-next/src/app/patients/create/page.tsx`

**Changes**:
- Yup validation → Zod validation
- MUI form components → shadcn/ui form components
- MUI MenuItem → shadcn/ui Select
- Form state management remains similar

### Patient Details
**Old**: `frontend/src/pages/PatientDetails.js`
**New**: `frontend-next/src/app/patients/[id]/page.tsx`

**Changes**:
- URL params: `useParams()` → `params` prop
- MUI Tabs → shadcn/ui Tabs
- MUI Chip → shadcn/ui Badge
- Dynamic routing: `/patients/:id` → `/patients/[id]`

### Generate Guideline
**Old**: `frontend/src/pages/GenerateGuideline.js`
**New**: `frontend-next/src/app/guidelines/generate/page.tsx`

**Changes**:
- MUI Stepper → Custom step indicator
- Multi-step logic improved
- Better type safety with TypeScript
- Enhanced UX with better loading states

## API Service Comparison

### Old API Service
```javascript
// frontend/src/services/api.js
export const patientsAPI = {
  getAll: () => axios.get('/patients/'),
  getById: (id) => axios.get(`/patients/${id}`),
  // ...
};
```

### New API Service
```typescript
// frontend-next/src/lib/api/patients.ts
export const patientsApi = {
  getAll: async (page = 1, size = 100) => {
    const { data } = await apiClient.get<PaginatedResponse<Patient>>('/patients/', {
      params: { page, size },
    });
    return data;
  },
  // ...
};
```

**Improvements**:
- TypeScript for type safety
- Better error handling
- Consistent return types
- Separated into multiple files

## Data Fetching Comparison

### Old (React Query 3)
```javascript
const { data, isLoading } = useQuery('patients', patientsAPI.getAll);
```

### New (React Query 5)
```typescript
const { data, isLoading } = usePatients();

// Hook definition:
export const usePatients = (page = 1, size = 100) => {
  return useQuery({
    queryKey: QUERY_KEYS.patients.list(page),
    queryFn: () => patientsApi.getAll(page, size),
  });
};
```

**Improvements**:
- Custom hooks for each data operation
- Centralized query keys
- Better TypeScript support
- Automatic type inference

## Form Validation Comparison

### Old (Yup)
```javascript
const patientSchema = yup.object({
  full_name: yup.string().required('Full name is required'),
  gender: yup.string().oneOf(['M', 'F', 'O']).required(),
  // ...
});
```

### New (Zod)
```typescript
export const patientSchema = z.object({
  full_name: z.string().min(1, 'Full name is required'),
  gender: z.enum(['M', 'F', 'O'], { message: 'Please select a gender' }),
  // ...
});

export type PatientFormData = z.infer<typeof patientSchema>;
```

**Improvements**:
- Better TypeScript integration
- Type inference from schema
- Runtime and compile-time type safety

## Styling Comparison

### Old (MUI + Emotion)
```javascript
<Box sx={{ display: 'flex', gap: 2 }}>
  <Card>
    <CardContent>
      <Typography variant="h6">Title</Typography>
    </CardContent>
  </Card>
</Box>
```

### New (Tailwind + shadcn/ui)
```typescript
<div className="flex gap-2">
  <Card>
    <CardContent>
      <h3 className="text-lg font-semibold">Title</h3>
    </CardContent>
  </Card>
</div>
```

**Benefits**:
- Smaller bundle size
- Faster development with utility classes
- Better performance (no runtime CSS-in-JS)
- Easier to customize

## Key Improvements

### 1. Type Safety
- **Old**: JavaScript with PropTypes (optional)
- **New**: Full TypeScript with strict mode
- **Benefit**: Catch errors at compile time

### 2. Performance
- **Old**: Client-side rendering only
- **New**: Server-side rendering + client components
- **Benefit**: Faster initial page loads, better SEO

### 3. Code Organization
- **Old**: Flat page structure
- **New**: Nested route-based structure
- **Benefit**: Better code organization, co-location

### 4. Developer Experience
- **Old**: React Router configuration
- **New**: File-based routing
- **Benefit**: Less boilerplate, clearer structure

### 5. Bundle Size
- **Old**: ~500KB (MUI + Emotion)
- **New**: ~200KB (shadcn/ui + Tailwind)
- **Benefit**: Faster load times

### 6. Accessibility
- **Old**: MUI built-in accessibility
- **New**: shadcn/ui built-in accessibility
- **Benefit**: Both have good a11y, maintained

## Breaking Changes

### Routing
- Change from React Router to Next.js App Router
- Update all `<Link to="...">` to `<Link href="...">`
- Update navigation logic

### Components
- Replace all MUI components with shadcn/ui equivalents
- Update styling from sx prop to className with Tailwind

### State Management
- React Query API updated from v3 to v5
- Update query syntax

### Forms
- Change from Yup to Zod schemas
- Update validation error handling

## What Stayed the Same

✅ **Backend API**: No changes needed
✅ **React Hook Form**: Same library, updated usage
✅ **Axios**: Same HTTP client
✅ **React Query**: Same library, newer version
✅ **Core Features**: All features maintained
✅ **Data Flow**: Similar patterns

## Migration Checklist

If you want to migrate features from old to new:

- [ ] Identify the old component
- [ ] Find corresponding new page in `frontend-next/src/app/`
- [ ] Replace MUI imports with shadcn/ui imports
- [ ] Convert JavaScript to TypeScript
- [ ] Update routing from React Router to Next.js
- [ ] Replace Yup schemas with Zod schemas
- [ ] Update React Query hooks to v5 syntax
- [ ] Test functionality
- [ ] Update tests (if any)

## Running Both Frontends

You can run both frontends simultaneously for comparison:

**Old Frontend**:
```bash
cd frontend
npm start
# Runs on http://localhost:3001 (or configured port)
```

**New Frontend**:
```bash
cd frontend-next
npm run dev
# Runs on http://localhost:3000
```

Both connect to the same backend at `http://localhost:8000`.

## Recommendations

### For Development
✅ Use the new frontend (`frontend-next/`)
- Modern tech stack
- Better developer experience
- Active maintenance

### For Production
✅ Use the new frontend (`frontend-next/`)
- Better performance
- Smaller bundle size
- SEO-friendly

### Removing Old Frontend
Once you're comfortable with the new frontend, you can:
```bash
# Optional: Back up old frontend
mv frontend frontend-old-backup

# Or remove it completely
rm -rf frontend
```

## Support & Resources

- **Next.js Docs**: https://nextjs.org/docs
- **shadcn/ui Docs**: https://ui.shadcn.com
- **Tailwind Docs**: https://tailwindcss.com/docs
- **React Query v5**: https://tanstack.com/query/latest
- **Zod Docs**: https://zod.dev

## Conclusion

The new Next.js frontend provides:
- Modern development experience
- Better performance
- Type safety with TypeScript
- Smaller bundle size
- Cleaner code organization

All original features are preserved and enhanced with better UX and developer experience!
