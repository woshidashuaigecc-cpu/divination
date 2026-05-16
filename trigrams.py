#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Trigrams:
    EIGHT_TRIGRAMS = {
        'qian': {'name': '乾', 'symbol': '☰', 'binary': '111', 'nature': '天'},
        'dui': {'name': '兑', 'symbol': '☱', 'binary': '110', 'nature': '泽'},
        'li': {'name': '离', 'symbol': '☲', 'binary': '101', 'nature': '火'},
        'zhen': {'name': '震', 'symbol': '☳', 'binary': '100', 'nature': '雷'},
        'xun': {'name': '巽', 'symbol': '☴', 'binary': '011', 'nature': '风'},
        'kan': {'name': '坎', 'symbol': '☵', 'binary': '010', 'nature': '水'},
        'gen': {'name': '艮', 'symbol': '☶', 'binary': '001', 'nature': '山'},
        'kun': {'name': '坤', 'symbol': '☷', 'binary': '000', 'nature': '地'}
    }

    SIXTY_FOUR_HEXAGRAMS = {
        '111111': {'name': '乾为天', 'upper': 'qian', 'lower': 'qian'},
        '111110': {'name': '天泽履', 'upper': 'qian', 'lower': 'dui'},
        '111101': {'name': '天火同人', 'upper': 'qian', 'lower': 'li'},
        '111100': {'name': '天雷无妄', 'upper': 'qian', 'lower': 'zhen'},
        '111011': {'name': '天风姤', 'upper': 'qian', 'lower': 'xun'},
        '111010': {'name': '天水讼', 'upper': 'qian', 'lower': 'kan'},
        '111001': {'name': '天山遁', 'upper': 'qian', 'lower': 'gen'},
        '111000': {'name': '天地否', 'upper': 'qian', 'lower': 'kun'},
        '110111': {'name': '泽天夬', 'upper': 'dui', 'lower': 'qian'},
        '110110': {'name': '兑为泽', 'upper': 'dui', 'lower': 'dui'},
        '110101': {'name': '泽火革', 'upper': 'dui', 'lower': 'li'},
        '110100': {'name': '泽雷随', 'upper': 'dui', 'lower': 'zhen'},
        '110011': {'name': '泽风大过', 'upper': 'dui', 'lower': 'xun'},
        '110010': {'name': '泽水困', 'upper': 'dui', 'lower': 'kan'},
        '110001': {'name': '泽山咸', 'upper': 'dui', 'lower': 'gen'},
        '110000': {'name': '泽地萃', 'upper': 'dui', 'lower': 'kun'},
        '101111': {'name': '火天大有', 'upper': 'li', 'lower': 'qian'},
        '101110': {'name': '火泽睽', 'upper': 'li', 'lower': 'dui'},
        '101101': {'name': '离为火', 'upper': 'li', 'lower': 'li'},
        '101100': {'name': '火雷噬嗑', 'upper': 'li', 'lower': 'zhen'},
        '101011': {'name': '火风鼎', 'upper': 'li', 'lower': 'xun'},
        '101010': {'name': '火水未济', 'upper': 'li', 'lower': 'kan'},
        '101001': {'name': '火山旅', 'upper': 'li', 'lower': 'gen'},
        '101000': {'name': '火地晋', 'upper': 'li', 'lower': 'kun'},
        '100111': {'name': '雷天大壮', 'upper': 'zhen', 'lower': 'qian'},
        '100110': {'name': '雷泽归妹', 'upper': 'zhen', 'lower': 'dui'},
        '100101': {'name': '雷火丰', 'upper': 'zhen', 'lower': 'li'},
        '100100': {'name': '震为雷', 'upper': 'zhen', 'lower': 'zhen'},
        '100011': {'name': '雷风恒', 'upper': 'zhen', 'lower': 'xun'},
        '100010': {'name': '雷水解', 'upper': 'zhen', 'lower': 'kan'},
        '100001': {'name': '雷山小过', 'upper': 'zhen', 'lower': 'gen'},
        '100000': {'name': '雷地豫', 'upper': 'zhen', 'lower': 'kun'},
        '011111': {'name': '风天小畜', 'upper': 'xun', 'lower': 'qian'},
        '011110': {'name': '风泽中孚', 'upper': 'xun', 'lower': 'dui'},
        '011101': {'name': '风火家人', 'upper': 'xun', 'lower': 'li'},
        '011100': {'name': '风雷益', 'upper': 'xun', 'lower': 'zhen'},
        '011011': {'name': '巽为风', 'upper': 'xun', 'lower': 'xun'},
        '011010': {'name': '风水涣', 'upper': 'xun', 'lower': 'kan'},
        '011001': {'name': '风山渐', 'upper': 'xun', 'lower': 'gen'},
        '011000': {'name': '风地观', 'upper': 'xun', 'lower': 'kun'},
        '010111': {'name': '水天需', 'upper': 'kan', 'lower': 'qian'},
        '010110': {'name': '水泽节', 'upper': 'kan', 'lower': 'dui'},
        '010101': {'name': '水火既济', 'upper': 'kan', 'lower': 'li'},
        '010100': {'name': '水雷屯', 'upper': 'kan', 'lower': 'zhen'},
        '010011': {'name': '水风井', 'upper': 'kan', 'lower': 'xun'},
        '010010': {'name': '坎为水', 'upper': 'kan', 'lower': 'kan'},
        '010001': {'name': '水山蹇', 'upper': 'kan', 'lower': 'gen'},
        '010000': {'name': '水地比', 'upper': 'kan', 'lower': 'kun'},
        '001111': {'name': '山天大畜', 'upper': 'gen', 'lower': 'qian'},
        '001110': {'name': '山泽损', 'upper': 'gen', 'lower': 'dui'},
        '001101': {'name': '山火贲', 'upper': 'gen', 'lower': 'li'},
        '001100': {'name': '山雷颐', 'upper': 'gen', 'lower': 'zhen'},
        '001011': {'name': '山风蛊', 'upper': 'gen', 'lower': 'xun'},
        '001010': {'name': '山水蒙', 'upper': 'gen', 'lower': 'kan'},
        '001001': {'name': '艮为山', 'upper': 'gen', 'lower': 'gen'},
        '001000': {'name': '山地剥', 'upper': 'gen', 'lower': 'kun'},
        '000111': {'name': '地天泰', 'upper': 'kun', 'lower': 'qian'},
        '000110': {'name': '地泽临', 'upper': 'kun', 'lower': 'dui'},
        '000101': {'name': '地火明夷', 'upper': 'kun', 'lower': 'li'},
        '000100': {'name': '地雷复', 'upper': 'kun', 'lower': 'zhen'},
        '000011': {'name': '地风升', 'upper': 'kun', 'lower': 'xun'},
        '000010': {'name': '地水师', 'upper': 'kun', 'lower': 'kan'},
        '000001': {'name': '地山谦', 'upper': 'kun', 'lower': 'gen'},
        '000000': {'name': '坤为地', 'upper': 'kun', 'lower': 'kun'}
    }

    @classmethod
    def get_hexagram(cls, binary_str):
        if binary_str in cls.SIXTY_FOUR_HEXAGRAMS:
            hexagram = cls.SIXTY_FOUR_HEXAGRAMS[binary_str]
            symbol = cls.generate_hexagram_symbol(binary_str)
            return {
                'name': hexagram['name'],
                'binary': binary_str,
                'symbol': symbol
            }
        return None

    @classmethod
    def generate_hexagram_symbol(cls, binary_str):
        lines = []
        for bit in binary_str:
            if bit == '1':
                lines.append('━━━')
            else:
                lines.append('━ ━')
        return '\n'.join(reversed(lines))

    @classmethod
    def change_line(cls, binary_str, line_num):
        bits = list(binary_str)
        idx = 5 - (line_num - 1)
        bits[idx] = '1' if bits[idx] == '0' else '0'
        return ''.join(bits)
