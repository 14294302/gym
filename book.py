import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import webbrowser
chinese_weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
state = ['<span class="time-slot closed">','<span class="time-slot fulled">','<span class="time-slot booked">']
time = ["10:30-12:00", "12:00-13:30", "13:30-15:00", "15:00-16:30", "16:30-18:00", "18:00-19:30", "19:30-21:00"]

def get_date_list():
    today = datetime.now().date()
    datelist = []
    for i in range(7):
        date = today + timedelta(days=i)
        weekday_index = date.weekday()
        chinese_weekday = chinese_weekdays[weekday_index]
        formatted_date = date.strftime('%Y-%m-%d') + f' ({chinese_weekday})'
        datelist.append(formatted_date)
    return datelist

def html_fragment(date,booktime):
    html_code = '<li class="slot"><span class="date-info">'+date+'</span><div class="clearfix hidden-lg"></div>\n'
    if booktime is None:
        for i in range(7):
            html_code += '\t'+state[1]+'<span>'+time[i]+'</span></span>\n'
    else:
        for i in range(7):
            if booktime == time[i]:
                html_code += '\t'+state[2]+'<span>'+time[i]+'</span></span>\n'
            else:
                html_code += '\t'+state[1]+'<span>'+time[i]+'</span></span>\n'
    html_code += '\t</li><div class="clearfix"></div>\n'
    return html_code

def thursday(date):
    html_code = '<li class="slot"><span class="date-info">'+date+'</span><div class="clearfix hidden-lg"></div>\n'
    html_code += '\t'+state[0]+'<span>'+time[0]+'</span></span>\n'
    html_code += '\t'+state[1]+'<span>'+time[1]+'</span></span>\n'
    html_code += '\t'+state[0]+'<span>'+time[2]+'</span></span>\n'
    html_code += '\t'+state[0]+'<span>'+time[3]+'</span></span>\n'
    html_code += '\t'+state[0]+'<span>'+time[4]+'</span></span>\n'
    html_code += '\t'+state[0]+'<span>'+time[5]+'</span></span>\n'
    html_code += '\t'+state[0]+'<span>'+time[6]+'</span></span>\n'
    html_code += '\t</li><div class="clearfix"></div>\n'
    return html_code

def htmlcode(selected_time):
    datelist = get_date_list()
    code = html_fragment(datelist[0],selected_time)
    for i in range(6):
        if datelist[i+1][12:15] == '星期四':
            code += thursday(datelist[i+1])
        else:
            code += html_fragment(datelist[i+1],None)
    return code

def insert_html(original_file, new_content):
    with open(original_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines.insert(108, new_content + '\n')
    return ''.join(lines)

def save_web():
    selected_time = selected.get()
    code = htmlcode(selected_time)
    new_content = code
    modified_html = insert_html("健身房预约 _ 翔安校区体育馆预约系统.html", new_content)
    with open("fakeweb.html", "w", encoding="utf-8") as file:
        file.write(modified_html)
    webbrowser.open("fakeweb.html")
    root.destroy()

root = tk.Tk()
root.title("健身房造假")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 400
window_height = 200
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

selected = tk.StringVar()
selected.set("选择时间")
dropdown_style = ttk.Style()
dropdown_style.configure("Dropdown.TCombobox", font=("Arial", 12))
dropdown = ttk.Combobox(root, textvariable=selected, values=time, style="Dropdown.TCombobox")
dropdown.pack(pady=40)

save_button = tk.Button(root, text="生成网页", command=save_web, width=15, height=1, borderwidth=2, relief="solid")
save_button.pack()

root.mainloop()
