import re

def format_pics(html):
    pattern=re.compile(r'(\w+\.)(jpg|jpeg|png|gif)')
    text=pattern.sub(r'<img src="static/upload/\1\2">',text)

def markup_to_html(text):
    #image
    pattern=re.compile(r'\*img\*(\w+\.)(jpg|jpeg|png|gif)\*\*')
    text=pattern.sub(r'<img src="static/upload/\1\2">',text)
    #linebreak
    text=re.sub(r'\n','<br>',text)
    #others
    pattern=re.compile(r'\*(\w+)\*([^*]*)\*\*')
    text=pattern.sub(r'<\1>\2</\1>',text)
    return text

