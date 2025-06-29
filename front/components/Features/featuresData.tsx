import { Feature } from "@/types/feature";

const featuresData: Feature[] = [
  {
    id: 1,
    icon: "🔒",
    title: "Votación Anónima y Segura",
    bullets: [
      "Cada voto se cifra en el navegador con claves públicas.",
      "No se guarda metadata del votante con el voto."
    ],
  },
  {
    id: 2,
    icon: "🗳️",
    title: "Soporte para Votaciones Múltiples",
    bullets: [
      "Votaciones de una o varias opciones.",
      "Configuración de fechas de inicio y cierre."
    ],
  },
  {
    id: 3,
    icon: "👥",
    title: "Autenticación Segura",
    bullets: [
      "Basada en tokens únicos por evento, generados por el sindicato.",
      "Opcional: integración con listas de emails, documentos o credenciales físicas."
    ],
  },
  {
    id: 4,
    icon: "📜",
    title: "Auditoría Completa",
    bullets: [
      "Los resultados pueden verificarse públicamente sin comprometer el anonimato.",
      "Hashes de votos y resultados exportables."
    ],
  },
  {
    id: 5,
    icon: "🔍",
    title: "Interfaz Clara y Accesible",
    bullets: [
      "Apta para dispositivos móviles.",
      "Modo oscuro y traducción multilenguaje."
    ],
  },
  {
    id: 6,
    icon: "🧱",
    title: "Diseño Monolítico pero Modular",
    bullets: [
      "Backend: Python (FastAPI) con SQLite/PostgreSQL.",
      "Frontend: React (ligero, rápido y accesible).",
      "Fácil de auto-hostear (Docker support incluido)."
    ],
  },
];

export default featuresData;
