#!/usr/bin/env python3
"""
HTML Beautifier - делает HTML шаблоны читаемыми для редактирования
Создает файлы с префиксом LOOK_ для просмотра и редактирования
+ Красивое форматирование CSS стилей по строкам
"""
from bs4 import BeautifulSoup
import sys
import os
import glob
import re

def format_css(css_content):
    """
    Форматирует CSS стили для лучшей читаемости
    Разбивает длинные CSS правила на строки
    """
    # Убираем лишние пробелы и переносы
    css_content = re.sub(r'\s+', ' ', css_content.strip())
    
    # Разбиваем CSS селекторы и правила
    formatted_css = ""
    
    # Находим все CSS правила вида .selector{property:value;property:value;}
    css_rules = re.findall(r'([^{}]+)\{([^{}]+)\}', css_content)
    
    for selector, properties in css_rules:
        selector = selector.strip()
        
        # Разбиваем свойства по точкам с запятой
        props = [prop.strip() for prop in properties.split(';') if prop.strip()]
        
        if len(props) <= 3:
            # Короткие правила оставляем в одну строку
            formatted_css += f"{selector} {{ {'; '.join(props)}; }}\n"
        else:
            # Длинные правила разбиваем по строкам
            formatted_css += f"{selector} {{\n"
            for prop in props:
                formatted_css += f"    {prop};\n"
            formatted_css += "}\n"
    
    # Если не удалось распарсить как правила, возвращаем построчно
    if not css_rules:
        # Разбиваем по точкам с запятой и делаем отступы
        parts = css_content.split(';')
        formatted_css = ""
        indent = 0
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            if '{' in part:
                formatted_css += "    " * indent + part + "\n"
                indent += 1
            elif '}' in part:
                indent = max(0, indent - 1)
                formatted_css += "    " * indent + part + "\n"
            else:
                formatted_css += "    " * indent + part + ";\n"
    
    return formatted_css

def beautify_html(input_file):
    """Делает HTML читаемым с красивым форматированием CSS"""
    print(f"📄 Обрабатываю: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Парсим HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Находим все <style> теги и форматируем CSS
        style_tags = soup.find_all('style')
        css_formatted_count = 0
        
        for style_tag in style_tags:
            if style_tag.string:
                original_css = style_tag.string
                formatted_css = format_css(original_css)
                style_tag.string = "\n" + formatted_css + "    "  # Добавляем отступы
                css_formatted_count += 1
        
        # Форматируем с отступами
        pretty_html = soup.prettify()
        
        # Создаем имя файла с префиксом LOOK_
        base_name = os.path.basename(input_file)
        output_file = f"LOOK_{base_name}"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_html)
        
        print(f"✅ Создан читаемый файл: {output_file}")
        if css_formatted_count > 0:
            print(f"🎨 Отформатировано CSS блоков: {css_formatted_count}")
        return output_file
        
    except Exception as e:
        print(f"❌ Ошибка обработки {input_file}: {e}")
        return None

def main():
    """Обрабатывает все HTML файлы в текущей директории"""
    html_files = glob.glob("*.html")
    
    # Исключаем уже обработанные файлы с префиксом LOOK_
    html_files = [f for f in html_files if not f.startswith("LOOK_")]
    
    if not html_files:
        print("❌ HTML файлы не найдены в текущей директории")
        return
    
    print(f"🔍 Найдено HTML файлов: {len(html_files)}")
    print(f"📋 Файлы: {', '.join(html_files)}")
    print()
    
    processed = 0
    for html_file in html_files:
        result = beautify_html(html_file)
        if result:
            processed += 1
    
    print()
    print(f"✅ Обработано файлов: {processed}/{len(html_files)}")
    print("🎯 Теперь можешь редактировать LOOK_*.html файлы")
    print("💡 CSS стили теперь красиво отформатированы по строкам!")

if __name__ == '__main__':
    main()
