#!/usr/bin/env python3
import base64
import logging
import os
import speech_recognition as sr
import sys
import tempfile


logger = logging.getLogger(__name__)


def filepath(filename, folder=None):
    if not folder:
        folder = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(folder, filename)


def split_audio_at_silence(folder):
    os.system(
        f"sox -V3 {filepath('audio.wav', folder)} {filepath('audio_.wav', folder)}"
        " silence -l 0 1 0.5 0.1% : newfile : restart > /dev/null 2> /dev/null"
    )
    return sorted([
        filepath(f, folder) for f in os.listdir(folder)
        if f.startswith("audio_") and f.endswith('.wav')
    ])


def save_audio_file(data, folder):
    filename = "audio.wav"
    with open(filepath(filename, folder), "wb") as f:
        f.write(base64.decodebytes(data.encode('utf8')))


def transcribe_letter(audiofile):
    r = sr.Recognizer()
    with sr.AudioFile(audiofile) as source:
        audio = r.record(source)

    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        raise IOError


def normalize(letter):
    if not letter:
        return ''

    c = letter.lower()
    if len(c) == 1:
        return c
    else:
        table = {
            'ar': 'r',
            'in': 'n',
            'jay': 'j',
            'key': 'k',
            'why': 'y',
            'tea': 't',
            'you': 'u',
        }
        if c in table:
            return table[c]
        else:
            logger.debug(f"Could't find letter '{c}'")
            return ''


def transcribe(data):
    with tempfile.TemporaryDirectory() as folder:
        save_audio_file(data, folder)
        audiofiles = split_audio_at_silence(folder)
        pieces = [transcribe_letter(audiofile) for audiofile in audiofiles]
        __import__('pdb').set_trace()
        pass
    msg = ''.join(map(normalize, pieces))
    return msg


def main():
    with open('audio.txt') as f:
        print(transcribe(f.read()))


if __name__ == '__main__':
    main()
