import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import HomePage from './components/HomePage';
import Packages from './components/Packages';
import BasicPage from './components/BasicPage';
import PremiumPage from './components/PremiumPage';
import UltraPage from './components/UltraPage';
import ElitePage from './components/ElitePage';
import ContactPage from './components/ContactPage';
import ExerciseBuilder from './components/ExerciseBuilder';
import WorkoutHistory from './components/WorkoutHistory';
import AuthPage from './components/AuthPage';
import NotFound from './components/NotFound';

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />

          <Route path="packages" element={<Packages />}>
            <Route path="basic" element={<BasicPage />} />
            <Route path="premium" element={<PremiumPage />} />
            <Route path="ultra" element={<UltraPage />} />
            <Route path="elite" element={<ElitePage />} />
          </Route>

          <Route path="contact" element={<ContactPage />} />
          <Route path="builder" element={<ExerciseBuilder />} />
          <Route path="history" element={<WorkoutHistory />} />
          <Route path="auth" element={<AuthPage />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}
