'use client';

import { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Box,
  Card,
  CardContent,
  Chip,
  Grid,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Divider,
} from '@mui/material';
import { Send, QuestionMark, CheckCircle, Warning } from '@mui/icons-material';

interface QAResponse {
  answer: string;
  needs_doctor: boolean;
  category: string;
  confidence: string;
  suggested_action: string;
}

export default function TestingPage() {
  const [question, setQuestion] = useState('');
  const [language, setLanguage] = useState('en');
  const [response, setResponse] = useState<QAResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [commonQuestions, setCommonQuestions] = useState<string[]>([]);

  // 语言选项
  const languages = [
    { code: 'en', name: 'English' },
    { code: 'zh-TW', name: '繁體中文' },
    { code: 'es', name: 'Español' },
    { code: 'fr', name: 'Français' },
  ];

  // 获取常见问题
  const loadCommonQuestions = async (lang: string) => {
    try {
      const res = await fetch(`http://localhost:8000/api/v1/qa/common-questions?language=${lang}`);
      const data = await res.json();
      setCommonQuestions(data.questions || []);
    } catch (err) {
      console.error('Failed to load common questions:', err);
    }
  };

  // 提交问题
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError('');
    setResponse(null);

    try {
      const res = await fetch('http://localhost:8000/api/v1/qa/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          language,
        }),
      });

      if (!res.ok) {
        throw new Error('Failed to get response');
      }

      const data: QAResponse = await res.json();
      setResponse(data);
    } catch (err) {
      setError('Failed to get answer. Make sure the backend is running and Ollama is available.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // 选择常见问题
  const handleSelectQuestion = (q: string) => {
    setQuestion(q);
  };

  // 更改语言时加载对应的常见问题
  const handleLanguageChange = (lang: string) => {
    setLanguage(lang);
    loadCommonQuestions(lang);
  };

  // 组件加载时获取默认语言的常见问题
  useState(() => {
    loadCommonQuestions('en');
  });

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
        🧪 HackthonProject-5 功能测试
      </Typography>

      <Typography variant="h5" gutterBottom align="center" color="text.secondary" sx={{ mb: 4 }}>
        RAG 问答系统演示
      </Typography>

      <Grid container spacing={3}>
        {/* 左侧：常见问题 */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <QuestionMark sx={{ mr: 1, verticalAlign: 'middle' }} />
                常见问题
              </Typography>
              <Divider sx={{ my: 2 }} />
              <List>
                {commonQuestions.map((q, index) => (
                  <ListItem key={index} disablePadding>
                    <ListItemButton onClick={() => handleSelectQuestion(q)}>
                      <ListItemText
                        primary={q}
                        primaryTypographyProps={{ variant: 'body2' }}
                      />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* 右侧：问答界面 */}
        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <form onSubmit={handleSubmit}>
              <Box sx={{ mb: 3 }}>
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Language / 语言</InputLabel>
                  <Select
                    value={language}
                    label="Language / 语言"
                    onChange={(e) => handleLanguageChange(e.target.value)}
                  >
                    {languages.map((lang) => (
                      <MenuItem key={lang.code} value={lang.code}>
                        {lang.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>

                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  variant="outlined"
                  label="Ask your question about anesthesia"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="e.g., Is general anesthesia safe?"
                />
              </Box>

              <Button
                type="submit"
                variant="contained"
                size="large"
                disabled={loading || !question.trim()}
                startIcon={loading ? <CircularProgress size={20} /> : <Send />}
                fullWidth
              >
                {loading ? 'Processing...' : 'Ask Question'}
              </Button>
            </form>

            {error && (
              <Alert severity="error" sx={{ mt: 3 }}>
                {error}
              </Alert>
            )}

            {response && (
              <Box sx={{ mt: 4 }}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ mb: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                      <Chip
                        label={`Category: ${response.category}`}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                      <Chip
                        label={`Confidence: ${response.confidence}`}
                        size="small"
                        color={response.confidence === 'high' ? 'success' : 'warning'}
                        variant="outlined"
                      />
                      {response.needs_doctor && (
                        <Chip
                          label="Doctor consultation recommended"
                          size="small"
                          color="warning"
                          icon={<Warning />}
                        />
                      )}
                    </Box>

                    <Divider sx={{ my: 2 }} />

                    <Typography variant="h6" gutterBottom>
                      Answer:
                    </Typography>
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', mb: 2 }}>
                      {response.answer}
                    </Typography>

                    <Alert
                      severity={response.needs_doctor ? 'warning' : 'info'}
                      icon={response.needs_doctor ? <Warning /> : <CheckCircle />}
                    >
                      {response.suggested_action}
                    </Alert>
                  </CardContent>
                </Card>
              </Box>
            )}

            {/* 说明 */}
            <Box sx={{ mt: 4, p: 2, bgcolor: 'background.default', borderRadius: 1 }}>
              <Typography variant="subtitle2" gutterBottom>
                📝 说明：
              </Typography>
              <Typography variant="body2" color="text.secondary">
                • 此功能使用 HackthonProject-5 的 RAG (Retrieval-Augmented Generation) 系统
                <br />
                • 基于 LangChain + Ollama 实现智能问答
                <br />
                • 支持多语言：英文、繁体中文、西班牙文、法文
                <br />
                • 后端 API: <code>POST /api/v1/qa/ask</code>
                <br />
                <br />
                ⚠️ 请确保 Ollama 服务正在运行，并已安装 llama3:8b 模型
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}
