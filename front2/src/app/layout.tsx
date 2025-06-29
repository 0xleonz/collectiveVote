"use client";

import './globals.css';
import Link from 'next/link';
import { useState } from 'react';

// Componente Navbar separado y estilizado
function Navbar({ user, setUser }: { user: { role: 'admin' | 'user' } | null; setUser: any }) {
  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-mocha-background border-b border-mocha-muted shadow-lg">
      <div className="flex items-center space-x-6">
        <Link href="/" className="text-lg font-semibold hover:text-mocha-blue transition">
          CollectiveVote
        </Link>
        <Link href="/vote" className="hover:text-mocha-blue transition">
          Votación
        </Link>
        <Link href="/create" className="hover:text-mocha-blue transition">
          Crear
        </Link>
        <Link href="/about" className="hover:text-mocha-blue transition">
          About
        </Link>
      </div>

      <div className="flex items-center space-x-4">
        {user ? (
          <>
            <span className="px-2 py-1 text-sm bg-mocha-overlay rounded">
              {user.role.toUpperCase()}
            </span>
            <button
              onClick={() => setUser(null)}
              className="px-3 py-1 text-sm border border-mocha-muted rounded hover:bg-mocha-overlay transition"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <button
              onClick={() => setUser({ role: 'user' })}
              className="px-3 py-1 text-sm border border-mocha-muted rounded hover:bg-mocha-overlay transition"
            >
              Login
            </button>
            <button
              onClick={() => setUser({ role: 'admin' })}
              className="px-3 py-1 text-sm bg-mocha-peach text-mocha-background rounded hover:bg-mocha-blue transition"
            >
              Signup
            </button>
          </>
        )}
      </div>
    </nav>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<{ role: 'admin' | 'user' } | null>(null);

  return (
    <html lang="es">
      <body className="bg-mocha-background text-mocha-text min-h-screen">
        <Navbar user={user} setUser={setUser} />
        <main className="p-6">{children}</main>
      </body>
    </html>
  );
}

