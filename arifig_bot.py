import telebot
import instaloader
from datetime import datetime
import time

# Inisialisasi bot Telegram dengan token
bot = telebot.TeleBot("7823657427:AAG1d8IZGCyceIHm26pOvNn-eD5DJ1Pabyo")

# Inisialisasi Instaloader tanpa login
L = instaloader.Instaloader()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Kirimkan username Instagram publik dan tanggal dalam format berikut:\n\nusername YYYY-MM-DD\nContoh: arifig_bot 2024-10-23")

@bot.message_handler(func=lambda message: True)
def fetch_instagram_post_by_date(message):
    try:
        # Pisahkan username dan tanggal dari input pengguna
        username, input_date = message.text.split()

        # Parsing tanggal dari string input pengguna
        search_date = datetime.strptime(input_date, "%Y-%m-%d").date()

        # Ambil profil Instagram dari username
        profile = instaloader.Profile.from_username(L.context, username)

        # Pastikan profil adalah publik
        if profile.is_private:
            bot.send_message(message.chat.id, f"Akun @{username} bersifat privat. Tidak dapat mengakses postingan.")
            return

        # Loop melalui postingan untuk menemukan postingan pada tanggal yang ditentukan
        found = False
        for post in profile.get_posts():
            post_date = post.date.date()

            # Jika tanggal postingan sesuai dengan yang dicari
            if post_date == search_date:
                # Kirim gambar dari URL postingan yang sesuai
                bot.send_photo(message.chat.id, post.url, caption=f"Postingan pada {search_date} dari @{username}")
                found = True

            # Tambahkan delay untuk menghindari rate limit
            time.sleep(2)

        if not found:
            bot.send_message(message.chat.id, f"Tidak ada postingan dari @{username} pada {search_date}.")
        
    except ValueError:
        bot.send_message(message.chat.id, "Format salah. Gunakan format: username YYYY-MM-DD")
    except instaloader.exceptions.ProfileNotExistsException:
        bot.send_message(message.chat.id, "Username tidak ditemukan atau akun pribadi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {str(e)}")

# Jalankan bot
bot.polling()
