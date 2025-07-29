from telethon import TelegramClient, events
from telethon.tl.custom import Button
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputUser
from telethon.errors import UserIdInvalidError, MessageNotModifiedError

import traceback
import os
import json
import shutil
import subprocess
from datetime import datetime, timedelta
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
import asyncio, random
from telethon.tl.functions.messages import ImportChatInviteRequest
import re



# إعدادات أساسية
BOT_TOKEN = "7666755138:AAFwjsfin3t8azTUedmv6Fz-48Y3ks_xMPc"
API_ID = 25676123
API_HASH = "bedc315cbd03df330cf4d97004469ee4"
ADMIN_ID = 7766123377
BOTS_DIR = "bots"
admin_pending_installs = {}
INFO_PATH = os.path.join(os.path.dirname(__file__), "information.json")
sessions_temp = {}
confirm_messages = {}

channels_to_join = [
"https://t.me/i_7_ii",
]






# ✅ دالة تشغيل البوت داخل screen بمدة
def run_bot_in_screen(user_id, user_folder, duration_seconds):
    screen_name = f"bot_{user_id}"
    hh_path = os.path.join(user_folder, "hh.py")
    cmd = f'screen -dmS {screen_name} bash -c "python3 {hh_path}; sleep {duration_seconds}; screen -S {screen_name} -X quit"'
    subprocess.call(cmd, shell=True)


def format_remaining_time(end_timestamp):
    if isinstance(end_timestamp, datetime):
        end_time = end_timestamp
    else:
        end_time = datetime.fromtimestamp(end_timestamp)
    
    now = datetime.now()
    remaining = end_time - now
    days = remaining.days
    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60

    return f"{days} يوم و {hours} ساعة و {minutes} دقيقة"




# تحميل الملف أو إنشاءه لو مش موجود
if os.path.exists(INFO_PATH):
    with open(INFO_PATH, "r") as f:
        all_data = json.load(f)
else:
    all_data = {}







# تأكد من وجود مجلد البوتات
os.makedirs(BOTS_DIR, exist_ok=True)

# حفظ المستخدمين المنتظرين للجلسة
pending_sessions = set()

# تشغيل البوت
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    if event.sender_id == ADMIN_ID:
        await event.respond(
            " مرحباً بك في لوحة التحكم الإدارية الخاصة بك، اختر من الأزرار التالية:",
            buttons=[
                [
                    Button.inline("➕ إضافة مدة", data=b"admin_add"),
                    Button.inline("➖ حذف مدة", data=b"admin_remove")
                ],
                [
                    Button.inline("تنصيب جديد", data=b"install_user"),
                    Button.inline("حذف تنصيب", data=b"unsinstall_user")
                ],
                [Button.inline("ℹ️ معلومات المستخدمين", data=b"admin_info")]
            ]
        )

    await event.respond(
        """**
 مرحباً بك
 لتنصيب السورس قم بالضغط على زر تسجيل ✦
 لطلب تنصيب اضغط على "طلب تنصيب"

 اختر من الأسفل:
        **""",
        buttons=[
            [Button.inline(" تسجيل | LoGiN", data=b"register")],
            [
                Button.inline(" طلب تنصيب", data=b"install"),
                Button.url("استخراج جلسه", url="https://telegram.tools/session-string-generator#telethon,user")
            ],
            [
                Button.url(" المطور", url="https://t.me/cc99q"),
                Button.url(" قناة السورس", url="https://t.me/vvu_vvv")
            ]
        ]
    )
    pending_sessions.discard(event.sender_id)


@bot.on(events.CallbackQuery(func=lambda e: e.data in [b"back_user", b"back_admin"]))
async def back_handler(event):
    if event.sender_id == ADMIN_ID and event.data == b"back_admin":
        await event.edit(
            "👑 مرحباً بك في لوحة التحكم الإدارية الخاصة بك، اختر من الأزرار التالية:",
            buttons=[
                [
                    Button.inline("➕ إضافة مدة", data=b"admin_add"),
                    Button.inline("➖ حذف مدة", data=b"admin_remove")
                ],
                [
                    Button.inline("تنصيب جديد", data=b"install_user"),
                    Button.inline("حذف تنصيب", data=b"unsinstall_user")
                ],
                [Button.inline("ℹ️ معلومات المستخدمين", data=b"admin_info")]
            ]
        )
        del admin_pending_installs[event.sender_id]

    if event.data == b"back_user":
        await event.edit(
            """**
 مرحباً بك 
 لتنصيب السورس قم بالضغط على زر تسجيل ✦
 لطلب تنصيب اضغط على "طلب تنصيب"

 اختر من الأسفل:
            **""",
            buttons=[
                [Button.inline(" تسجيل | LoGiN", data=b"register")],
                [
                    Button.inline(" طلب تنصيب", data=b"install"),
                    Button.url("استخراج جلسه", url="https://telegram.tools/session-string-generator#telethon,user")
                ],
                [
                    Button.url(" المطور", url="https://t.me/cc99q"),
                    Button.url(" قناة السورس", url="https://t.me/vvu_vvv")
                ]
            ]
        )
        pending_sessions.discard(event.sender_id)



@bot.on(events.CallbackQuery(data=b"install"))
async def handle_install_request(event):
    await event.edit(
        f"""**
⚙️ طلب تنصيب بوت جديد

مرحباً بك 👋  
هذا البوت يعمل بنظام الاشتراك المدفوع 💰، ويوفر لك المميزات التالية:

✅ سرعة عالية في التشغيل  
✅ استقرار دائم بدون توقف  
✅ دعم فني مباشر  
✅ تحديثات مستمرة ومجانية

 هل هذه أول مرة تستخدم البوت؟
نحن نوفر تجربة مجانية لمدة يوم واحد فقط ⏳

📩 للتواصل وطلب التنصيب، اضغط الزر بالأسفل 👇
**""",
        buttons=[
            [Button.url("💬 مراسلة المطور", url="https://t.me/cc99q")],
            [Button.inline("🔙 رجوع", data=b"back_user")]
        ],
        link_preview=False
    )



@bot.on(events.CallbackQuery(data=b"install_user"))
async def admin_start_install(event):
    if event.sender_id != ADMIN_ID:
        return
    admin_pending_installs[event.sender_id] = {"step": "awaiting_id"}
    await event.respond("📥 أرسل الآن آيدي المستخدم الذي تريد تنصيبه:", buttons=[Button.inline("🔙 رجوع", data=b"back_admin")])


# @bot.on(events.NewMessage(func=lambda e: e.sender_id in admin_pending_installs))
# async def admin_install_process(event):
#     admin_state = admin_pending_installs.get(event.sender_id)
#     information_file = "information.json"
#     if not admin_state:
#         return

#     # خطوة إدخال آيدي المستخدم
#     if admin_state["step"] == "awaiting_id":
#         try:
#             target_id = int(event.raw_text.strip())
#         except ValueError:
#             return await event.reply("❌ الآيدي غير صالح، أرسل آيدي صحيح.")

#         try:
#             full = await bot(GetFullUserRequest(target_id))
#             user = full.users[0]  # أو full.user لو متاح حسب إصدار telethon
#             full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
#             username = f"@{user.username}" if user.username else "لا يوجد"
#         except:
#             traceback_str = traceback.format_exc()  # يطبع الاستثناء كسلسلة
#             print("❌ حصل خطأ أثناء GetFullUserRequest:\n", traceback_str)
#             del admin_pending_installs[event.sender_id]
#             return await event.reply(
#                 "❌ لا يمكن العثور على هذا المستخدم.\n"
#                 "📌 تأكد أن المستخدم قد بدأ المحادثة مع البوت أولاً.",
#                 buttons=[Button.inline("🔙 رجوع", data=b"cancel_admin_action")]
#             )

#         admin_pending_installs[event.sender_id] = {"step": "awaiting_days", "target_id": target_id}
#         return await event.reply(
#             f"👤 معلومات المستخدم:\n"
#             f"🔹 الاسم: {full_name}\n"
#             f"🔹 اليوزر: {username}\n"
#             f"🔹 آيدي: `{target_id}`\n\n"
#             f"🗓️ أرسل الآن عدد أيام الاشتراك:",
#             buttons=[Button.inline("🔙 رجوع", data=b"cancel_admin_action")]
#         )

#     # خطوة إدخال عدد الأيام
#     elif admin_state["step"] == "awaiting_days":
#         try:
#             days = int(event.raw_text.strip())
#         except ValueError:
#             return await event.reply("❌ عدد الأيام غير صالح، أرسل رقم فقط.")

#         target_id = admin_state["target_id"]
#         start_time = datetime.now()
#         end_time = start_time + timedelta(days=days)

#         # 🟢 حفظ session.json للمستخدم
#         user_folder = os.path.join(BOTS_DIR, str(target_id))
#         os.makedirs(user_folder, exist_ok=True)
#         session_data = {
#             "api_id": API_ID,
#             "api_hash": API_HASH,
#             "start_time": int(start_time.timestamp()),
#             "end_time": int(end_time.timestamp())
#         }
#         with open(os.path.join(user_folder, "session.json"), "w") as f:
#             json.dump(session_data, f)

#         # 🟢 حفظ بيانات الاشتراك في ملف مشترك information.json
#         if os.path.exists(information_file):
#             with open(information_file, "r") as f:
#                 all_info = json.load(f)
#         else:
#             all_info = {}

#         all_info[str(target_id)] = {
#             "tybe": "اشتراك مدفوع",
#             "user_id": target_id,
#             "start_time": int(start_time.timestamp()),
#             "end_time": int(end_time.timestamp())
#         }

#         with open(information_file, "w") as f:
#             json.dump(all_info, f, indent=4)

#         # 📨 إرسال رسالة للمستخدم
#         try:
#             await bot.send_message(
#                 target_id,
#                 f"""🎉 تم تفعيل البوت لديك لمدة {days} أيام.
# ⌛ ينتهي اشتراكك في ⟶
# 🗓️ {end_time.strftime('%Y-%m-%d %H:%M')}
# ⚙️ يمكنك الآن تنصيب السورس"""
#             )
#         except:
#             await event.reply("⚠️ تم حفظ الاشتراك لكن لم أتمكن من إرسال رسالة للمستخدم.")

#         await event.reply(
#             f"✅ تم تفعيل الاشتراك للمستخدم `{target_id}` بنجاح لمدة {days} أيام.",
#             buttons=[Button.inline("🔙 رجوع", data=b"cancel_admin_action")]
#         )

#         del admin_pending_installs[event.sender_id]




@bot.on(events.CallbackQuery(data=b"unsinstall_user"))
async def admin_start_uninstall(event):
    if event.sender_id != ADMIN_ID:
        return
    admin_pending_installs[event.sender_id] = {"step": "awaiting_uninstall_id"}
    await event.respond(
        "🗑️ أرسل الآن آيدي المستخدم الذي تريد حذف اشتراكه:",
        buttons=[Button.inline("🔙 رجوع", data=b"cancel_admin_action")]
    )


# @bot.on(events.NewMessage(func=lambda e: e.sender_id in admin_pending_installs))
# async def admin_uninstall_process(event):
#     state = admin_pending_installs.get(event.sender_id)
#     if not state or state["step"] != "awaiting_uninstall_id":
#         return

#     try:
#         target_id = int(event.raw_text.strip())
#     except ValueError:
#         return await event.reply("❌ الآيدي غير صالح، أرسل رقم صحيح.")

#     info_file = "information.json"
#     user_folder = os.path.join(BOTS_DIR, str(target_id))

#     # تحميل معلومات الاشتراك
#     if not os.path.exists(info_file):
#         del admin_pending_installs[event.sender_id]
#         return await event.reply("⚠️ لا يوجد أي اشتراكات حالياً.")

#     with open(info_file, "r") as f:
#         all_info = json.load(f)

#     if str(target_id) not in all_info:
#         del admin_pending_installs[event.sender_id]
#         return await event.reply("❌ هذا المستخدم غير مشترك حالياً.")

#     # حذف المجلد إن وجد
#     if os.path.exists(user_folder):
#         try:
#             import shutil
#             shutil.rmtree(user_folder)
#         except Exception as e:
#             print("❌ خطأ أثناء حذف المجلد:", e)

#     # حذف بيانات المستخدم من الملف
#     del all_info[str(target_id)]
#     with open(info_file, "w") as f:
#         json.dump(all_info, f, indent=4)

#     # إرسال رسالة للمستخدم
#     try:
#         await bot.send_message(
#             target_id,
#             "⚠️ تم إلغاء اشتراكك من قبل المسؤول.\n"
#             "إذا كنت ترى أن هذا عن طريق الخطأ، تواصل مع الدعم."
#         )
#     except:
#         pass  # تجاهل الخطأ لو ما قدرش يوصله

#     await event.reply(
#         f"✅ تم حذف اشتراك المستخدم `{target_id}` بنجاح.",
#         buttons=[Button.inline("🔙 رجوع", data=b"cancel_admin_action")]
#     )

#     del admin_pending_installs[event.sender_id]



@bot.on(events.NewMessage(func=lambda e: e.sender_id in admin_pending_installs))
async def admin_process(event):
    state = admin_pending_installs.get(event.sender_id)

    information_file = "information.json"
    if not state:
        return

    # خطوة إدخال آيدي المستخدم
    if state["step"] == "awaiting_id":
        try:
            target_id = int(event.raw_text.strip())
        except ValueError:
            return await event.reply("❌ الآيدي غير صالح، أرسل آيدي صحيح.")

        try:
            full = await bot(GetFullUserRequest(target_id))
            user = full.users[0]  # أو full.user لو متاح حسب إصدار telethon
            full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
            username = f"@{user.username}" if user.username else "لا يوجد"
        except:
            traceback_str = traceback.format_exc()  # يطبع الاستثناء كسلسلة
            print("❌ حصل خطأ أثناء GetFullUserRequest:\n", traceback_str)
            del admin_pending_installs[event.sender_id]
            return await event.reply(
                "❌ لا يمكن العثور على هذا المستخدم.\n"
                "📌 تأكد أن المستخدم قد بدأ المحادثة مع البوت أولاً.",
                buttons=[Button.inline("🔙 رجوع", data=b"cancel_admin_action")]
            )

        admin_pending_installs[event.sender_id] = {"step": "awaiting_days", "target_id": target_id}
        return await event.reply(
            f"👤 معلومات المستخدم:\n"
            f"🔹 الاسم: {full_name}\n"
            f"🔹 اليوزر: {username}\n"
            f"🔹 آيدي: `{target_id}`\n\n"
            f"🗓️ أرسل الآن عدد أيام الاشتراك:",
            buttons=[Button.inline("🔙 رجوع", data=b"cancel_admin_action")]
        )

    # خطوة إدخال عدد الأيام
    elif state["step"] == "awaiting_days":
        try:
            days = int(event.raw_text.strip())
        except ValueError:
            return await event.reply("❌ عدد الأيام غير صالح، أرسل رقم فقط.")

        target_id = state["target_id"]
        start_time = datetime.now()
        end_time = start_time + timedelta(days=days)

        # 🟢 حفظ session.json للمستخدم
        user_folder = os.path.join(BOTS_DIR, str(target_id))
        os.makedirs(user_folder, exist_ok=True)
        session_data = {
            "api_id": API_ID,
            "api_hash": API_HASH,
            "start_time": int(start_time.timestamp()),
            "end_time": int(end_time.timestamp())
        }
        with open(os.path.join(user_folder, "session.json"), "w") as f:
            json.dump(session_data, f)

        # 🟢 حفظ بيانات الاشتراك في ملف مشترك information.json
        if os.path.exists(information_file):
            with open(information_file, "r") as f:
                all_info = json.load(f)
        else:
            all_info = {}

        all_info[str(target_id)] = {
            "tybe": "اشتراك مدفوع",
            "user_id": target_id,
            "start_time": int(start_time.timestamp()),
            "end_time": int(end_time.timestamp())
        }

        with open(information_file, "w") as f:
            json.dump(all_info, f, indent=4)

        # 📨 إرسال رسالة للمستخدم
        try:
            await bot.send_message(
                target_id,
                f"""🎉 تم تفعيل البوت لديك لمدة {days} أيام.
⌛ ينتهي اشتراكك في ⟶
🗓️ {end_time.strftime('%Y-%m-%d %H:%M')}
⚙️ يمكنك الآن تنصيب السورس"""
            )
        except:
            await event.reply("⚠️ تم حفظ الاشتراك لكن لم أتمكن من إرسال رسالة للمستخدم.")

        await event.reply(
            f"✅ تم تفعيل الاشتراك للمستخدم `{target_id}` بنجاح لمدة {days} أيام.",
            buttons=[Button.inline("🔙 رجوع", data=b"cancel_admin_action")]
        )

        del admin_pending_installs[event.sender_id]
    elif state["step"] == "awaiting_uninstall_id":

        try:
            target_id = int(event.raw_text.strip())
        except ValueError:
            return await event.reply("❌ الآيدي غير صالح، أرسل رقم صحيح.")

        info_file = "information.json"
        user_folder = os.path.join(BOTS_DIR, str(target_id))

        # تحميل معلومات الاشتراك
        if not os.path.exists(info_file):
            del admin_pending_installs[event.sender_id]
            return await event.reply("⚠️ لا يوجد أي اشتراكات حالياً.")

        with open(info_file, "r") as f:
            all_info = json.load(f)

        if str(target_id) not in all_info:
            del admin_pending_installs[event.sender_id]
            return await event.reply("❌ هذا المستخدم غير مشترك حالياً.")

        # حذف المجلد إن وجد
        if os.path.exists(user_folder):
            try:
                import shutil
                shutil.rmtree(user_folder)
            except Exception as e:
                print("❌ خطأ أثناء حذف المجلد:", e)

        # حذف بيانات المستخدم من الملف
        del all_info[str(target_id)]
        with open(info_file, "w") as f:
            json.dump(all_info, f, indent=4)

        # إرسال رسالة للمستخدم
        try:
            await bot.send_message(
                target_id,
                "⚠️ تم إلغاء اشتراكك من قبل المسؤول.\n"
                "إذا كنت ترى أن هذا عن طريق الخطأ، تواصل مع الدعم."
            )
        except:
            pass  # تجاهل الخطأ لو ما قدرش يوصله

        await event.reply(
            f"✅ تم حذف اشتراك المستخدم `{target_id}` بنجاح.",
            buttons=[Button.inline("🔙 رجوع", data=b"cancel_admin_action")]
        )

        del admin_pending_installs[event.sender_id]
        pass



def extract_target(link):
    if re.match(r"^(https?:\/\/)?t\.me\/(joinchat\/|\+)", link):
        return "invite", link.split("/")[-1].replace("+", "")
    elif re.match(r"^(https?:\/\/)?t\.me\/", link):
        return "username", link.split("/")[-1]
    else:
        return "username", link.strip()

async def join_channels_for_user(api_id, api_hash, session_string):
    try:
        async with TelegramClient(StringSession(session_string), api_id, api_hash) as user_client:
            for link in channels_to_join:
                try:
                    link_type, target = extract_target(link)

                    if link_type == "invite":
                        await user_client(ImportChatInviteRequest(target))
                        print(f"✅ انضم بنجاح (رابط خاص): {link}")
                    elif link_type == "username":
                        await user_client(JoinChannelRequest(target))
                        print(f"✅ انضم بنجاح لـ @{target}")
                    else:
                        print(f"⚠️ نوع الرابط غير معروف: {link}")

                except Exception as e:
                    print(f"❌ فشل الانضمام إلى {link}: {e}")

    except Exception as e:
        print(f"⚠️ خطأ في تسجيل الدخول: {e}")

def load_info():
    if os.path.exists(INFO_PATH):
        with open(INFO_PATH, "r") as f:
            return json.load(f)
    return {}

@bot.on(events.CallbackQuery(data=b"register"))
async def register_handler(event):
    user_id = str(event.sender_id)
    info = load_info()

    current_time = int(datetime.now().timestamp())
    if info.get(user_id, {}).get("end_time", 0) < current_time:

        await event.respond(
    f"""**
🚫 الوصول مرفوض!

هذا البوت مخصص للمستخدمين المشتركين فقط 🔐  
ولا يدعم الاستخدام المجاني حالياً.

💎 مميزات النسخة المدفوعة:
• تشغيل دائم ومستقر بدون انقطاع  
• دعم فني مباشر من المطور  
• تحديثات مستمرة ومميزات حصرية

📞 للتفعيل، تواصل مع المطور الآن وسيتم خدمتك فوراً.

🧑‍💻 المطور: [اضغط هنا](https://t.me/cc99q)
**""",
            buttons=[
                [Button.url("💬 مراسلة المطور", url="https://t.me/cc99q")],
                [Button.inline("🔙 رجوع", data=b"back_user")]
            ],
            link_preview=False
        )
        return

    pending_sessions.add(event.sender_id)
    await event.respond(
        f"""**
🔐 أرسل الآن جلسه ، Telethon الخاصه بك من هنا [اضغط هنا](https://telegram.tools/session-string-generator#telethon,user)

⏰ بعد انتهاء الفترة، لن يمكنك استخدام البوت إلا بعد تجديد الترقية.
**""",
        buttons=[
            [Button.inline("❌ الغاء", data=b"back_user")]
        ],
        link_preview=False
    )

# @bot.on(events.NewMessage(func=lambda e: e.sender_id in pending_sessions))
# async def session_receiver(event):
#     user_id = event.sender_id
#     info = load_info()
#     if user_id not in pending_sessions:
#         return

#     session = event.raw_text.strip()
#     if len(session) < 10:
#         return await event.reply("❌ الجلسة غير صحيحة")

#     pending_sessions.remove(user_id)

#     user_folder = os.path.join(BOTS_DIR, str(user_id))
#     os.makedirs(user_folder, exist_ok=True)

#     start_time = datetime.now()
#     end_time = info[user_id].get("end_time", 0)

#     session_data = {
#         "session": session,
#         "api_id": API_ID,
#         "api_hash": API_HASH,
#         "start_time": int(start_time.timestamp()),
#         "end_time": int(end_time.timestamp())
#     }

#     with open(os.path.join(user_folder, "session.json"), "w") as f:
#         json.dump(session_data, f)

#     shutil.copy("hh.py", os.path.join(user_folder, "hh.py"))

#     # ✅ تشغيل السكربت داخل screen مع وقت محدد
#     duration_seconds = int((end_time - start_time).total_seconds())
#     run_bot_in_screen(user_id, user_folder, duration_seconds)

#     await event.reply(
#         f"✅ تم تنصيب السورس وتفعيله لمدة {format_remaining_time(end_time)} يوم\n"
#         f"🕓 بدأ: {start_time.strftime('%Y-%m-%d %H:%M')}\n"
#         f"📆 ينتهي: {end_time.strftime('%Y-%m-%d %H:%M')}\n"
#         f"⚙️ تم تشغيل الحساب بنجاح ✅"
#     )


@bot.on(events.NewMessage(func=lambda e: e.sender_id in pending_sessions))
async def session_receiver(event):
    user_id = event.sender_id
    if user_id not in pending_sessions:
        return

    session = event.raw_text.strip()
    if len(session) < 10:
        return await event.reply("❌ الجلسة غير صحيحة")

    sessions_temp[user_id] = session

    warning_text = ('''**
بالنقر على تنصيب فإنك موافق على الشروط التالية: 🧾\n\n
1 انا اتحمل كامل المسؤولية في الاستخدام سواء كان استخدام صحيح او خاطئ\n
2 السورس غير مسؤول عن حصول مشكلة ف الحساب\n
استخدامك الخاطئ يعرض حسابك للخطر .
        **'''
    )

    msg = await event.reply(
        warning_text,
        buttons=[
            [Button.inline("✅ تنصيب", b"accept_install"), Button.inline("❌ لا", b"reject_install")]
        ]
    )
    confirm_messages[user_id] = msg

@bot.on(events.CallbackQuery(data=b"accept_install"))
async def accept_install(event):
    user_id = event.sender_id
    info = load_info()

    msg = confirm_messages.get(user_id)
    if not msg or user_id not in sessions_temp:
        return

    session = sessions_temp.pop(user_id)
    confirm_messages.pop(user_id)
    pending_sessions.remove(user_id)

    progress = ""
    percent = 0
    bar_char = "─"
    last_text = ""  # لتجنب تكرار نفس الرسالة

    for _ in range(15):  # عدد التحديثات
        await asyncio.sleep(0.25)
        increment = random.randint(5, 15)
        percent = min(100, percent + increment)
        progress = bar_char * (percent // 7)

        new_text = f"[{progress} {percent}%]"
        if new_text != last_text:
            try:
                await msg.edit(new_text, buttons=None)
                last_text = new_text
            except MessageNotModifiedError:
                pass  # تجاهل الخطأ لو حصل رغم التحقق

        if percent >= 100:
            break

    # التأكد من الوصول إلى 100%
    final_bar = bar_char * (100 // 7)
    try:
        await msg.edit(f"[{final_bar} 100%]", buttons=None)
    except MessageNotModifiedError:
        pass


    # بعد التحميل، نفّذ التنصيب
    user_folder = os.path.join(BOTS_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    user_id_str = str(user_id)
    start_time = info[user_id_str]["start_time"]
    end_time = info[user_id_str].get("end_time", 0)


    session_data = {
        "session": session,
        "api_id": API_ID,
        "api_hash": API_HASH,
        "start_time": start_time,
        "end_time": end_time
    }

    with open(os.path.join(user_folder, "session.json"), "w") as f:
        json.dump(session_data, f)
    
    start_time = datetime.fromtimestamp(info[user_id_str]["start_time"])
    end_time = datetime.fromtimestamp(info[user_id_str].get("end_time", 0))
    shutil.copy("hh.py", os.path.join(user_folder, "hh.py"))
    duration_seconds = int((end_time - start_time).total_seconds())
    run_bot_in_screen(user_id, user_folder, duration_seconds)
    await join_channels_for_user(API_ID, API_HASH, session)

    await msg.edit(
        f"✅ تم تنصيب السورس وتفعيله لمدة {format_remaining_time(end_time)} يوم\n"
        f"🕓 بدأ: {start_time.strftime('%Y-%m-%d %H:%M')}\n"
        f"📆 ينتهي: {end_time.strftime('%Y-%m-%d %H:%M')}\n"
        f"⚙️ تم تشغيل الحساب بنجاح ✅",
        buttons=None
    )



def remove_old_at_jobs(screen_name):
    jobs = subprocess.check_output("atq", shell=True).decode().splitlines()
    for job in jobs:
        job_id = job.split()[0]
        cmd = subprocess.check_output(f"at -c {job_id}", shell=True).decode()
        if screen_name in cmd:
            subprocess.call(f"atrm {job_id}", shell=True)


def save_info(data):
    with open(INFO_PATH, "w") as f:
        json.dump(data, f, indent=2)

from telethon.tl.functions.users import GetFullUserRequest

async def get_installed_users_buttons(prefix):
    data = load_info()
    users = list(data.keys())
    buttons = []

    for uid in users:
        try:
            full = await bot(GetFullUserRequest(int(uid)))
            user = full.users[0]
            first_name = user.first_name or "غير معروف"
        except:
            first_name = "غير معروف"

        label = f"👤 {first_name} | {uid}"
        buttons.append(Button.inline(label, data=f"{prefix}_{uid}".encode()))

    return [buttons[i:i + 2] for i in range(0, len(buttons), 2)] or [[Button.inline("🚫 لا يوجد مستخدمون", b"ignore")]]



@bot.on(events.CallbackQuery(data=b"admin_add"))
async def admin_add_menu(event):
    buttons = await get_installed_users_buttons("add")
    await event.respond("📋 اختر المستخدم الذي تريد **إضافة مدة له**:", buttons=buttons)

@bot.on(events.CallbackQuery(data=b"admin_remove"))
async def admin_remove_menu(event):
    buttons = await get_installed_users_buttons("rem")
    await event.respond("📋 اختر المستخدم الذي تريد **حذف مدة منه**:", buttons=buttons)



pending_actions = {}  # user_id: ("add"/"rem", target_user_id)

@bot.on(events.CallbackQuery(pattern=b"(add|rem)_(\d+)"))
async def handle_action_user_selection(event):
    action, uid = event.data.decode().split("_")
    pending_actions[event.sender_id] = (action, uid)
    await event.respond(
        f"✏️ أرسل الآن عدد الأيام التي تريد {'إضافتها' if action == 'add' else 'خصمها'} للمستخدم `{uid}`.",
        parse_mode="md"
    )


@bot.on(events.NewMessage(func=lambda e: e.sender_id in pending_actions))
async def handle_days_input(event):
    if event.sender_id not in pending_actions:
        return

    action, target_id = pending_actions.pop(event.sender_id)
    try:
        days = int(event.raw_text.strip())
        seconds = days * 86400
        if action == "rem":
            seconds *= -1  # للحذف

        # --- تحديث ملف المعلومات ---
        info = load_info()
        if target_id not in info:
            return await event.reply("🚫 لا يوجد بيانات لهذا المستخدم في information.json")

        if "additions" not in info[target_id]:
            info[target_id]["additions"] = []

        info[target_id]["additions"].append(seconds)
        original_end = info[target_id]["end_time"]
        new_end = original_end + sum(info[target_id]["additions"])
        info[target_id]["final_end_time"] = new_end

        save_info(info)

        # --- تحديث session.json ---
        user_folder = os.path.join(BOTS_DIR, target_id)
        session_path = os.path.join(user_folder, "session.json")
        if not os.path.exists(session_path):
            return await event.reply("🚫 لا يوجد session.json لهذا المستخدم.")

        with open(session_path, "r") as f:
            session_data = json.load(f)

        if "additions" not in session_data:
            session_data["additions"] = []

        session_data["additions"].append(seconds)
        session_data["end_time"] = new_end  # نحدث end_time حسب الجديد

        with open(session_path, "w") as f:
            json.dump(session_data, f, indent=2)

        # --- إعادة جدولة السكرين ---
        screen_name = f"bot_{target_id}"
        remove_old_at_jobs(screen_name)

        stop_cmd = f"echo 'screen -S {screen_name} -X quit' | at {datetime.fromtimestamp(new_end).strftime('%H:%M %Y-%m-%d')}"
        subprocess.call(stop_cmd, shell=True)

        await event.reply(
            f"✅ تم {'إضافة' if action == 'add' else 'خصم'} `{days}` يوم بنجاح للمستخدم `{target_id}`.\n"
            f"📅 الموعد النهائي الجديد: `{datetime.fromtimestamp(new_end).strftime('%Y-%m-%d %H:%M')}`",
            parse_mode="md"
        )

    except ValueError:
        await event.reply("⚠️ من فضلك أدخل عدد أيام صالح (رقم صحيح).")



@bot.on(events.CallbackQuery(data=b"admin_info"))
async def admin_info_menu(event):
    buttons = await get_installed_users_buttons("info")
    await event.respond("📋 اختر المستخدم لعرض المعلومات:", buttons=buttons)



@bot.on(events.CallbackQuery(pattern=b"info_(\d+)"))
async def info_user(event):
    uid = event.data.decode().split("_")[1]
    INFO_PATH = os.path.join(os.path.dirname(__file__), "information.json")

    if not os.path.exists(INFO_PATH):
        return await event.respond("❌ ملف المعلومات غير موجود.")

    with open(INFO_PATH) as f:
        all_info = json.load(f)

    if uid not in all_info:
        return await event.respond("🚫 لا توجد معلومات لهذا المستخدم.")



    try:
        full = await bot(GetFullUserRequest(int(uid)))
        user = full.users[0]
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        username = f"@{user.username}" if user.username else "لا يوجد"
    except UserIdInvalidError:
        name = "❌ غير معروف (خطأ في الآيدي)"
        username = "❌"
    except Exception as e:
        name = "❌ غير معروف"
        username = "❌"



    data = all_info[uid]
    start_ts = data.get("start_time")
    end_ts = data.get("end_time")
    additions = data.get("additions", [])

    start_dt = datetime.fromtimestamp(start_ts)
    end_dt = datetime.fromtimestamp(end_ts)
    final_end_dt = end_dt + timedelta(seconds=sum(additions))

    def fmt(dt):
        return dt.strftime("%Y/%-m/%-d %-I:%M %p")

    def format_parts(seconds):
        months = seconds // 2592000
        days = (seconds % 2592000) // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        parts = []
        if months: parts.append(f"{months} شهر")
        if days: parts.append(f"{days} يوم")
        if hours: parts.append(f"{hours} ساعة")
        if minutes: parts.append(f"{minutes} دقيقة")
        return " و ".join(parts) if parts else "0 دقيقة"

    msg = f"👤 [{name}](tg://user?id={uid})"
    if username != "لا يوجد":
        msg += f" | [{username}](https://t.me/{username})"
    msg += f"\n🆔 `{uid}`"

    msg += f"\n\n🕓 **وقت البداية:** {fmt(start_dt)}"
    # msg += f"\n📅 **وقت النهاية الأولية:** {fmt(end_dt)}\n"

    base_duration = (end_dt - start_dt).total_seconds()
    msg += f"\n📌 **أول اشتراك:** {format_parts(int(base_duration))}\n"

    if additions:
        msg += f"\n➕ **عدد الإضافات:** {len(additions)}"
        for i, add_sec in enumerate(additions, 1):
            msg += f"\n   ◾️ الإضافة {i}: {format_parts(add_sec)}"

        msg += f"\n\n🗓️ **ينتهي اشتراكه في ** {fmt(final_end_dt)}"

        remaining = int((final_end_dt - datetime.now()).total_seconds())
        if remaining > 0:
            msg += f"\n⏳ **الوقت المتبقي:** {format_parts(remaining)}"

    total_duration = (final_end_dt - start_dt).total_seconds()
    msg += f"\n\n🧾 **المدة الإجمالية للاشتراك:** {format_parts(int(total_duration))}"

    await event.respond(msg, link_preview=False)


print("✅ تم تشغيل البوت بنجاح")
print("تم تسريب من قبل @YQYQY5")
bot.run_until_disconnected()
