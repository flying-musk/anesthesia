import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';
import './i18n';

// Components
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import PatientManagement from './pages/PatientManagement';
import AnesthesiaGuidelines from './pages/AnesthesiaGuidelines';
import PatientDetails from './pages/PatientDetails';
import CreatePatient from './pages/CreatePatient';
import GenerateGuideline from './pages/GenerateGuideline';
import GuidelineDetails from './pages/GuidelineDetails';

// Create a client
const queryClient = new QueryClient();

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 500,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Box sx={{ display: 'flex', minHeight: '100vh' }}>
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/patients" element={<PatientManagement />} />
                <Route path="/patients/create" element={<CreatePatient />} />
                <Route path="/patients/:id" element={<PatientDetails />} />
                <Route path="/guidelines" element={<AnesthesiaGuidelines />} />
                <Route path="/guidelines/generate" element={<GenerateGuideline />} />
                <Route path="/guidelines/:id" element={<GuidelineDetails />} />
              </Routes>
            </Layout>
          </Box>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
