'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Upload, Video, Loader2, CheckCircle, XCircle, Clock } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

const API_BASE = 'http://localhost:8080';

const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'zh-TW', name: '繁體中文' },
  { code: 'zh-CN', name: '简体中文' },
  { code: 'es', name: 'Español' },
  { code: 'ja', name: '日本語' },
  { code: 'ko', name: '한국어' },
];

export default function UploadPage() {
  // Video upload state
  const [videoTitle, setVideoTitle] = useState('');
  const [videoLanguage, setVideoLanguage] = useState('en');
  const [videoDescription, setVideoDescription] = useState('');
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [subtitleFile, setSubtitleFile] = useState<File | null>(null);


  // UI state
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Processing state
  const [processingStatus, setProcessingStatus] = useState<{
    stage: string;
    current: number;
    total: number;
    message: string;
  } | null>(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleVideoUpload = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!videoFile || !videoTitle) {
      setMessage({ type: 'error', text: 'Please provide video title and file' });
      return;
    }

    setUploading(true);
    setMessage(null);
    setShowSuccess(false);

    // 顯示上傳和處理狀態
    if (subtitleFile) {
      setProcessingStatus({
        stage: 'Processing',
        current: 10,
        total: 100,
        message: 'Uploading video, translating subtitles (5 languages), and generating audio files... This may take 3-5 minutes.',
      });
    } else {
      setProcessingStatus({
        stage: 'Uploading',
        current: 10,
        total: 100,
        message: 'Uploading video file...',
      });
    }

    // 模擬進度增長（讓用戶知道系統還在工作）
    const progressInterval = setInterval(() => {
      setProcessingStatus((prev) => {
        if (!prev) return null;
        const newCurrent = Math.min(prev.current + 5, 90); // 最多到 90%
        return { ...prev, current: newCurrent };
      });
    }, 3000); // 每3秒增加5%

    const formData = new FormData();
    formData.append('title', videoTitle);
    formData.append('language', videoLanguage);
    if (videoDescription) formData.append('description', videoDescription);
    formData.append('video_file', videoFile);
    if (subtitleFile) formData.append('subtitle_file', subtitleFile);

    try {
      const response = await fetch(`${API_BASE}/api/upload/video`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      // 清除進度計時器
      clearInterval(progressInterval);

      if (response.ok && data.success) {
        // 顯示成功訊息
        setShowSuccess(true);
        setProcessingStatus(null);

        let successMsg = 'Video uploaded successfully!';
        if (data.subtitle_uploaded) {
          successMsg = `✅ Video processed! ${data.subtitles_count || 0} subtitles, ${data.translations_generated || 0} translations, ${data.audio_files_generated || 0} audio languages available`;
        }

        setMessage({
          type: 'success',
          text: successMsg,
        });

        // Reset form after delay
        setTimeout(() => {
          setVideoTitle('');
          setVideoDescription('');
          setVideoFile(null);
          setSubtitleFile(null);
          setVideoLanguage('en');
          setShowSuccess(false);
        }, 3000);
      } else {
        setMessage({ type: 'error', text: data.detail || 'Upload failed' });
      }
    } catch (error) {
      // 清除進度計時器
      clearInterval(progressInterval);
      setMessage({ type: 'error', text: 'Network error. Please check if the server is running.' });
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
      setProcessingStatus(null);
    }
  };


  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Upload Video</h1>
        <p className="text-muted-foreground">
          Upload educational videos with optional subtitles
        </p>
      </div>

      {/* Processing Status */}
      {processingStatus && (
        <Card className="border-blue-200 bg-blue-50 dark:bg-blue-950 dark:border-blue-800">
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
                <h3 className="font-semibold text-blue-900 dark:text-blue-100">
                  {processingStatus.stage}
                </h3>
              </div>
              <div className="space-y-2">
                <Progress
                  value={(processingStatus.current / processingStatus.total) * 100}
                  className="h-3"
                />
                <div className="flex items-center justify-between text-xs text-blue-600 dark:text-blue-400">
                  <span>{Math.round((processingStatus.current / processingStatus.total) * 100)}%</span>
                  <span>{processingStatus.current} / {processingStatus.total}</span>
                </div>
              </div>
              <div className="bg-white dark:bg-gray-900 p-3 rounded-md border border-blue-100 dark:border-blue-900">
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  {processingStatus.message}
                </p>
              </div>
              <div className="flex items-center gap-2 text-xs text-blue-600 dark:text-blue-400">
                <Clock className="h-3 w-3" />
                <span>Please wait, this process cannot be interrupted...</span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Success Animation */}
      {showSuccess && (
        <Alert className="border-green-200 bg-green-50 dark:bg-green-950 dark:border-green-800">
          <CheckCircle className="h-5 w-5 text-green-600" />
          <AlertDescription className="text-green-900 dark:text-green-100 font-semibold">
            Processing Complete! All subtitles translated and audio tracks prepared.
          </AlertDescription>
        </Alert>
      )}

      {/* Error/Info Messages */}
      {message && !showSuccess && (
        <Alert variant={message.type === 'error' ? 'destructive' : 'default'}>
          {message.type === 'success' ? (
            <CheckCircle className="h-4 w-4" />
          ) : (
            <XCircle className="h-4 w-4" />
          )}
          <AlertDescription>{message.text}</AlertDescription>
        </Alert>
      )}

      {/* Video Upload Form */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Video className="h-5 w-5" />
            Upload Video
          </CardTitle>
          <CardDescription>
            Upload a video file with optional subtitles for the education system
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleVideoUpload} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="video-title">Video Title *</Label>
                  <Input
                    id="video-title"
                    placeholder="Enter video title"
                    value={videoTitle}
                    onChange={(e) => setVideoTitle(e.target.value)}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="video-language">Language</Label>
                  <Select value={videoLanguage} onValueChange={setVideoLanguage}>
                    <SelectTrigger id="video-language">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {LANGUAGES.map((lang) => (
                        <SelectItem key={lang.code} value={lang.code}>
                          {lang.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="video-description">Description</Label>
                  <Textarea
                    id="video-description"
                    placeholder="Enter video description (optional)"
                    value={videoDescription}
                    onChange={(e) => setVideoDescription(e.target.value)}
                    rows={3}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="video-file">Video File * (.mp4, .avi, .mov, .mkv)</Label>
                  <Input
                    id="video-file"
                    type="file"
                    accept=".mp4,.avi,.mov,.mkv"
                    onChange={(e) => setVideoFile(e.target.files?.[0] || null)}
                    required
                  />
                  {videoFile && (
                    <p className="text-sm text-muted-foreground">
                      Selected: {videoFile.name} ({Math.round(videoFile.size / 1024 / 1024)} MB)
                    </p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="subtitle-file">Subtitle File (optional) (.srt, .vtt, .txt)</Label>
                  <Input
                    id="subtitle-file"
                    type="file"
                    accept=".srt,.vtt,.txt"
                    onChange={(e) => setSubtitleFile(e.target.files?.[0] || null)}
                  />
                  {subtitleFile && (
                    <p className="text-sm text-muted-foreground">
                      Selected: {subtitleFile.name}
                    </p>
                  )}
                </div>

                <Button type="submit" disabled={uploading} className="w-full">
                  {uploading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Uploading...
                    </>
                  ) : (
                    <>
                      <Upload className="mr-2 h-4 w-4" />
                      Upload Video
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
    </div>
  );
}
