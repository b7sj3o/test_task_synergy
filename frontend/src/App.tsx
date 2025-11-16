import { Route, Routes, Navigate } from "react-router-dom";
import UsersPage from "./pages/Main";

export default function App() {
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-40 border-b border-white/10 bg-slate-900/40 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <div className="text-lg font-semibold">
            Synergy — тестове завдання
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">
        <Routes>
          <Route path="/" element={<UsersPage />} />
        </Routes>
      </main>
    </div>
  );
}


