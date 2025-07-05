"use client";
import { useState } from 'react';

export default function CreatePage() {
  const [title, setTitle] = useState('');

  const crear = () => {
    // aquí llamarías a tu API para crear la votación real
    alert(`Votación “${title}” creada`);
    setTitle('');
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl">Crear una nueva votación</h2>
      <input
        value={title}
        onChange={e => setTitle(e.target.value)}
        placeholder="Título de la votación"
        className="w-full px-3 py-2 border rounded bg-mocha-background text-mocha-text"
      />
      <button
        onClick={crear}
        className="px-4 py-2 bg-mocha-peach text-mocha-background rounded"
      >
        Crear
      </button>
    </div>
  );
}

