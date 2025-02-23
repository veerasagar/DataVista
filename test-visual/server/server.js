import express from 'express';
import cors from 'cors';
import multer from 'multer';
import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';
import fs from 'fs';
import csv from 'csv-parser';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import path from 'path';

// ES Module fixes
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Initialize environment variables
dotenv.config();

const app = express();

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadDir = path.join(__dirname, 'uploads');
    // Create uploads directory if it doesn't exist
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir);
    }
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ storage: storage });

// Middleware
app.use(cors());
app.use(express.json());

console.log(process.env.GEMINI_API_KEY);
// Initialize Gemini
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Helper function to parse CSV files
function parseCSV(filePath) {
  return new Promise((resolve, reject) => {
    const results = [];
    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => resolve(results))
      .on('error', (error) => reject(error));
  });
}

// Helper function to analyze data using Gemini
async function analyzeData(data) {
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });
    
    const prompt = `Analyze this data and suggest the best visualization type. 
      Data: ${JSON.stringify(data)}
      Consider the data type, distribution, and relationships between variables.
      Return a JSON object with:
      1. chartType: string (one of: 'line', 'bar', 'pie', 'scatter', 'area')
      2. explanation: string (why this chart type is suitable)
      3. configuration: object (settings for Recharts library)
      4. dataTransformation: object (how the data should be processed)`;

    const result = await model.generateContent(prompt);
    const response = await result.response.text();
    
const cleanedContent = response
  .replace(/^```json\s*/, '')  // Remove the starting code fence and "json"
  .replace(/\s*```$/, ''); 
    console.log('Gemini response:', cleanedContent);
    return JSON.parse(cleanedContent);
  } catch (error) {
    console.error('Error analyzing data:', error);
    throw new Error('Failed to analyze data with Gemini');
  }
}

// Routes
app.post('/api/analyze', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    let data;
    const filePath = req.file.path;
    
    try {
      // Parse file based on type
      if (req.file.mimetype === 'text/csv') {
        data = await parseCSV(filePath);
      } else if (req.file.mimetype === 'application/json') {
        const fileContent = fs.readFileSync(filePath, 'utf8');
        data = JSON.parse(fileContent);
      } else {
        throw new Error('Unsupported file type');
      }

      // Get visualization suggestion from Gemini
      const visualizationSuggestion = await analyzeData(data);
      
      // Clean up uploaded file
      fs.unlink(filePath, (err) => {
        if (err) console.error('Error deleting file:', err);
      });
      
      res.json({
        data,
        visualization: visualizationSuggestion
      });
    } catch (error) {
      // Clean up file in case of error
      fs.unlink(filePath, (err) => {
        if (err) console.error('Error deleting file:', err);
      });
      throw error;
    }
  } catch (error) {
    console.error('Error processing request:', error);
    res.status(500).json({ 
      error: error.message || 'Internal server error'
    });
  }
});

// Health check route
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Error handling for uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  // Perform any cleanup if necessary
  process.exit(1);
});