import speech_recognition as sr
import asyncio
from playsound import playsound
from speech_recognition import *
from Functions.voice_transfer import voice_transfer
from Functions.commands import answer_variation
from Functions.search_video import search_video, open_browser
from Functions.set_volume import set_system_volume
from Functions.program_interactive import get_program_path, open_program, close_program
import re, json, random, webbrowser, keyboard


r = sr.Recognizer()
sr.pause_threshold = 0.5


with open('sites.json', 'r', encoding='utf-8') as f:
    sites = json.load(f)['сайты']


def listen_command():
    with Microphone() as mic:
        try:
            r.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = r.listen(source=mic, timeout=5)
            query = r.recognize_google(audio_data=audio, language='ru-RU')
            query = query.lower()
            bot_name = 'бот'
            if bot_name in query:
                query = ' '.join(query.split()[1:])
            else:
                pass
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            query = ''
        return query


def get_site_url(site_name):
    for site in sites:
        name = site('название')
        if name and site_name in name.lower():
            print(name)
            return site['ссылка']
    print(f"Сайт с названием {site_name} не найден в списке доступных сайтов.")
    return None


def main():
    while True:
        query = listen_command()
        bot_name = 'бот'
        if query.startswith(bot_name):
            query = ' '.join(query.split()[1:])

        if not query:
            continue

        if any(variation in query for variation in answer_variation['commands']['kill_program']['variations']):
            voice_transfer('До свидания!')
            break
        
        if any(variation in query for variation in answer_variation['commands']['restart']['variations']):
            voice_transfer('Перезапускаюсь...')
            os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:])

        if any(variation in query for variation in answer_variation['commands']['full_mute']['variations']):
            voice_transfer('Ты без наушников, клоун')
            keyboard.press_and_release('-')

        if any(variation in query for variation in answer_variation['commands']['mute']['variations']):
            voice_transfer('Ты в муте, клоун')
            keyboard.press_and_release('/')


        for command, variations in answer_variation['commands'].items():
            for variation in variations['variations']:
                if variation in query:
                    try:
                    
                        if command in ('open_browser', 'открой сайт'):
                            site_name_match = re.findall(r'\b(\w+)\b', query)
                            site_name = site_name_match[-1] if site_name_match else None
                            url = get_site_url(site_name)
                            voice_transfer(f"Открываю сайт {site_name}")
                            if url:
                                open_browser(url)
                            else:
                                voice_transfer('К сожалению, я не могу открыть этот сайт.')
                        

                        elif command in ('open_program', 'бот открой программу', 'бот открой'):
                            program_name_match = re.findall(r'\b(\w+)\b', query)
                            program_name = program_name_match[-1] if program_name_match else None
                            program_path = get_program_path(program_name)
                            if program_path:
                                voice_transfer(f"Открываю программу {program_name}")
                                open_program(program_path)
                            else:
                                voice_transfer(f"Программа {program_name} не найдена.")


                        elif command in ('close_program', 'бот закрой программу', 'бот выключи программу', 'бот закрой'):
                            program_name_match = re.findall(r'\b(\w+)\b', query)
                            program_name = program_name_match[-1] if program_name_match else None
                            close_program(program_name)


                        elif command in ('play_music', 'включи музыку', 'поставь музыку'):
                            if 'песню' in query:
                                track_name = query.split('песню')[1].strip()
                            elif 'музыку' in query:
                                track_name = query.split('музыку')[1].strip()
                            else:
                                return
                            video_url = search_video(track_name)
                            webbrowser.open(video_url)
                            voice_transfer(f'Включаю музыку на YouTube для трека {track_name}')


                        elif command in('set_volume', 'громкость звука', 'громкость звука на'):
                            try:
                                if 'громкость звука на ' in query:
                                    volume = int(query.split('громкость звука на ')[1])
                                elif 'громкость звука' in query:
                                    volume = int(query.split('громкость звука ')[1])
                                elif 'громкость на' in query:
                                    volume = int(query.split('громкость на ')[1])
                                elif 'поставь громкость на ' in query:
                                    volume = int(query.split('поставь громкость на ')[1])
                                if volume < 0 or volume > 100:
                                    raise ValueError("Значение громкости должно быть в диапазоне от 0 до 100.")
                                set_system_volume(volume)
                                voice_transfer(f"Громкость изменена на {volume}.")
                            except (IndexError, ValueError):
                                voice_transfer("Укажите значение громкости от 0 до 100.")

                                
                        elif command in('pause', 'поставь паузу', 'паузу', 'пауза', 'выключи паузу'):
                            try:
                                if 'поставь паузу' in query:
                                    keyboard.press_and_release('play/pause media')
                                    voice_transfer(f"Пауза установлена.")
                                elif 'выключи паузу' in query:
                                    keyboard.press_and_release('play/pause media')
                                    voice_transfer(f"Сделано.")
                            except (IndexError, ValueError):
                                voice_transfer("Ошибка.")
                        else:
                            response = variations['response']
                            if isinstance(response, list):
                                rand_response = random.choice(response)
                            print(rand_response)
                            voice_transfer(rand_response)


                    except Exception as e:
                        print(f"Произошло исключение: {e}")
                        voice_transfer('Что-то пошло не так:(')
                        continue
                    break
            else:
                continue
            break



if __name__ == '__main__':
    enable = 'D:\\\\projects\\\\Voice_Assistant\\\\sounds\\\\enable.mp3'
    playsound(enable)
    main()

