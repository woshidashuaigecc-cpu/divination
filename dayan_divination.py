#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from trigrams import Trigrams


class DayanDivination:
    def __init__(self):
        self.trigrams = Trigrams()

    def divine(self):
        lines = []
        for _ in range(6):
            line = self.get_line()
            lines.append(line)

        binary_original = ''.join(['1' if l in [7, 9] else '0' for l in lines])
        changing_lines = []
        for i in range(6):
            if lines[i] in [6, 9]:
                changing_lines.append(6 - i)

        original_hexagram = self.trigrams.get_hexagram(binary_original)

        changed_hexagram = None
        if changing_lines:
            binary_changed = binary_original
            for line_num in changing_lines:
                binary_changed = self.trigrams.change_line(binary_changed, line_num)
            changed_hexagram = self.trigrams.get_hexagram(binary_changed)

        return {
            'original': original_hexagram,
            'changing_lines': changing_lines,
            'changed': changed_hexagram
        }

    def get_line(self):
        total = 49
        
        for _ in range(3):
            total = self.perform_change(total)
        
        return total // 4

    def perform_change(self, total):
        left = random.randint(1, total - 1)
        right = total - left
        
        right -= 1
        if right < 1:
            right += 4
        
        remainder_left = left % 4
        if remainder_left == 0:
            remainder_left = 4
        
        remainder_right = right % 4
        if remainder_right == 0:
            remainder_right = 4
        
        return total - remainder_left - remainder_right - 1
