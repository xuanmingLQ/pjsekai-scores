import json, base64, os
from src.sekaiworld.scores import Score, meta, Drawing


MUSICS_MD_FILE_PATH = "musics.json"
MUSIC_DIFFICULTIES_MD_FILE_PATH = "musicDifficulties.json"
JACKET_FILE_PATH = "jacket_s_074.png"
NOTE_HOST_PATH = "note"
SUS_PATH = "master"



def get_playlevel(music_id: int, difficulty: str):
    music_difficulties_md = read_json_from_file(MUSIC_DIFFICULTIES_MD_FILE_PATH)
    for diff in music_difficulties_md:
        if diff['musicId'] == music_id and diff['musicDifficulty'] == difficulty:
            return diff['playLevel']
    print(f"music {music_id} difficulty {difficulty} not found")
    return None
    

def test(music_id: int, difficulty: str):
    musics_md = read_json_from_file(MUSICS_MD_FILE_PATH)
    for music in musics_md:
        if music['id'] == music_id:
            break
    else:
        print(f"music {music_id} not found")
        exit(0)
    if music['composer'] == music['arranger']:
        artist = music['composer']
    elif music['composer'] in music['arranger'] or music['composer'] == '-':
        artist = music['arranger']
    elif music['arranger'] in music['composer'] or music['arranger'] == '-':
        artist = music['composer']
    else:
        artist = '%s / %s' % (music['composer'], music['arranger'])
    playlevel = get_playlevel(music_id, difficulty) or "?"
    jacket = get_img_b64(JACKET_FILE_PATH, 'png')
    score = Score.open(SUS_PATH, encoding='utf-8')
    score.meta = meta.Meta(
        title=music['title'],
        artist=artist,
        difficulty=difficulty,
        playlevel=str(playlevel),
        jacket=jacket,
        songid=str(music_id)
    )
    # no skill
    drawing = Drawing(
        score=score,
        note_host=f"file://{os.path.abspath(NOTE_HOST_PATH)}",
    )
    drawing.svg().saveas(f"{music_id}_{difficulty}.svg")
    # skill
    drawing = Drawing(
        score=score,
        note_host=NOTE_HOST_PATH,
        skill=True
    )
    drawing.svg().saveas(f"{music_id}_{difficulty}_skill.svg")
    pass


def read_json_from_file(path:str):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return json.loads(text)

def get_img_b64(img_path:str, format:str='jpeg'):
    with open(img_path, 'rb') as f:
        return f"data:image/{format};base64,{base64.b64encode(f.read()).decode('utf-8')}"

if __name__ == "__main__":
    music_id = 74
    difficulty = 'master'
    test(music_id, difficulty)