'use client';

import { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Play, Info } from 'lucide-react';
import ChatBox from '@/components/chat/ChatBox';

interface Video {
  id: number;
  title: string;
  file_path: string;
  duration: number;
  language: string;
  available_languages: string[];
  subtitle_count: number;
}

const LANGUAGE_NAMES: Record<string, string> = {
  'en': 'English',
  'zh-TW': '繁體中文',
  'zh-CN': '简体中文',
  'es': 'Español',
  'ja': '日本語',
  'ko': '한국어',
};

const API_BASE = 'http://localhost:8080';

export default function PlayerPage() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);
  const [subtitleLanguage, setSubtitleLanguage] = useState<string>('');
  const [audioLanguage, setAudioLanguage] = useState<string>('original');
  const [availableAudioLanguages, setAvailableAudioLanguages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [playerLoaded, setPlayerLoaded] = useState(false);

  const videoRef = useRef<HTMLVideoElement>(null);
  const playerInstanceRef = useRef<any>(null);
  const audioPlayerRef = useRef<HTMLAudioElement | null>(null);

  // Load videos on mount
  useEffect(() => {
    loadVideos();
    loadVideoJsScript();
  }, []);

  const loadVideoJsScript = () => {
    // Check if already loaded
    if ((window as any).videojs) {
      console.log('Video.js already loaded');
      return;
    }

    // Load Video.js CSS if not already loaded
    if (!document.querySelector('link[href*="video-js.css"]')) {
      const link = document.createElement('link');
      link.href = 'https://vjs.zencdn.net/8.6.1/video-js.css';
      link.rel = 'stylesheet';
      document.head.appendChild(link);
    }

    // Load Video.js script if not already loaded
    if (!document.querySelector('script[src*="video.min.js"]')) {
      const script = document.createElement('script');
      script.src = 'https://vjs.zencdn.net/8.6.1/video.min.js';
      script.async = true;
      script.onload = () => {
        console.log('Video.js loaded successfully');
      };
      document.head.appendChild(script);
    }
  };

  const loadVideos = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/api/subtitles/videos`);
      if (!response.ok) throw new Error('Failed to load videos');
      const data = await response.json();
      setVideos(data);
    } catch (err) {
      setError('Failed to load videos. Make sure the API server is running on port 8080.');
      console.error('Error loading videos:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadAvailableAudioLanguages = async (videoId: number) => {
    try {
      const response = await fetch(`${API_BASE}/api/audio/videos`);
      if (!response.ok) return;
      const videos = await response.json();
      const video = videos.find((v: any) => v.id === videoId);
      if (video && video.available_audio_languages) {
        setAvailableAudioLanguages(video.available_audio_languages);
      }
    } catch (err) {
      console.error('Error loading audio languages:', err);
    }
  };

  const handleVideoSelect = async (videoId: string) => {
    const video = videos.find((v) => v.id === parseInt(videoId));
    if (!video) return;

    setSelectedVideo(video);
    setSubtitleLanguage(video.available_languages[0] || 'en');
    setAudioLanguage('original');
    setPlayerLoaded(false);

    await loadAvailableAudioLanguages(video.id);
  };

  const handleLoadVideo = async () => {
    console.log('handleLoadVideo called');
    console.log('selectedVideo:', selectedVideo);
    console.log('subtitleLanguage:', subtitleLanguage);

    if (!selectedVideo || !subtitleLanguage) {
      setError('Please select a video and subtitle language');
      return;
    }

    setError(null);

    try {
      await initializePlayer();
    } catch (err) {
      console.error('Error initializing player:', err);
      setError('Failed to initialize video player');
    }
  };

  const initializePlayer = async () => {
    console.log('initializePlayer called');
    if (!videoRef.current || !selectedVideo) {
      console.log('Missing videoRef or selectedVideo');
      return;
    }

    // Dispose of existing player
    if (playerInstanceRef.current) {
      console.log('Disposing existing player');
      playerInstanceRef.current.dispose();
    }
    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause();
      audioPlayerRef.current = null;
    }

    // Wait for Video.js to be available with timeout
    return new Promise<void>((resolve, reject) => {
      let attempts = 0;
      const maxAttempts = 50; // 5 seconds timeout

      const checkVideoJs = setInterval(() => {
        attempts++;
        console.log(`Checking for Video.js... attempt ${attempts}`);

        if (attempts > maxAttempts) {
          clearInterval(checkVideoJs);
          reject(new Error('Video.js failed to load'));
          return;
        }

        if ((window as any).videojs) {
          clearInterval(checkVideoJs);
          console.log('Video.js found, initializing player...');

        // Initialize player
        const player = (window as any).videojs(videoRef.current, {
          controls: true,
          autoplay: false,
          preload: 'auto',
          fluid: true,
          playbackRates: [0.5, 1, 1.5, 2],
        });

        playerInstanceRef.current = player;

        // Set video source
        const filename = selectedVideo.file_path.split('/').pop();
        const videoSrc = `${API_BASE}/videos/${filename}`;

        player.src({
          type: 'video/mp4',
          src: videoSrc,
        });

        // Handle audio
        if (audioLanguage && audioLanguage !== 'original') {
          player.muted(true);
          const audioUrl = `${API_BASE}/api/audio/videos/${selectedVideo.id}/audio/${audioLanguage}`;
          const audio = new Audio(audioUrl);
          audioPlayerRef.current = audio;

          // Sync audio with video
          player.on('play', () => audio.play());
          player.on('pause', () => audio.pause());
          player.on('seeked', () => {
            audio.currentTime = player.currentTime();
          });
          player.on('ratechange', () => {
            audio.playbackRate = player.playbackRate();
          });
        } else {
          player.muted(false);
        }

        // Add subtitles
        const subtitleUrl = `${API_BASE}/api/subtitles/videos/${selectedVideo.id}/subtitles/${subtitleLanguage}.vtt`;
        player.addRemoteTextTrack({
          kind: 'subtitles',
          src: subtitleUrl,
          srclang: subtitleLanguage,
          label: LANGUAGE_NAMES[subtitleLanguage] || subtitleLanguage,
          default: true,
        }, false);

        // Ensure subtitles are showing
        setTimeout(() => {
          const tracks = player.textTracks();
          for (let i = 0; i < tracks.length; i++) {
            if (tracks[i].kind === 'subtitles') {
              tracks[i].mode = 'showing';
            }
          }
        }, 100);

        setPlayerLoaded(true);
        console.log('Player initialized successfully');
        resolve();
        }
      }, 100);
    });
  };

  const formatDuration = (seconds: number) => {
    if (!seconds) return 'N/A';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return mins === 0 ? `${secs}s` : `${mins}m ${secs}s`;
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Video Player</h1>
        <p className="text-muted-foreground">
          Watch educational videos with multi-language subtitles and audio
        </p>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Select Video</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Video Selection */}
          <div className="space-y-2">
            <Label htmlFor="video-select">Choose a Video</Label>
            <Select onValueChange={handleVideoSelect} disabled={loading}>
              <SelectTrigger id="video-select">
                <SelectValue placeholder={loading ? 'Loading videos...' : 'Select a video'} />
              </SelectTrigger>
              <SelectContent>
                {videos.map((video) => (
                  <SelectItem key={video.id} value={video.id.toString()}>
                    {video.title} ({formatDuration(video.duration)})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Video Info */}
          {selectedVideo && (
            <Card>
              <CardContent className="pt-6 space-y-2">
                <div className="flex items-start gap-2">
                  <Info className="h-4 w-4 mt-0.5 text-muted-foreground" />
                  <div className="space-y-1">
                    <h3 className="font-semibold">{selectedVideo.title}</h3>
                    <p className="text-sm text-muted-foreground">
                      Duration: {formatDuration(selectedVideo.duration)} | Subtitles: {selectedVideo.subtitle_count} segments
                    </p>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {selectedVideo.available_languages.map((lang) => (
                        <Badge key={lang} variant="secondary">
                          {LANGUAGE_NAMES[lang] || lang}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Subtitle Language Selection */}
          {selectedVideo && (
            <div className="space-y-2">
              <Label htmlFor="subtitle-select">Subtitle Language</Label>
              <Select value={subtitleLanguage} onValueChange={setSubtitleLanguage}>
                <SelectTrigger id="subtitle-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {selectedVideo.available_languages.map((lang) => (
                    <SelectItem key={lang} value={lang}>
                      {LANGUAGE_NAMES[lang] || lang}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}

          {/* Audio Language Selection */}
          {selectedVideo && (
            <div className="space-y-2">
              <Label htmlFor="audio-select">Audio Language</Label>
              <Select value={audioLanguage} onValueChange={setAudioLanguage}>
                <SelectTrigger id="audio-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="original">Original Audio</SelectItem>
                  {availableAudioLanguages.map((lang) => (
                    <SelectItem key={lang} value={lang}>
                      {LANGUAGE_NAMES[lang] || lang} (Dubbed)
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}

          {/* Load Button */}
          {selectedVideo && !playerLoaded ? (
            <div className="space-y-2">
              <p className="text-xs text-muted-foreground">
                Debug: Video selected: {selectedVideo?.title}, Player loaded: {playerLoaded ? 'Yes' : 'No'}
              </p>
              <Button
                onClick={() => {
                  console.log('Button clicked!');
                  handleLoadVideo();
                }}
                className="w-full"
                size="lg"
              >
                <Play className="h-4 w-4 mr-2" />
                Load Video with Subtitles
              </Button>
            </div>
          ) : (
            selectedVideo && (
              <p className="text-sm text-muted-foreground">
                Player already loaded
              </p>
            )
          )}
        </CardContent>
      </Card>

      {/* Video Player */}
      {selectedVideo && (
        <Card style={{ display: playerLoaded ? 'block' : 'none' }}>
          <CardContent className="pt-6">
            <div className="relative bg-black rounded-lg overflow-hidden">
              <video
                ref={videoRef}
                id="video-player"
                className="video-js vjs-default-skin w-full"
                controls
                preload="auto"
              >
                <p className="vjs-no-js">
                  To view this video please enable JavaScript
                </p>
              </video>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Chat Box - Show after video is loaded */}
      {selectedVideo && playerLoaded && (
        <div className="mt-6">
          <ChatBox language={subtitleLanguage || 'en'} />
        </div>
      )}
    </div>
  );
}
