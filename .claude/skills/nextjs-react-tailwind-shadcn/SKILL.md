---
name: nextjs-react-tailwind-shadcn
description: Next.js App Router with React Server Components, Tailwind CSS, shadcn/ui, and TypeScript. Use when building frontend pages, layouts, client/server components, data fetching, or adding shadcn/ui components.
---

# Next.js React Tailwind shadcn/ui

Production Next.js App Router patterns with Server/Client Components, Tailwind CSS, shadcn/ui, and TypeScript.

## When to Apply

- Building pages with Next.js App Router
- Choosing between Server and Client Components
- Adding shadcn/ui components to a project
- Implementing data fetching, loading, and error states
- Setting up layouts, middleware, and API routes

## Critical Rules

**Server Components by default**: Only add `'use client'` when you need browser APIs, state, or effects

```tsx
// WRONG - unnecessary 'use client' on a data display component
'use client'
export default function UserProfile({ user }) {
  return <div>{user.name}</div>
}

// RIGHT - Server Component fetches and renders data
export default async function UserProfile({ userId }: { userId: string }) {
  const user = await getUser(userId)
  return <div>{user.name}</div>
}
```

**Compose Server + Client**: Push `'use client'` to the leaves of the component tree

```tsx
// page.tsx - Server Component (fetches data)
import { InteractiveForm } from './interactive-form'

export default async function Page() {
  const data = await getData()
  return (
    <div>
      <h1>{data.title}</h1>
      <InteractiveForm initialData={data} />  {/* Client at the leaf */}
    </div>
  )
}

// interactive-form.tsx - Client Component (needs state)
'use client'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export function InteractiveForm({ initialData }: { initialData: Data }) {
  const [value, setValue] = useState(initialData.defaultValue)
  return (
    <form>
      <Input value={value} onChange={(e) => setValue(e.target.value)} />
      <Button type="submit">Save</Button>
    </form>
  )
}
```

## Key Patterns

### Root Layout with Tailwind

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { cn } from '@/lib/utils'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

export const metadata: Metadata = {
  title: 'My App',
  description: 'Built with Next.js and shadcn/ui',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn('min-h-screen bg-background font-sans antialiased', inter.variable)}>
        {children}
      </body>
    </html>
  )
}
```

### Loading and Error Boundaries

```tsx
// app/dashboard/loading.tsx
import { Skeleton } from '@/components/ui/skeleton'

export default function Loading() {
  return (
    <div className="space-y-4 p-6">
      <Skeleton className="h-8 w-[250px]" />
      <Skeleton className="h-[200px] w-full" />
    </div>
  )
}

// app/dashboard/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 p-6">
      <h2 className="text-lg font-semibold">Something went wrong</h2>
      <button onClick={() => reset()} className="rounded bg-primary px-4 py-2 text-white">
        Try again
      </button>
    </div>
  )
}
```

### Server Actions for Mutations

```tsx
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'

export async function createItem(formData: FormData) {
  const title = formData.get('title') as string

  const response = await fetch(`${process.env.API_URL}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  })

  if (!response.ok) throw new Error('Failed to create item')
  revalidatePath('/dashboard')
}
```

### shadcn/ui Data Table

```tsx
// columns.tsx
'use client'

import { ColumnDef } from '@tanstack/react-table'
import { Badge } from '@/components/ui/badge'

export type Payment = {
  id: string
  amount: number
  status: 'pending' | 'processing' | 'success' | 'failed'
  email: string
}

export const columns: ColumnDef<Payment>[] = [
  { accessorKey: 'email', header: 'Email' },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ row }) => (
      <Badge variant={row.getValue('status') === 'success' ? 'default' : 'secondary'}>
        {row.getValue('status')}
      </Badge>
    ),
  },
  {
    accessorKey: 'amount',
    header: () => <div className="text-right">Amount</div>,
    cell: ({ row }) => {
      const amount = parseFloat(row.getValue('amount'))
      const formatted = new Intl.NumberFormat('en-US', {
        style: 'currency', currency: 'USD',
      }).format(amount / 100)
      return <div className="text-right font-medium">{formatted}</div>
    },
  },
]

// page.tsx - Server Component renders the table
import { columns } from './columns'
import { DataTable } from './data-table'

export default async function PaymentsPage() {
  const data = await getPayments()
  return (
    <div className="container mx-auto py-10">
      <DataTable columns={columns} data={data} />
    </div>
  )
}
```

### API Route Handlers

```tsx
// app/api/items/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const page = parseInt(searchParams.get('page') ?? '1')

  const items = await getItems({ page, limit: 20 })
  return NextResponse.json(items)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const item = await createItem(body)
  return NextResponse.json(item, { status: 201 })
}
```

### shadcn/ui CLI Commands

```bash
# Initialize shadcn/ui in Next.js project
npx shadcn@latest init -t next

# Add individual components
npx shadcn@latest add button input dialog sheet data-table form

# Add multiple components at once
npx shadcn@latest add badge card skeleton toast
```

## Common Mistakes

- **`'use client'` at the top of every file**: Only use it when the component needs useState, useEffect, event handlers, or browser APIs
- **Fetching data in Client Components**: Fetch in Server Components and pass data down as props — avoid useEffect + fetch patterns
- **Direct DOM manipulation**: Use React state and refs, not `document.querySelector` — Next.js pre-renders on the server
- **Missing loading.tsx**: Every route with async data should have a loading state — prevents blank screens during navigation
- **Importing server code in client**: Never import database clients, env secrets, or server actions into `'use client'` files — use the server/client boundary intentionally
