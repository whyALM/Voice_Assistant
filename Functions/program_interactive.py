import json, os, psutil
from Functions.voice_transfer import voice_transfer

def get_program_path(program_name):
    with open('programs.json', 'r') as f:
        programs = json.load(f)
    if program_name in programs:
        return programs[program_name]['path']
    return None


def open_program(program_path):
    try:
        os.startfile(program_path)
    except:
        voice_transfer(f"Не удалось открыть программу {program_path}")


def close_program(program_name):
    for proc in psutil.process_iter():
        with open('programs.json', 'r') as f:
            programs = json.load(f)
        try:
            if proc.name().lower() == programs[program_name]['procces'].lower():
                print(programs[program_name]['name'])
                proc.kill()
                voice_transfer(f"Программа {programs[program_name]['name']} была закрыта")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(e)
    voice_transfer(f"Программа {programs[program_name]['name']} не была найдена")
    return False