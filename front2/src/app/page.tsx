"use client";
import { useState } from 'react';

export default function HomePage() {
  // simula si hay votación activa
  const [activeVote, setActiveVote] = useState<boolean>(false);
  const [userRole] = useState<'admin'|'user'>('user'); // ajusta según auth real

  if (!activeVote) {
    return userRole === 'admin' ? (
      <button
        onClick={() => setActiveVote(true)}
        className="px-4 py-2 bg-mocha-peach text-mocha-background rounded"
      >
        Crear nueva votación
      </button>
    ) : (
      <button
        onClick={() => setActiveVote(true)}
        className="px-4 py-2 bg-mocha-blue text-mocha-background rounded"
      >
        Proponer votación
      </button>
    );
  }

  // si hay votación, redirige a /vote
  if (activeVote) {
    window.location.href = '/vote';
    return null;
  }

  return null;
}
