#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

class SubtitleMatcher:
    """Match video filenames to subtitle files"""

    # Subtitle file naming pattern: sabri_maranan_s1eXX_english-{name}.srt
    SUBTITLE_PATTERNS = {
        1: "sabri_maranan_s1e01_english-Babysitters_Big_Brother.srt",
        2: "sabri_maranan_s1e02_english-Huge_Mistake.srt",
        3: "sabri_maranan_s1e03_english-Happy_Itzik.srt",
        4: "sabri_maranan_s1e04_english-Holiday_Evening.srt",
        5: "sabri_maranan_s1e05_english-Saturday_Morning_Hard_Day.srt",
        6: "sabri_maranan_s1e06_english-Stockholm_Syndrome.srt",
        7: "sabri_maranan_s1e07_english-No_Help.srt",
        8: "sabri_maranan_s1e08_english-Ill_Go_to_the_Forest.srt",
        9: "sabri_maranan_s1e09_english-A_Matter_of_Five_Minutes.srt",
        10: "sabri_maranan_s1e10_english-Early_Wedding.srt",
        11: "sabri_maranan_s1e11_english-Lice.srt",
        12: "sabri_maranan_s1e12_english-On_the_Head_of_the_Year.srt",
        13: "sabri_maranan_s1e13_english-Painting.srt",
        14: "sabri_maranan_s1e14_english-Hasson_Towers.srt",
        15: "sabri_maranan_s1e15_english-Hammer_and_Nail.srt",
    }

    def extract_episode_number(self, filename):
        """
        Extract episode number from video filename

        Supports patterns like:
        - s1e12, S1E12
        - s01e12, S01E12
        - Season 1 Episode 12
        - sabri_maranan_s1e12_...
        - Sabri_Maranan_07_... (streaming URLs)
        - פרק 1 (Hebrew: "Episode 1")

        Args:
            filename: Video filename or path

        Returns:
            Episode number (int), or None if not found
        """
        # Get just the filename without path
        basename = os.path.basename(filename)
        basename_lower = basename.lower()
        filename_lower = filename.lower()

        # Pattern 1: s1e12 or s01e12
        match = re.search(r's0?1e(\d{1,2})', basename_lower)
        if match:
            return int(match.group(1))

        # Pattern 2: episode 12, ep12, e12
        match = re.search(r'ep(?:isode)?\s*(\d{1,2})', basename_lower)
        if match:
            return int(match.group(1))

        # Pattern 3: season 1 episode 12
        match = re.search(r'season\s+1.*episode\s+(\d{1,2})', basename_lower)
        if match:
            return int(match.group(1))

        # Pattern 4: Sabri_Maranan_XX_ (streaming URLs like Sabri_Maranan_07_090911_...)
        match = re.search(r'sabri_maranan_(\d{1,2})_', filename_lower)
        if match:
            return int(match.group(1))

        # Pattern 5: Hebrew "פרק X" (episode X)
        # Matches Hebrew character פרק followed by whitespace and digits
        match = re.search(r'פרק\s*(\d{1,2})', basename)
        if match:
            return int(match.group(1))

        return None

    def get_subtitle_filename(self, episode_num):
        """
        Get the subtitle filename for an episode

        Args:
            episode_num: Episode number (1-42)

        Returns:
            Subtitle filename, or a generated name if not in mapping
        """
        if episode_num in self.SUBTITLE_PATTERNS:
            return self.SUBTITLE_PATTERNS[episode_num]

        # Generate filename for episodes not yet in mapping
        # This will be used for future episodes
        return f"sabri_maranan_s1e{episode_num:02d}_english-Episode_{episode_num}.srt"

    def is_sabri_maranan(self, filename):
        """Check if filename appears to be a Sabri Maranan episode"""
        # For URLs, check the full string; for local files, check the basename
        basename = os.path.basename(filename)
        basename_lower = basename.lower()
        filename_lower = filename.lower()

        # Check for English names (works for both URLs and file paths)
        if 'sabri' in filename_lower or 'maranan' in filename_lower:
            return True

        # Check for Hebrew episodes (פרק = episode in Hebrew)
        # Filename pattern: פרק X * DATE - TITLE
        # Works for both URLs and file paths
        if 'פרק' in filename and re.search(r'פרק\s*(\d{1,2})', filename):
            return True

        return False
