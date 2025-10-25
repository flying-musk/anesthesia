'use client';

import { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Tabs,
  Tab,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import {
  VideoLibrary,
  Upload,
  Subtitles,
  Translate,
  VolumeUp,
  Download,
  Edit,
  PlayArrow,
  Info,
  Add
} from '@mui/icons-material';

interface Video {
  id: number;
  title: string;
  file_path: string;
  duration: number;
  language: string;
  created_at: string;
  subtitle_count?: number;
  translation_count?: number;
}

interface Subtitle {
  id: number;
  video_id: number;
  start_time: number;
  end_time: number;
  text: string;
  language: string;
}

interface TTSRequest {
  text: string;
  language: string;
  slow: boolean;
}

export default function VideosPage() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);
  const [subtitles, setSubtitles] = useState<Subtitle[]>([]);
  const [loading, setLoading] = useState(false);
  const [tabValue, setTabValue] = useState(0);

  // Dialog states
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [subtitleDialogOpen, setSubtitleDialogOpen] = useState(false);
  const [ttsDialogOpen, setTtsDialogOpen] = useState(false);
  const [videoInfoDialogOpen, setVideoInfoDialogOpen] = useState(false);

  // Form states
  const [uploadTitle, setUploadTitle] = useState('');
  const [uploadLanguage, setUploadLanguage] = useState('ja');
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [ttsText, setTtsText] = useState('');
  const [ttsLanguage, setTtsLanguage] = useState('ja');
  const [translateTargetLang, setTranslateTargetLang] = useState('en');

  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'info'; text: string } | null>(null);

  const languages = [
    { code: 'ja', name: '日本語 (Japanese)' },
    { code: 'en', name: 'English' },
    { code: 'zh-TW', name: '繁體中文 (Traditional Chinese)' },
    { code: 'zh', name: '简体中文 (Simplified Chinese)' },
    { code: 'es', name: 'Español (Spanish)' },
    { code: 'fr', name: 'Français (French)' },
    { code: 'ko', name: '한국어 (Korean)' }
  ];

  // Load videos on component mount
  useEffect(() => {
    loadVideos();
  }, []);

  const loadVideos = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/videos/list');
      const data = await response.json();
      if (data.success) {
        setVideos(data.videos);
      }
    } catch (error) {
      console.error('Failed to load videos:', error);
      setMessage({ type: 'error', text: 'Failed to load videos' });
    } finally {
      setLoading(false);
    }
  };

  const loadSubtitles = async (videoId: number) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/v1/videos/${videoId}/subtitles`);
      const data = await response.json();
      if (data.success) {
        setSubtitles(data.subtitles);
      }
    } catch (error) {
      console.error('Failed to load subtitles:', error);
      setMessage({ type: 'error', text: 'Failed to load subtitles' });
    } finally {
      setLoading(false);
    }
  };

  const handleVideoSelect = (video: Video) => {
    setSelectedVideo(video);
    loadSubtitles(video.id);
    setTabValue(1); // Switch to subtitles tab
  };

  const handleUploadVideo = async () => {
    if (!uploadFile || !uploadTitle) {
      setMessage({ type: 'error', text: 'Please provide title and file' });
      return;
    }

    const formData = new FormData();
    formData.append('title', uploadTitle);
    formData.append('language', uploadLanguage);
    formData.append('file', uploadFile);

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/videos/upload', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();

      if (data.success) {
        setMessage({ type: 'success', text: 'Video uploaded successfully!' });
        setUploadDialogOpen(false);
        setUploadTitle('');
        setUploadFile(null);
        loadVideos();
      }
    } catch (error) {
      console.error('Upload failed:', error);
      setMessage({ type: 'error', text: 'Upload failed' });
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadSubtitles = async (videoId: number, format: 'vtt' | 'srt') => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/videos/${videoId}/subtitles/download?format=${format}&language=ja`
      );

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `subtitles_${videoId}.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setMessage({ type: 'success', text: `Subtitles downloaded as ${format.toUpperCase()}` });
    } catch (error) {
      console.error('Download failed:', error);
      setMessage({ type: 'error', text: 'Download failed' });
    }
  };

  const handleTranslate = async (videoId: number) => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/videos/${videoId}/translate?target_language=${translateTargetLang}`,
        { method: 'POST' }
      );
      const data = await response.json();

      if (data.success) {
        setMessage({
          type: 'success',
          text: `Translated ${data.total} subtitles to ${translateTargetLang}`
        });
      }
    } catch (error) {
      console.error('Translation failed:', error);
      setMessage({ type: 'error', text: 'Translation failed' });
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateTTS = async () => {
    if (!ttsText) {
      setMessage({ type: 'error', text: 'Please enter text' });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/tts/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: ttsText,
          language: ttsLanguage,
          slow: false
        })
      });

      const data = await response.json();

      if (data.success) {
        setMessage({
          type: 'success',
          text: `Audio generated: ${data.filename}`
        });
        setTtsDialogOpen(false);
        setTtsText('');
      }
    } catch (error) {
      console.error('TTS generation failed:', error);
      setMessage({ type: 'error', text: 'TTS generation failed' });
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = (seconds % 60).toFixed(1);
    return `${mins}:${secs.padStart(4, '0')}`;
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <VideoLibrary sx={{ fontSize: 40, color: 'primary.main' }} />
          <Typography variant="h3" component="h1">
            视频管理系统
          </Typography>
        </Box>
        <Typography variant="body1" color="text.secondary">
          Video Management System - Upload, Subtitle, Translate & TTS
        </Typography>
      </Box>

      {/* Alert Messages */}
      {message && (
        <Alert
          severity={message.type}
          onClose={() => setMessage(null)}
          sx={{ mb: 3 }}
        >
          {message.text}
        </Alert>
      )}

      {/* Action Buttons */}
      <Box sx={{ mb: 3, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <Button
          variant="contained"
          startIcon={<Upload />}
          onClick={() => setUploadDialogOpen(true)}
        >
          Upload Video
        </Button>
        <Button
          variant="outlined"
          startIcon={<VolumeUp />}
          onClick={() => setTtsDialogOpen(true)}
        >
          Generate TTS
        </Button>
      </Box>

      {/* Main Content Tabs */}
      <Paper sx={{ width: '100%' }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab label="Video Library" icon={<VideoLibrary />} iconPosition="start" />
          <Tab
            label="Subtitles & Translations"
            icon={<Subtitles />}
            iconPosition="start"
            disabled={!selectedVideo}
          />
        </Tabs>

        {/* Tab 0: Video Library */}
        {tabValue === 0 && (
          <Box sx={{ p: 3 }}>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <CircularProgress />
              </Box>
            ) : (
              <Grid container spacing={3}>
                {videos.map((video) => (
                  <Grid item xs={12} sm={6} md={4} key={video.id}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          {video.title}
                        </Typography>
                        <Box sx={{ my: 2 }}>
                          <Chip
                            label={video.language.toUpperCase()}
                            size="small"
                            color="primary"
                            sx={{ mr: 1 }}
                          />
                          <Chip
                            label={formatDuration(video.duration)}
                            size="small"
                            variant="outlined"
                          />
                        </Box>
                        <Typography variant="body2" color="text.secondary">
                          Subtitles: {video.subtitle_count || 0} | Translations: {video.translation_count || 0}
                        </Typography>
                      </CardContent>
                      <CardActions>
                        <Button
                          size="small"
                          startIcon={<Subtitles />}
                          onClick={() => handleVideoSelect(video)}
                        >
                          View Subtitles
                        </Button>
                        <IconButton size="small" onClick={() => {
                          setSelectedVideo(video);
                          setVideoInfoDialogOpen(true);
                        }}>
                          <Info />
                        </IconButton>
                      </CardActions>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}
          </Box>
        )}

        {/* Tab 1: Subtitles & Translations */}
        {tabValue === 1 && selectedVideo && (
          <Box sx={{ p: 3 }}>
            <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">
                {selectedVideo.title}
              </Typography>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <FormControl size="small" sx={{ minWidth: 120 }}>
                  <InputLabel>Translate to</InputLabel>
                  <Select
                    value={translateTargetLang}
                    label="Translate to"
                    onChange={(e) => setTranslateTargetLang(e.target.value)}
                  >
                    {languages.map((lang) => (
                      <MenuItem key={lang.code} value={lang.code}>
                        {lang.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Button
                  variant="outlined"
                  startIcon={<Translate />}
                  onClick={() => handleTranslate(selectedVideo.id)}
                >
                  Translate
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Download />}
                  onClick={() => handleDownloadSubtitles(selectedVideo.id, 'vtt')}
                >
                  Download VTT
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Download />}
                  onClick={() => handleDownloadSubtitles(selectedVideo.id, 'srt')}
                >
                  Download SRT
                </Button>
              </Box>
            </Box>

            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Time</TableCell>
                    <TableCell>Text</TableCell>
                    <TableCell>Language</TableCell>
                    <TableCell align="right">Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {subtitles.map((subtitle) => (
                    <TableRow key={subtitle.id}>
                      <TableCell>
                        {formatTime(subtitle.start_time)} - {formatTime(subtitle.end_time)}
                      </TableCell>
                      <TableCell>{subtitle.text}</TableCell>
                      <TableCell>
                        <Chip label={subtitle.language} size="small" />
                      </TableCell>
                      <TableCell align="right">
                        <IconButton size="small">
                          <Edit />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => {
                            setTtsText(subtitle.text);
                            setTtsLanguage(subtitle.language);
                            setTtsDialogOpen(true);
                          }}
                        >
                          <VolumeUp />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}
      </Paper>

      {/* Upload Video Dialog */}
      <Dialog open={uploadDialogOpen} onClose={() => setUploadDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Upload Video</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Video Title"
              fullWidth
              value={uploadTitle}
              onChange={(e) => setUploadTitle(e.target.value)}
            />
            <FormControl fullWidth>
              <InputLabel>Language</InputLabel>
              <Select
                value={uploadLanguage}
                label="Language"
                onChange={(e) => setUploadLanguage(e.target.value)}
              >
                {languages.map((lang) => (
                  <MenuItem key={lang.code} value={lang.code}>
                    {lang.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Button
              variant="outlined"
              component="label"
              startIcon={<Upload />}
            >
              {uploadFile ? uploadFile.name : 'Choose Video File'}
              <input
                type="file"
                hidden
                accept="video/*"
                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
              />
            </Button>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleUploadVideo} variant="contained" disabled={loading}>
            {loading ? <CircularProgress size={24} /> : 'Upload'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* TTS Dialog */}
      <Dialog open={ttsDialogOpen} onClose={() => setTtsDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Generate Text-to-Speech</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Language</InputLabel>
              <Select
                value={ttsLanguage}
                label="Language"
                onChange={(e) => setTtsLanguage(e.target.value)}
              >
                {languages.map((lang) => (
                  <MenuItem key={lang.code} value={lang.code}>
                    {lang.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              label="Text"
              multiline
              rows={4}
              fullWidth
              value={ttsText}
              onChange={(e) => setTtsText(e.target.value)}
              placeholder="Enter text to convert to speech..."
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTtsDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleGenerateTTS} variant="contained" disabled={loading}>
            {loading ? <CircularProgress size={24} /> : 'Generate Audio'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
