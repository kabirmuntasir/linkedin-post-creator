import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  LinearProgress
} from '@mui/material';
import { ContentCopy, Send, AutoAwesome } from '@mui/icons-material';
import axios from 'axios';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

function App() {
  const [topic, setTopic] = useState('');
  const [industry, setIndustry] = useState('Technology');
  const [tone, setTone] = useState('professional');
  const [audience, setAudience] = useState('professionals');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState('');
  const [jobId, setJobId] = useState(null);

  const industries = [
    'Technology', 'Healthcare', 'Finance', 'Education', 'Marketing',
    'Sales', 'Consulting', 'Manufacturing', 'Retail', 'Media'
  ];

  const tones = [
    'professional', 'casual', 'inspiring', 'educational', 'conversational'
  ];

  const audiences = [
    'professionals', 'software engineers', 'data scientists', 'managers',
    'entrepreneurs', 'students', 'executives', 'consultants'
  ];

  const pollJobStatus = async (jobId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/status/${jobId}`);
      const { status, progress, result, error } = response.data;
      
      setProgress(progress || '');
      
      if (status === 'completed') {
        setResult(result);
        setLoading(false);
        setJobId(null);
      } else if (status === 'failed') {
        setError(error || 'Generation failed');
        setLoading(false);
        setJobId(null);
      } else {
        // Continue polling
        setTimeout(() => pollJobStatus(jobId), 2000);
      }
    } catch (err) {
      setError('Failed to check job status');
      setLoading(false);
      setJobId(null);
    }
  };

  const generatePost = async () => {
    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setProgress('Starting generation...');

    try {
      const response = await axios.post(`${API_BASE_URL}/api/generate-post`, {
        topic: topic.trim(),
        industry,
        tone,
        audience
      });

      const { job_id } = response.data;
      setJobId(job_id);
      
      // Start polling for status
      setTimeout(() => pollJobStatus(job_id), 1000);
      
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate post');
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (result?.post) {
      navigator.clipboard.writeText(result.post);
    }
  };

  const getWordCount = (text) => {
    return text ? text.split(/\s+/).filter(word => word.length > 0).length : 0;
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <AutoAwesome sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
          <Typography variant="h3" component="h1" gutterBottom>
            LinkedIn Post Creator
          </Typography>
          <Typography variant="h6" color="text.secondary">
            AI-powered LinkedIn content generation with multi-agent workflow
          </Typography>
        </Box>

        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            label="Topic"
            placeholder="e.g., AI and Machine Learning trends"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            variant="outlined"
            sx={{ mb: 2 }}
          />

          <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Industry</InputLabel>
              <Select
                value={industry}
                label="Industry"
                onChange={(e) => setIndustry(e.target.value)}
              >
                {industries.map((ind) => (
                  <MenuItem key={ind} value={ind}>{ind}</MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Tone</InputLabel>
              <Select
                value={tone}
                label="Tone"
                onChange={(e) => setTone(e.target.value)}
              >
                {tones.map((t) => (
                  <MenuItem key={t} value={t}>{t}</MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl sx={{ minWidth: 200 }}>
              <InputLabel>Target Audience</InputLabel>
              <Select
                value={audience}
                label="Target Audience"
                onChange={(e) => setAudience(e.target.value)}
              >
                {audiences.map((aud) => (
                  <MenuItem key={aud} value={aud}>{aud}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>

          <Button
            variant="contained"
            size="large"
            onClick={generatePost}
            disabled={loading || !topic.trim()}
            startIcon={loading ? <CircularProgress size={20} /> : <Send />}
            sx={{ mt: 2 }}
          >
            {loading ? 'Generating...' : 'Generate LinkedIn Post'}
          </Button>
        </Box>

        {loading && (
          <Box sx={{ mb: 3 }}>
            <LinearProgress sx={{ mb: 2 }} />
            <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center' }}>
              {progress}
            </Typography>
          </Box>
        )}

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Generated LinkedIn Post</Typography>
                <IconButton onClick={copyToClipboard} title="Copy to clipboard">
                  <ContentCopy />
                </IconButton>
              </Box>
              
              <Paper 
                variant="outlined" 
                sx={{ 
                  p: 2, 
                  mb: 2, 
                  backgroundColor: '#f8f9fa',
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'inherit'
                }}
              >
                {result.post}
              </Paper>

              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip 
                  label={`${getWordCount(result.post)} words`} 
                  size="small" 
                  color={getWordCount(result.post) <= 200 ? 'success' : 'warning'}
                />
                <Chip label={`Topic: ${result.topic}`} size="small" variant="outlined" />
                <Chip label={`Industry: ${result.industry}`} size="small" variant="outlined" />
                <Chip label={`Tone: ${result.tone}`} size="small" variant="outlined" />
                <Chip label={`Audience: ${result.audience}`} size="small" variant="outlined" />
              </Box>
            </CardContent>
          </Card>
        )}

        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Powered by CrewAI multi-agent workflow • Research → Create → Refine
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}

export default App;
