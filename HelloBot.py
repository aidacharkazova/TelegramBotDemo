from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import undetected_chromedriver as uc 
import httpx

def take_screenshot(url: str, output_path: str = "screenshot.png"):
    options = uc.ChromeOptions()
    # options.headless = True
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280x800')

    driver = uc.Chrome(options=options)
    driver.get(url)
    driver.save_screenshot(output_path)
    driver.quit()



async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if not context.args:
        await update.message.reply_text("Please provide a city name. Example: /weather London")
        return
    WEATHER_API_KEY = "2146ac52adc02f347f3124b462791a50"
    city = " ".join(context.args)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    print(f"Request URL: {url}")

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    print("Request URL:", url)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code != 200:
        await update.message.reply_text("Sorry, I couldn't find that city.")
        return
    
    data = response.json()
    name = data['name']
    temp = data['main']['temp']
    desc = data['weather'][0]['description'].capitalize()
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    reply = (
        f"🌤️ Weather in **{name}**\n"
        f"Temperature: {temp}°C\n"
        f"Description: {desc}\n"
        f"Humidity: {humidity}%\n"
        f"Wind: {wind_speed} m/s"
    )

    await update.message.reply_markdown(reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I'm Aida's Bot, How can I help you?")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Taking screnshoot..")
     
    url = 'https://bhos.edu.az/en'
    screenshot_file = 'screenshot.png'

    take_screenshot(url,screenshot_file)

    with open(screenshot_file, 'rb') as photo:
        await update.message.reply_photo(photo)
    


if __name__ == '__main__':
    import os
    TOKEN = '7625042019:AAH4M2LSsVR0nOv8HpRubkjW7yj1KbzbI_k'

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(CommandHandler("screenshot",screenshot))
    app.add_handler(CommandHandler("weather",weather))

    print("Bot is running..")
    app.run_polling()

