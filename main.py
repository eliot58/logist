from gtts import gTTS

def text_to_wav(text, output_file="output.wav", lang="ru"):
    print("Converting text to speech...")

    # Используем gTTS для синтеза речи
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("temp.mp3")

    print(f"Audio file '{output_file}' created successfully.")

if __name__ == "__main__":
    text = "Здравствуйте у вас на завтра в 17:00 заказ от окна петров готовы принять если нет то продиктуйте дату и время следующего приема заказа "
    text_to_wav(text)
