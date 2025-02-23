import React from 'react';
import { Paper, Typography, Box } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const FileUpload = ({ onFileUpload, isLoading }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: onFileUpload,
    accept: {
      'application/json': ['.json'],
      'text/csv': ['.csv']
    },
    disabled: isLoading,
    multiple: false
  });

  return (
    <Paper
      {...getRootProps()}
      sx={{
        p: 4,
        mb: 3,
        textAlign: 'center',
        backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
        cursor: isLoading ? 'not-allowed' : 'pointer',
        border: '2px dashed',
        borderColor: isDragActive ? 'primary.main' : 'grey.300',
        '&:hover': {
          borderColor: 'primary.main',
          backgroundColor: 'action.hover'
        }
      }}
    >
      <input {...getInputProps()} />
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
        <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main' }} />
        <Typography variant="h6" component="div">
          {isDragActive
            ? "Drop the file here..."
            : "Drag 'n' drop a CSV or JSON file here, or click to select"}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Supported formats: CSV, JSON
        </Typography>
      </Box>
    </Paper>
  );
};

export default FileUpload;