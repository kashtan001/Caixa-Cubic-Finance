#!/usr/bin/env python3
"""
HTML Minifier - сжимает читаемые LOOK_*.html файлы обратно в рабочий формат
"""
import re
import sys
import os
import glob

def minify_html(input_file):
    """Сжимает HTML в одну строку"""
    print(f"📄 Сжимаю: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Убираем переносы строк между тегами
        html = re.sub(r'>\s+<', '><', html)
        
        # Убираем лишние пробелы и переносы внутри тегов
        html = re.sub(r'\s+', ' ', html)
        
        # Убираем пробелы в начале и конце
        html = html.strip()
        
        # Определяем имя выходного файла (убираем префикс LOOK_)
        base_name = os.path.basename(input_file)
        if base_name.startswith("LOOK_"):
            output_file = base_name[5:]  # Убираем "LOOK_"
        else:
            output_file = base_name.replace('_readable', '')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Сжат в рабочий файл: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"❌ Ошибка сжатия {input_file}: {e}")
        return None

def main():
    """Обрабатывает все LOOK_*.html файлы в текущей директории"""
    look_files = glob.glob("LOOK_*.html")
    
    if not look_files:
        print("❌ LOOK_*.html файлы не найдены")
        print("💡 Сначала запусти: python html_beautifier.py")
        return
    
    print(f"🔍 Найдено LOOK_ файлов: {len(look_files)}")
    print(f"📋 Файлы: {', '.join(look_files)}")
    print()
    
    processed = 0
    for look_file in look_files:
        result = minify_html(look_file)
        if result:
            processed += 1
    
    print()
    print(f"✅ Сжато файлов: {processed}/{len(look_files)}")
    print("🎯 Рабочие HTML файлы обновлены и готовы для PDF конструктора")

if __name__ == '__main__':
    main()
