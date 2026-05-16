#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
import random
import os

def register_chinese_font():
    font_paths = [
        r'C:\Windows\Fonts\msyh.ttc',
        r'C:\Windows\Fonts\simhei.ttf',
        r'C:\Windows\Fonts\simsun.ttc',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name='ChineseFont', fn_regular=font_path)
                return 'ChineseFont'
            except:
                continue
    return None

chinese_font = register_chinese_font()

from trigrams import Trigrams
from dayan_divination import DayanDivination
from number_divination import NumberDivination


class StickDragWidget(Widget):
    def __init__(self, total_sticks, **kwargs):
        super().__init__(**kwargs)
        self.total_sticks = total_sticks
        self.split_index = total_sticks // 2
        self.is_splitting = False
        self.stick_width = 8
        self.spacing = 4
        self.bind(size=self.update_sticks)
        self.bind(pos=self.update_sticks)
        self.update_sticks()

    def update_sticks(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.8, 0.8, 0.8, 1)
            Rectangle(pos=self.pos, size=self.size)

            stick_height = 60
            start_x = self.x + 5  # 最小左边距
            start_y = self.y + self.height / 2 - stick_height / 2
            
            # 动态计算竹签宽度和间距，确保完整显示
            available_width = self.width - 10  # 最小总边距
            if self.total_sticks > 0:
                # 间距固定为1或2像素，竹签宽度自适应
                self.spacing = 1 if self.total_sticks > 40 else 2
                # 竹签宽度 = (可用宽度 - 间距总和) / 竹签数
                spacing_total = self.spacing * (self.total_sticks - 1)
                self.stick_width = max(1, int((available_width - spacing_total) / self.total_sticks))
            else:
                self.stick_width = 8
                self.spacing = 4

            for i in range(self.total_sticks):
                if i < self.split_index:
                    Color(0.2, 0.6, 0.9, 1)
                else:
                    Color(0.9, 0.4, 0.2, 1)

                x = start_x + i * (self.stick_width + self.spacing)
                Rectangle(pos=(x, start_y), size=(self.stick_width, stick_height))

            if self.total_sticks > 0:
                Color(0.3, 0.3, 0.3, 1)
                split_x = start_x + self.split_index * (self.stick_width + self.spacing) + self.stick_width / 2
                Rectangle(pos=(split_x - 1, start_y - 10), size=(2, stick_height + 20))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.is_splitting = True
            self.update_split_index(touch.x)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.is_splitting and self.collide_point(*touch.pos):
            self.update_split_index(touch.x)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.is_splitting:
            self.is_splitting = False
            return True
        return super().on_touch_up(touch)

    def update_split_index(self, x):
        start_x = self.x + 5
        relative_x = x - start_x

        if relative_x < 0:
            self.split_index = 0
        else:
            # 根据触摸位置和竹签宽度计算索引
            index = int(relative_x / (self.stick_width + self.spacing))
            # 确保不超过范围
            self.split_index = max(0, min(index, self.total_sticks - 1))

        self.update_sticks()


class DivinationApp(App):
    def build(self):
        Window.size = (360, 640)
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(DayanScreen(name='dayan'))
        self.sm.add_widget(NumberScreen(name='number'))
        return self.sm


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(text='占卜起卦', font_size=30, size_hint_y=None, height=60, font_name=chinese_font)
        layout.add_widget(title)

        btn_dayan = Button(text='大衍起卦', font_size=20, size_hint_y=None, height=60, font_name=chinese_font)
        btn_dayan.bind(on_press=self.show_dayan)
        layout.add_widget(btn_dayan)

        btn_number = Button(text='数字起卦', font_size=20, size_hint_y=None, height=60, font_name=chinese_font)
        btn_number.bind(on_press=self.show_number)
        layout.add_widget(btn_number)
        
        self.add_widget(layout)

    def show_dayan(self, instance):
        self.manager.current = 'dayan'

    def show_number(self, instance):
        self.manager.current = 'number'


class DayanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reset_game()
        self.build_ui()

    def reset_game(self):
        self.line_index = 0
        self.change_index = 0
        self.total = 49
        self.lines = []
        self.history = []
        self.game_started = False
        self.game_finished = False

    def build_ui(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text='大衍起卦', font_size=24, size_hint_y=None, height=40, font_name=chinese_font)
        layout.add_widget(title)

        self.status_label = Label(text='点击开始，然后拖动分割线分草', font_size=14, size_hint_y=None, height=50, font_name=chinese_font)
        layout.add_widget(self.status_label)

        self.count_label = Label(text='', font_size=18, size_hint_y=None, height=30, font_name=chinese_font)
        layout.add_widget(self.count_label)

        self.stick_widget = StickDragWidget(self.total, size_hint_y=None, height=100)
        layout.add_widget(self.stick_widget)

        self.scroll_view = ScrollView(size_hint=(1, 0.45))
        self.history_text = Label(text='', font_size=12, size_hint_y=None, font_name=chinese_font)
        self.history_text.bind(texture_size=self.history_text.setter('size'))
        self.scroll_view.add_widget(self.history_text)
        layout.add_widget(self.scroll_view)

        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        self.btn_start = Button(text='开始', font_size=18, font_name=chinese_font)
        self.btn_start.bind(on_press=self.start_game)
        btn_layout.add_widget(self.btn_start)

        self.btn_confirm = Button(text='确认分草', font_size=18, font_name=chinese_font)
        self.btn_confirm.bind(on_press=self.split_sticks)
        self.btn_confirm.disabled = True
        btn_layout.add_widget(self.btn_confirm)

        self.btn_reset = Button(text='重置', font_size=18, font_name=chinese_font)
        self.btn_reset.bind(on_press=self.reset_game_ui)
        btn_layout.add_widget(self.btn_reset)

        layout.add_widget(btn_layout)

        btn_back = Button(text='返回', font_size=16, size_hint_y=None, height=50, font_name=chinese_font)
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)

    def reset_game_ui(self, instance=None):
        self.reset_game()
        self.build_ui()

    def start_game(self, instance):
        self.game_started = True
        self.btn_start.disabled = True
        self.btn_confirm.disabled = False
        self.update_display()

    def split_sticks(self, instance):
        if not self.game_started or self.game_finished:
            return

        left = self.stick_widget.split_index
        right = self.total - left

        right -= 1
        if right < 1:
            right += 4

        remainder_left = left % 4
        if remainder_left == 0:
            remainder_left = 4

        remainder_right = right % 4
        if remainder_right == 0:
            remainder_right = 4

        remainder_total = remainder_left + remainder_right
        new_total = self.total - remainder_total - 1

        self.history.append(f'第{self.line_index + 1}爻 - 第{self.change_index + 1}变：')
        self.history.append(f'  总数：{self.total}根 → 分为 {left} | {right + 1}')
        self.history.append(f'  余数：{remainder_left} + {remainder_right} = {remainder_total}，挂1，共去掉{remainder_total + 1}根')
        self.history.append(f'  剩余：{new_total}根\n')

        self.total = new_total
        self.change_index += 1

        if self.change_index == 3:
            line_number = self.total // 4
            line_type = ''
            if line_number == 6:
                line_type = '老阴 (×)'
            elif line_number == 7:
                line_type = '少阳 (—)'
            elif line_number == 8:
                line_type = '少阴 (- -)'
            elif line_number == 9:
                line_type = '老阳 (○)'

            self.lines.append(line_number)
            self.history.append(f'★ 第{self.line_index + 1}爻得出：{line_number} → {line_type}\n')

            self.line_index += 1
            self.change_index = 0
            self.total = 49

            if self.line_index == 6:
                self.finish_game()

        self.stick_widget.total_sticks = self.total
        self.stick_widget.split_index = self.total // 2
        self.stick_widget.update_sticks()
        self.update_display()

    def update_display(self):
        if not self.game_started:
            self.status_label.text = '点击开始，然后拖动分割线分草'
            self.count_label.text = ''
        elif self.game_finished:
            self.status_label.text = '起卦完成！'
            self.count_label.text = ''
        else:
            self.status_label.text = f'第{self.line_index + 1}爻 - 第{self.change_index + 1}变'
            left = self.stick_widget.split_index
            self.count_label.text = f'左堆：{left}  |  右堆：{self.total - left}  |  共{self.total}根'

        self.history_text.text = '\n'.join(self.history)

    def finish_game(self):
        self.game_finished = True
        self.btn_confirm.disabled = True

        binary_original = ''.join(['1' if l in [7, 9] else '0' for l in self.lines])
        changing_lines = []
        for i in range(6):
            if self.lines[i] in [6, 9]:
                changing_lines.append(6 - i)

        trigrams = Trigrams()
        original_hexagram = trigrams.get_hexagram(binary_original)

        changed_hexagram = None
        if changing_lines:
            binary_changed = binary_original
            for line_num in changing_lines:
                binary_changed = trigrams.change_line(binary_changed, line_num)
            changed_hexagram = trigrams.get_hexagram(binary_changed)

        result_text = '\n【起卦结果】\n'
        result_text += f'本卦：{original_hexagram["name"]}\n'
        result_text += f'{original_hexagram["symbol"]}\n\n'

        if changing_lines:
            result_text += '动爻：' + ', '.join([f'第{l}爻' for l in changing_lines]) + '\n'
            if changed_hexagram:
                result_text += f'之卦：{changed_hexagram["name"]}\n'
                result_text += f'{changed_hexagram["symbol"]}\n'

        self.history.append(result_text)
        self.update_display()

    def go_back(self, instance):
        self.manager.current = 'main'


class NumberScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(text='数字起卦', font_size=26, size_hint_y=None, height=50, font_name=chinese_font)
        layout.add_widget(title)

        # 添加提示标签
        hint_label = Label(text='请输入三个1-999之间的数字', font_size=14, size_hint_y=None, height=30, font_name=chinese_font, color=(0.6, 0.6, 0.6, 1))
        layout.add_widget(hint_label)

        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        self.input1 = TextInput(hint_text='1-999', font_size=16, input_filter='int', multiline=False, font_name=chinese_font)
        self.input1.bind(text=self.on_input_change)
        input_layout.add_widget(self.input1)
        
        self.input2 = TextInput(hint_text='1-999', font_size=16, input_filter='int', multiline=False, font_name=chinese_font)
        self.input2.bind(text=self.on_input_change)
        input_layout.add_widget(self.input2)
        
        self.input3 = TextInput(hint_text='1-999', font_size=16, input_filter='int', multiline=False, font_name=chinese_font)
        self.input3.bind(text=self.on_input_change)
        input_layout.add_widget(self.input3)
        
        layout.add_widget(input_layout)

        self.result_label = Label(text='输入三个数字后点击起卦', font_size=16, size_hint_y=None, height=80, font_name=chinese_font)
        layout.add_widget(self.result_label)

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.result_text = Label(text='', font_size=14, size_hint_y=None, font_name=chinese_font)
        self.result_text.bind(texture_size=self.result_text.setter('size'))
        self.scroll_view.add_widget(self.result_text)
        layout.add_widget(self.scroll_view)

        btn_divine = Button(text='开始起卦', font_size=20, size_hint_y=None, height=60, font_name=chinese_font)
        btn_divine.bind(on_press=self.do_divination)
        layout.add_widget(btn_divine)

        btn_back = Button(text='返回', font_size=16, size_hint_y=None, height=50, font_name=chinese_font)
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)

    def on_input_change(self, instance, value):
        # 限制每个输入框最多只能输入3位数字
        if len(value) > 3:
            instance.text = value[:3]

    def do_divination(self, instance):
        try:
            num1 = int(self.input1.text) if self.input1.text else 0
            num2 = int(self.input2.text) if self.input2.text else 0
            num3 = int(self.input3.text) if self.input3.text else 0
            
            # 检查是否输入了数字且在1-999之间
            if num1 == 0 or num2 == 0 or num3 == 0:
                self.result_label.text = '请输入三个1-999的数字'
                return
            
            if num1 > 999 or num2 > 999 or num3 > 999:
                self.result_label.text = '数字必须在1-999之间'
                return
            
            number_div = NumberDivination()
            result = number_div.divine(num1, num2, num3)
            self.result_label.text = '起卦完成！'
            self.result_text.text = self.format_result(result)
        except ValueError:
            self.result_label.text = '请输入有效的数字'

    def format_result(self, result):
        text = '【本卦】\n'
        text += f'卦名：{result["original"]["name"]}\n'
        text += f'卦象：\n{result["original"]["symbol"]}\n\n'
        
        text += '【动爻】\n'
        text += f'第 {result["changing_line"]} 爻变\n'
        
        text += '\n【之卦】\n'
        text += f'卦名：{result["changed"]["name"]}\n'
        text += f'卦象：\n{result["changed"]["symbol"]}\n'
        
        return text

    def go_back(self, instance):
        self.manager.current = 'main'


if __name__ == '__main__':
    DivinationApp().run()
