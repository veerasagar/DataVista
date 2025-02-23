import React, { useState } from 'react';
import { 
  Container, 
  Paper, 
  Typography, 
  Box,
  CircularProgress,
  Alert,
  Snackbar
} from '@mui/material';
import axios from 'axios';
import FileUpload from './components/FileUpload';
import VisualizationChart from './components/VisualizationChart';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [visualization, setVisualization] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const handleFileUpload = async (acceptedFiles) => {
    setLoading(true);
    setError(null);
    const file = acceptedFiles[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/analyze`, formData);
      setVisualization(response.data);
      setSnackbar({
        open: true,
        message: 'Data analyzed successfully!',
        severity: 'success'
      });
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Error processing file';
      setError(errorMessage);
      setSnackbar({
        open: true,
        message: errorMessage,
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSnackbarClose = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h1" component="h1" gutterBottom align="center">
          Data Visualization Dashboard
        </Typography>
        
        <FileUpload onFileUpload={handleFileUpload} isLoading={loading} />

        {loading && (
          <Box display="flex" justifyContent="center" my={4}>
            <CircularProgress />
          </Box>
        )}

        {visualization && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h2" gutterBottom>
              Suggested Visualization
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              {visualization.visualization.explanation}
            </Typography>
            <Box sx={{ height: 400, mt: 4 }}>
              <VisualizationChart 
                data={visualization.data}
                visualization={visualization.visualization}
              />
            </Box>
          </Paper>
        )}

        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={handleSnackbarClose}
        >
          <Alert 
            onClose={handleSnackbarClose} 
            severity={snackbar.severity}
            sx={{ width: '100%' }}
          >
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
}

export default App;