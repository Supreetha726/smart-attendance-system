# utils.py
marked_today = {}

def is_already_marked(name):
    from datetime import date
    
    today = str(date.today())
    
    if name in marked_today and marked_today[name] == today:
        return True
    
    marked_today[name] = today
    return False