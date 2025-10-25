"""
字幕解析工具
将纯文本分割成字幕段落并计算时间轴
"""

import re
from typing import List, Dict


class SubtitleParser:
    """字幕解析器"""

    def __init__(
        self,
        chars_per_second: float = 15.0,  # 平均阅读速度（字符/秒）
        min_duration: float = 1.5,        # 最短显示时间（秒）
        max_duration: float = 7.0,        # 最长显示时间（秒）
        max_chars_per_subtitle: int = 100 # 每条字幕最多字符数
    ):
        self.chars_per_second = chars_per_second
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.max_chars_per_subtitle = max_chars_per_subtitle

    def parse_text_file(self, file_path: str) -> List[Dict]:
        """
        解析纯文本文件为字幕段落

        Args:
            file_path: 文本文件路径

        Returns:
            字幕段落列表，每个包含 sequence, text, start_time, end_time
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.parse_text(content)

    def parse_text(self, text: str) -> List[Dict]:
        """
        解析纯文本为字幕段落

        Args:
            text: 文本内容

        Returns:
            字幕段落列表
        """
        # 清理文本
        text = self._clean_text(text)

        # 分段
        segments = self._split_into_segments(text)

        # 计算时间轴
        subtitles = self._calculate_timings(segments)

        return subtitles

    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 去除前后空白
        text = text.strip()
        return text

    def _split_into_segments(self, text: str) -> List[str]:
        """将文本分割成适合的段落"""
        # 按句子分割（以句号、问号、感叹号为界）
        sentences = re.split(r'([.!?]+\s+)', text)

        segments = []
        current_segment = ""

        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            if i + 1 < len(sentences):
                sentence += sentences[i + 1]

            # 如果当前段落加上新句子超过最大长度，保存当前段落
            if len(current_segment) + len(sentence) > self.max_chars_per_subtitle:
                if current_segment:
                    segments.append(current_segment.strip())
                current_segment = sentence
            else:
                current_segment += sentence

        # 添加最后一个段落
        if current_segment:
            segments.append(current_segment.strip())

        return segments

    def _calculate_timings(self, segments: List[str]) -> List[Dict]:
        """计算每个段落的时间轴"""
        subtitles = []
        current_time = 0.0

        for idx, text in enumerate(segments, 1):
            # 计算显示时长
            char_count = len(text)
            duration = char_count / self.chars_per_second

            # 限制时长范围
            duration = max(self.min_duration, min(duration, self.max_duration))

            # 创建字幕对象
            subtitle = {
                "sequence": idx,
                "text": text,
                "start_time": round(current_time, 2),
                "end_time": round(current_time + duration, 2)
            }

            subtitles.append(subtitle)
            current_time += duration

        return subtitles

    def adjust_timing_for_video(
        self,
        subtitles: List[Dict],
        video_duration: float
    ) -> List[Dict]:
        """
        根据视频实际时长调整字幕时间轴

        Args:
            subtitles: 字幕列表
            video_duration: 视频总时长（秒）

        Returns:
            调整后的字幕列表
        """
        if not subtitles:
            return subtitles

        # 计算当前总时长
        current_duration = subtitles[-1]["end_time"]

        # 计算缩放比例
        scale_factor = video_duration / current_duration

        # 调整所有时间
        for subtitle in subtitles:
            subtitle["start_time"] = round(subtitle["start_time"] * scale_factor, 2)
            subtitle["end_time"] = round(subtitle["end_time"] * scale_factor, 2)

        return subtitles


def parse_srt_file(file_path: str) -> List[Dict]:
    """
    解析SRT格式字幕文件

    Args:
        file_path: SRT文件路径

    Returns:
        字幕段落列表
    """
    subtitles = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割字幕块
    blocks = re.split(r'\n\n+', content.strip())

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue

        # 序号
        try:
            sequence = int(lines[0])
        except ValueError:
            continue

        # 时间
        time_line = lines[1]
        time_match = re.match(
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})',
            time_line
        )
        if not time_match:
            continue

        # 转换为秒
        start_time = (
            int(time_match.group(1)) * 3600 +
            int(time_match.group(2)) * 60 +
            int(time_match.group(3)) +
            int(time_match.group(4)) / 1000
        )
        end_time = (
            int(time_match.group(5)) * 3600 +
            int(time_match.group(6)) * 60 +
            int(time_match.group(7)) +
            int(time_match.group(8)) / 1000
        )

        # 文本
        text = '\n'.join(lines[2:])

        subtitles.append({
            "sequence": sequence,
            "text": text,
            "start_time": start_time,
            "end_time": end_time
        })

    return subtitles
