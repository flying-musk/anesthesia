'use client';

import { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Send, Loader2, MessageCircle, AlertCircle, CheckCircle } from 'lucide-react';

const API_BASE = 'http://localhost:8080';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  needsDoctor?: boolean;
  category?: string;
  confidence?: string;
  suggestedAction?: string;
}

interface ChatBoxProps {
  language: string;
}

const LANGUAGE_NAMES: Record<string, string> = {
  'en': 'English',
  'zh-TW': '繁體中文',
  'zh-CN': '简体中文',
  'es': 'Español',
  'ja': '日本語',
  'ko': '한국어',
};

export default function ChatBox({ language }: ChatBoxProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [commonQuestions, setCommonQuestions] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadCommonQuestions();
  }, [language]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadCommonQuestions = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/qa/common-questions?language=${language}`);
      const data = await response.json();
      setCommonQuestions(data.questions || []);
    } catch (error) {
      console.error('Failed to load common questions:', error);
    }
  };

  const sendMessage = async (question: string) => {
    if (!question.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/api/qa/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          language,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get answer');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: data.answer,
        needsDoctor: data.needs_doctor,
        category: data.category,
        confidence: data.confidence,
        suggestedAction: data.suggested_action,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(input);
  };

  const handleCommonQuestionClick = (question: string) => {
    sendMessage(question);
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageCircle className="h-5 w-5" />
          Ask Questions About Anesthesia
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col gap-4">
        {/* Common Questions */}
        {messages.length === 0 && commonQuestions.length > 0 && (
          <div className="space-y-2">
            <p className="text-sm text-muted-foreground">Common questions:</p>
            <div className="flex flex-wrap gap-2">
              {commonQuestions.slice(0, 5).map((q, idx) => (
                <Button
                  key={idx}
                  variant="outline"
                  size="sm"
                  onClick={() => handleCommonQuestionClick(q)}
                  className="text-xs"
                >
                  {q}
                </Button>
              ))}
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 min-h-[300px] max-h-[500px]">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.type === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                {message.type === 'assistant' && (
                  <div className="mt-2 space-y-1">
                    {message.category && (
                      <Badge variant="secondary" className="text-xs">
                        {message.category}
                      </Badge>
                    )}
                    {message.needsDoctor && (
                      <Alert className="mt-2 border-orange-200 bg-orange-50 dark:bg-orange-950 dark:border-orange-800">
                        <AlertCircle className="h-4 w-4 text-orange-600" />
                        <AlertDescription className="text-xs text-orange-900 dark:text-orange-100">
                          {message.suggestedAction}
                        </AlertDescription>
                      </Alert>
                    )}
                    {!message.needsDoctor && message.confidence && (
                      <div className="flex items-center gap-1 mt-1">
                        <CheckCircle className="h-3 w-3 text-green-600" />
                        <span className="text-xs text-muted-foreground">
                          Confidence: {message.confidence}
                        </span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-muted rounded-lg px-4 py-2">
                <Loader2 className="h-4 w-4 animate-spin" />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Ask a question in ${LANGUAGE_NAMES[language] || language}...`}
            disabled={loading}
            className="flex-1"
          />
          <Button type="submit" disabled={loading || !input.trim()}>
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
