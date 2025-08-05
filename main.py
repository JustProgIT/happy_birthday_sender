from flask import Flask, request, render_template, redirect, url_for
import datetime
import sendmail
import json
from PIL import Image, ImageDraw, ImageFont
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

months_list = {
    "1":"января",
    "2":"февраля",
    "3":"марта",
    "4":"апреля",
    "5":"мая",
    "6":"июня",
    "7":"июля" ,
    "8":"августа ",
    "9":"сентября",
    "10":"октября",
    "11":"ноября",
    "12":"декабря",
}

global data

font1 = ImageFont.truetype("fonts\\DancingScript-VariableFont_wght.ttf", 250)
font2 = ImageFont.truetype("fonts\\ArialMT.ttf", 50)
font3 = ImageFont.truetype("fonts\\Arial-BoldMT.ttf", 50)
font4 = ImageFont.truetype("fonts\\Caveat-SemiBold.ttf", 180)

@app.route('/')
def index():
    return render_template('admin_index.html')

@app.post("/api/birthday")
def publicData():
    time_now = datetime.datetime.now()
    time_day = time_now.strftime("%d")
    time_month = time_now.strftime("%m")
    name_moth = months_list[time_month]
    data = request.json["data"]
    name = ""
    dep = ""
    range = ""
    lines = []
    for d in data:
        list1 = {
            'name':  d["name"],
            'range': d["range"],
            'department': d["department"],
        }
        lines.append(list1)
        name += d["name"] + " \n" + d["range"] + " " + d["department"] + "\n"
        dep += d["range"] + "\n"
        range += d["department"] + "\n"

    try:
        with open('status.txt', 'r') as status_file:
            status_content = status_file.read().strip()
    except FileNotFoundError:
        print("Error: status.txt not found.")
        status_content = None

    if status_content == '0':
        try:
            with open('info.txt', 'w', encoding="utf-8") as info_file:
                for line in lines:
                    json.dump(line, info_file, ensure_ascii=False)
                    info_file.write('\n')
                    #info_file.write(str(line) + '\n')
                    #info_file.write(str(line) + '\n')
            print("Lines written to info.txt.")
            with open('status.txt', 'w', encoding="utf-8") as status_file:
                status_file.write('1')
        except Exception as e:
            print(f"Error writing to info.txt: {e}")

    elif status_content == '1':
        print('status_content 1')
        try:
            with open('info1.txt', 'w', encoding="utf-8") as info_file:
                for line in lines:
                    json.dump(line, info_file, ensure_ascii=False)
                    info_file.write('\n')
                    #info_file.write(str(line) + '\n')
                    #info_file.write(str(line) + '\n')
            print("Lines written to info.txt.")
            with open('status.txt', 'w', encoding="utf-8") as status_file:
                status_file.write('2')
        except Exception as e:
            print(f"Error writing to info.txt: {e}")
        
    elif status_content == '2':
        print('status_content 2')
        with open('info.txt', 'r', encoding="utf-8") as info_file:
            content = info_file.readlines()
            for line in content:
                data = json.loads(line)
                list1 = {
                    'name':  data["name"],
                    'range': data["range"],
                    'department': data["department"],
                }
                if list1['name'] in content:
                    pass
                else:
                    lines.append(list1)
        with open('info1.txt', 'r', encoding="utf-8") as info_file:
            content = info_file.readlines()
            for line in content:
                data = json.loads(line)
                list1 = {
                    'name':  data["name"],
                    'range': data["range"],
                    'department': data["department"],
                }
                if list1['name'] in content:
                    pass
                else:
                    lines.append(list1)




        print('starting sending emails')
        coord_y = 0
        image_size = 0
        

        lines2 = []
        names_set = set()

        for i in lines:
            if i['name'] not in names_set:
                print(i)
                lines2.append(i)
                names_set.add(i['name'])

        # lines2 = [] 
        # for i in lines: 
        #     if i not in lines2: 
        #         print(i) 
        #         lines2.append(i)

        
        # [lines2.append(i) for i in lines if i not in lines2]

        image_size = 0

        for i in lines2:
            if i['department'] != "":
                image_size += 230
            else:
                image_size += 210
            image_size+=25

        imageMonth = Image.new('RGB', (1920, 300), 'white')
        draw_date = ImageDraw.Draw(imageMonth)
        draw_date.text((960-(len(time_day) * 170), -50), time_day, fill="#00008B", font=font1)
        draw_date.text((960-(len(name_moth) * 5), 45), name_moth, fill="#00008B", font=font4)
        imageMonth.save("im2.png")
        
        image = Image.new('RGB', (1920, image_size), 'white')
        draw = ImageDraw.Draw(image)
        a = 0
        for i in lines2:
            if a == 0:
                coord_x_name = (960 - (len(i['name']) * 14.5))
                coord_x_dep = (960 - (len(i['range']) * 14.5))
                coord_x_range = (960 - (len(i['department']) * 14.5))
                draw.text((coord_x_name, coord_y+5), i['name'], fill="#00008B", font=font2)
                draw.text((coord_x_dep, coord_y+65), i['range'], fill="#00008B", font=font3)
                draw.text((coord_x_range, coord_y+125), i['department'], fill="#00008B", font=font3)
                coord_y += 135
                a = 1
            else:
                coord_x_name = (960 - (len(i['name']) * 14.5))
                coord_x_dep = (960 - (len(i['range']) * 14.5))
                coord_x_range = (960 - (len(i['department']) * 14.5))
                draw.text((coord_x_name, coord_y + 100), i['name'], fill="#00008B", font=font2)
                draw.text((coord_x_dep, coord_y + 160), i['range'], fill="#00008B", font=font3)
                draw.text((coord_x_range, coord_y + 220), i['department'], fill="#00008B", font=font3)
                coord_y += 230

        image.save("im3.png")
            
        
        sendmail.send_message_finally()
        with open("status.txt", "w") as file:
            file.write("0")
        return 'emails sent'
            
    return 'ok'

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")
