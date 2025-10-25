'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { Trash2, Video, Loader2, RefreshCw, AlertCircle } from 'lucide-react';

const API_BASE = 'http://localhost:8080';

interface Video {
  id: number;
  title: string;
  duration: number;
  file_path: string;
  subtitle_count: number;
  available_languages: string[];
}

const LANGUAGE_NAMES: Record<string, string> = {
  'en': 'English',
  'zh-TW': '繁體中文',
  'zh-CN': '简体中文',
  'es': 'Español',
  'ja': '日本語',
  'ko': '한국어',
};

export default function ManagePage() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [videoToDelete, setVideoToDelete] = useState<Video | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    loadVideos();
  }, []);

  const loadVideos = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const response = await fetch(`${API_BASE}/api/subtitles/videos`);
      if (!response.ok) throw new Error('Failed to load videos');
      const data = await response.json();
      setVideos(data);
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to load videos. Make sure the API server is running.' });
      console.error('Error loading videos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = (video: Video) => {
    setVideoToDelete(video);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!videoToDelete) return;

    setDeleting(true);
    setMessage(null);

    try {
      const response = await fetch(`${API_BASE}/api/upload/video/${videoToDelete.id}`, {
        method: 'DELETE',
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setMessage({ type: 'success', text: `Video "${videoToDelete.title}" deleted successfully!` });
        // Reload videos list
        await loadVideos();
      } else {
        setMessage({ type: 'error', text: data.detail || 'Delete failed' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Network error. Please check if the server is running.' });
      console.error('Delete error:', error);
    } finally {
      setDeleting(false);
      setDeleteDialogOpen(false);
      setVideoToDelete(null);
    }
  };

  const formatDuration = (seconds: number) => {
    if (!seconds) return 'N/A';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return mins === 0 ? `${secs}s` : `${mins}m ${secs}s`;
  };

  const getFileName = (path: string) => {
    return path.split('/').pop() || path;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Manage Videos</h1>
          <p className="text-muted-foreground">
            View and delete uploaded videos and their associated data
          </p>
        </div>
        <Button onClick={loadVideos} disabled={loading} variant="outline">
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {/* Messages */}
      {message && (
        <Alert variant={message.type === 'error' ? 'destructive' : 'default'}>
          {message.type === 'error' && <AlertCircle className="h-4 w-4" />}
          <AlertDescription>{message.text}</AlertDescription>
        </Alert>
      )}

      {/* Videos Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Video className="h-5 w-5" />
            Videos ({videos.length})
          </CardTitle>
          <CardDescription>
            All uploaded videos with subtitles and audio tracks
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : videos.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              No videos uploaded yet
            </div>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>ID</TableHead>
                    <TableHead>Title</TableHead>
                    <TableHead>Duration</TableHead>
                    <TableHead>Subtitles</TableHead>
                    <TableHead>Languages</TableHead>
                    <TableHead>File Name</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {videos.map((video) => (
                    <TableRow key={video.id}>
                      <TableCell className="font-medium">{video.id}</TableCell>
                      <TableCell>{video.title}</TableCell>
                      <TableCell>{formatDuration(video.duration)}</TableCell>
                      <TableCell>{video.subtitle_count} segments</TableCell>
                      <TableCell>
                        <div className="flex flex-wrap gap-1">
                          {video.available_languages.slice(0, 3).map((lang) => (
                            <Badge key={lang} variant="secondary" className="text-xs">
                              {LANGUAGE_NAMES[lang] || lang}
                            </Badge>
                          ))}
                          {video.available_languages.length > 3 && (
                            <Badge variant="outline" className="text-xs">
                              +{video.available_languages.length - 3}
                            </Badge>
                          )}
                        </div>
                      </TableCell>
                      <TableCell className="text-xs text-muted-foreground">
                        {getFileName(video.file_path)}
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleDeleteClick(video)}
                        >
                          <Trash2 className="h-4 w-4 mr-1" />
                          Delete
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This will permanently delete the video <strong>"{videoToDelete?.title}"</strong> and all associated data including:
              <ul className="list-disc list-inside mt-2 space-y-1">
                <li>Video file</li>
                <li>All subtitles ({videoToDelete?.subtitle_count} segments)</li>
                <li>All translations ({videoToDelete?.available_languages.length} languages)</li>
                <li>All audio files</li>
              </ul>
              <p className="mt-2 text-destructive font-semibold">This action cannot be undone.</p>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={deleting}>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteConfirm}
              disabled={deleting}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              {deleting ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Deleting...
                </>
              ) : (
                <>
                  <Trash2 className="h-4 w-4 mr-2" />
                  Delete
                </>
              )}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
