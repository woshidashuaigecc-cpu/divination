#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from trigrams import Trigrams


class NumberDivination:
    def __init__(self):
        self.trigrams = Trigrams()
        self.eight_trigrams_list = ['kun', 'gen', 'kan', 'xun', 'zhen', 'li', 'dui', 'qian']

    def divine(self, num1, num2, num3):
        upper_idx = (num1 - 1) % 8
        lower_idx = (num2 - 1) % 8
        
        upper_trigram = self.eight_trigrams_list[upper_idx]
        lower_trigram = self.eight_trigrams_list[lower_idx]
        
        binary_upper = self.trigrams.EIGHT_TRIGRAMS[upper_trigram]['binary']
        binary_lower = self.trigrams.EIGHT_TRIGRAMS[lower_trigram]['binary']
        binary_original = binary_upper + binary_lower
        
        changing_line = num3 % 6
        if changing_line == 0:
            changing_line = 6
        
        original_hexagram = self.trigrams.get_hexagram(binary_original)
        
        binary_changed = self.trigrams.change_line(binary_original, changing_line)
        changed_hexagram = self.trigrams.get_hexagram(binary_changed)
        
        return {
            'original': original_hexagram,
            'changing_line': changing_line,
            'changed': changed_hexagram
        }
