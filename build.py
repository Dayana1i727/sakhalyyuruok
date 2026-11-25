#!/usr/bin/env python3
"""Собирает самодостаточный index.html: инлайнит картинки и шрифты в base64."""
import base64, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
BUILD = ROOT / "assets" / "web"
OUT = ROOT / "index.html"

def b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()

def datauri(path, mime=None):
    p = pathlib.Path(path)
    if mime is None:
        mime = "image/png" if p.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64,{b64(p)}"

PERSON_IMG = {f"p{i}": datauri(BUILD / f"p{i}.jpg") for i in range(1, 7)}

# обложки школьного раздела (лексика / фонетика / морфология)
SCHOOL_IMG = {"S1": "s1.jpg", "S2": "s2.jpg", "S3": "s3.jpg",
              "L1": "l1.jpg", "L2": "l2.jpg", "L3": "l3.jpg", "L4": "l4.jpg"}

IMG = {
    "HERO": datauri(BUILD / "hero.jpg"),
    "L1": datauri(BUILD / "lesson1.jpg"),
    "L2": datauri(BUILD / "lesson2.jpg"),
    "L3": datauri(BUILD / "lesson3.jpg"),
    "L4": datauri(BUILD / "words.jpg"),
    "L5": datauri(BUILD / "lesson5.jpg"),
    "L6": datauri(BUILD / "lesson6.jpg"),
    "F1": datauri(BUILD / "ph1.jpg"),
    "F2": datauri(BUILD / "ph2.jpg"),
    "F3": datauri(BUILD / "ph3.jpg"),
    "F4": datauri(BUILD / "ph4.jpg"),
    "F5": datauri(BUILD / "ph5.jpg"),
    "F6": datauri(BUILD / "ph6.jpg"),
    "F7": datauri(BUILD / "ph7.jpg"),
    "F8": datauri(BUILD / "ph8.jpg"),
    "F9": datauri(BUILD / "ph9.jpg"),
    "PROMO": datauri(BUILD / "promo.jpg"),
    "WORDS": datauri(BUILD / "words.jpg"),
    "CAT": datauri(BUILD / "cat.png"),
    "ORN": datauri(BUILD / "ornament.png"),
    "SCENE": datauri(BUILD / "scene_left.png"),
    "MASCOT": datauri(BUILD / "mascot.jpg"),
    "MASCOT_FACE": datauri(BUILD / "mascot-face.jpg"),
}

# иллюстрации слов первого урока (аниме-минимализм, якутские мотивы)
WORD_IMG = {
    "Дорообо": "w1",
    "Үтүө күн": "w2",
    "Аат": "w3",
    "Мин": "w4",
    "Эн": "w5",
    "Үөрүстүм": "w6",
    "Баһыыба": "w7",
    "Көрсүһүөххэ диэри": "w8",
    # урок 6 «Еда и традиции»
    "Ас": "w9",
    "Эт": "w10",
    "Балык": "w11",
    "Үүт": "w12",
    "Чэй": "w13",
    "Кымыс": "w14",
    "Саламат": "w15",
    "Ыһыах": "w16",
}

# записанная озвучка якутских слов (женский голос, вшивается в файлы)
AUDIO_DIR = ROOT / "assets" / "audio"

def _nkey(t):
    import re
    k = re.sub(r"\s+", " ", str(t)).strip()
    k = re.sub(r"[!?.,]+$", "", k)
    return k.lower()


def audio_map():
    import json
    man = AUDIO_DIR / "manifest.json"
    if not man.exists():
        return {}
    data = json.loads(man.read_text(encoding="utf-8"))
    out = {}
    for text, fname in data.items():
        f = AUDIO_DIR / fname
        if f.exists():
            mime = "audio/wav" if f.suffix.lower() == ".wav" else "audio/mpeg"
            out["sah|" + _nkey(text)] = datauri(f, mime)
    return out


# все слова для standalone-виджета
WIDGET_WORDS = [
    ("Дорообо", "привет", 1), ("Үтүө күн", "добрый день", 1), ("Аат", "имя", 1),
    ("Мин", "я", 1), ("Эн", "ты", 1), ("Үөрүстүм", "рад познакомиться", 1),
    ("Баһыыба", "спасибо", 1), ("Көрсүһүөххэ диэри", "до свидания", 1),
    ("Үчүгэй", "хорошо", 2), ("Куһаҕан", "плохо", 2), ("Көрдөһөбүн", "пожалуйста", 2),
    ("Бырастыы гыныҥ", "извините", 2), ("Хас?", "сколько?", 2), ("Бу", "это", 2),
    ("Уу", "вода", 2), ("Дьиэ", "дом", 2),
    ("Аатыҥ кимий?", "как тебя зовут?", 3), ("Мин аатым Айсен", "меня зовут Айсен", 3),
    ("Хайдах олороҕут?", "как поживаете?", 3), ("Үчүгэй, баһыыба", "хорошо, спасибо", 3),
]

LESSONS = [
    dict(n=1, title="Знакомства", time="10 мин", img="L1", tags="a1 лексика", done=0, play=True),
    dict(n=2, title="Бытовые фразы", time="12 мин", img="L2", tags="a1 лексика", done=0, play=True),
    dict(n=3, title="Мини-диалоги", time="12 мин", img="L3", tags="a1 лексика", done=0, play=True),
    dict(n=4, title="Предложения", time="14 мин", img="L4", tags="фразы", done=0, play=True),
    dict(n=5, title="Заверши диалог", time="13 мин", img="L5", tags="диалоги", done=0, play=True),
    dict(n=6, title="Еда и традиции", time="14 мин", img="L6", tags="культура лексика", done=0, play=True),
    dict(n=7, title="Олонхо и культура", time="16 мин", img="L3", tags="культура", done=0,
         style="object-position:60% 85%"),
    dict(n=8, title="Города и места", time="13 мин", img="L2", tags="лексика", done=0,
         style="filter:saturate(.9) hue-rotate(-8deg)"),
]

WORDS = [
    ("Дорообо", "привет"),
    ("Үтүө күн", "добрый день"),
    ("Баһыыба", "спасибо"),
    ("Үөрүстүм", "рад познакомиться"),
]

FAV = [
    ("дьон", "люди, народ"),
    ("сибэкки", "цветок"),
    ("доҕор", "друг"),
    ("дьол", "счастье"),
    ("үтүө күн", "добрый день"),
    ("баһыыба", "спасибо"),
]


FACTS = [
    dict(img="F1", cat="nature", tag="Якутия", title="Полюс холода",
         text="В Оймяконе столбик термометра опускался до −71,2 °C — это самая низкая температура "
              "на Земле, где постоянно живут люди. Вывешенное бельё замерзает за минуту, а зимой "
              "носят по пять слоёв одежды."),
    dict(img="F2", cat="nature", tag="Якутия", title="Ленские столбы",
         text="Скалы высотой до 200 метров тянутся на 40 км вдоль реки Лены. С 2012 года это "
              "наследие ЮНЕСКО, а в пещерах рядом нашли стоянки людей каменного века."),
    dict(img="F3", cat="nature", tag="Якутия", title="Северное сияние",
         text="Больше трети республики лежит за Полярным кругом, поэтому с сентября по март сияние "
              "видно почти каждую ясную ночь. Для оленей, что пасутся рядом, −50 °C — обычная погода."),
    dict(img="F4", cat="nature", tag="Якутия", title="Алмазы",
         text="В 1955 году геологи нашли кимберлитовую трубку «Мир». Сегодня в Якутии добывают около "
              "четверти всех алмазов мира, а сам карьер ушёл в глубину на 525 метров."),
    dict(img="F5", cat="nature", tag="Якутия", title="Вечная мерзлота",
         text="Почти вся Якутия стоит на вечной мерзлоте: дома в Якутске строят на сваях, а под "
              "землёй устраивают «холодильники», где круглый год держится около −8 °C."),
    dict(img="F6", cat="culture", tag="Культура", title="Олонхо",
         text="Героический эпос саха о трёх мирах, где богатырь защищает людей. Его поют нараспев "
              "часами, без музыки. В 2005 году ЮНЕСКО признало олонхо шедевром устного наследия "
              "человечества."),
    dict(img="F7", cat="culture", tag="Культура", title="Ыһыах и осуохай",
         text="Главный праздник лета в день солнцестояния: огромный хоровод осуохай, кумыс, саламат "
              "и алгыс — благопожелание на год вперёд. Танцуют все — от детей до стариков."),
    dict(img="F8", cat="culture", tag="Культура", title="Хомус",
         text="Якутский варган размером с ладонь: звук рождают язык и дыхание. Каждый июнь в Якутске "
              "собираются мастера и музыканты со всего мира — на фестиваль хомуса."),
    dict(img="F9", cat="history", tag="История", title="Якутский острог",
         text="В 1632 году отряд Петра Бекетова поставил на берегу Лены деревянную крепость. С неё "
              "начался Якутск, а сам острог стал опорным пунктом на пути к Тихому океану."),
]

HISTORY = [
    ("XIII–XV вв.", "Предки саха — тюркоязычные племена с юга — приходят на Среднюю Лену. "
                    "Здесь складывается народ саха, его язык и культура коневодов."),
    ("1632", "Отряд Петра Бекетова ставит Якутский острог на правом берегу Лены — с этого года "
             "Якутия входит в состав Российского государства."),
    ("1922", "27 апреля образуется Якутская АССР — день государственности якутского народа."),
    ("1955", "Найдена кимберлитовая трубка «Мир» — начинается промышленная добыча алмазов."),
    ("1990", "Якутия становится Республикой Саха (Якутия) в составе России."),
    ("2005 · 2012", "Олонхо признано шедевром устного наследия ЮНЕСКО, а Ленские столбы "
                    "попадают в список Всемирного наследия."),
]


def fact_card(f):
    return f'''<article class="fact-card" data-cat="{f['cat']}">
          <div class="fact-thumb"><img src="{IMG[f['img']]}" alt="{f['title']}" loading="lazy"><span class="fact-tag">{f['tag']}</span></div>
          <div class="fact-body">
            <h4>{f['title']}</h4>
            <p>{f['text']}</p>
          </div>
        </article>'''


def history_row(i, year, text):
    return f'''<div class="tl-row">
            <span class="tl-dot"></span>
            <div class="tl-year">{year}</div>
            <p>{text}</p>
          </div>'''


PEOPLE = [
    dict(name="Суорун Омоллоон", real="Дмитрий Сивцев", years="1906–2005",
         role="писатель, драматург, фольклорист", img="p1",
         text="Народный писатель Якутии и Герой Социалистического Труда. Написал больше сорока пьес, "
              "собирал олонхо, стал автором либретто первой якутской оперы «Ньургун Боотур» и основал "
              "несколько музеев в республике."),
    dict(name="Платон Ойунский", real="Платон Слепцов", years="1893–1939",
         role="поэт, учёный, государственный деятель", img="p2",
         text="Основоположник якутской советской литературы: стихи, рассказы, работы о языке. Его поэму "
              "«Кыһыл ойуун» («Красный шаман») перевели на многие языки. В 1939 году был репрессирован."),
    dict(name="Алексей Кулаковский", real="Өксөкүлээх Өлөксөөй", years="1877–1926",
         role="поэт и этнограф", img="p3",
         text="Один из основоположников якутской письменной литературы. Писал стихи и научные труды, "
              "собирал фольклор и верования саха, автор «Письма якутской интеллигенции»."),
    dict(name="Семён Данилов", real="Семён Данилов", years="1917–1978",
         role="поэт", img="p4",
         text="Народный поэт Якутии, автор десятков сборников о родной земле и людях. Перевёл на якутский "
              "Пушкина, Лермонтова и Шевченко, возглавлял Союз писателей республики."),
    dict(name="Роман Дмитриев", real="Роман Дмитриев", years="1949–2010",
         role="борец, первый олимпийский чемпион из Якутии", img="p5",
         text="Золото Олимпиады-1972 в Мюнхене в вольной борьбе (до 48 кг) — первое олимпийское золото "
              "Якутии. Ещё серебро Олимпиады-1976, титулы чемпиона мира и Европы, шесть побед на "
              "чемпионатах СССР."),
    dict(name="Дмитрий Давыдов", real="Дмитрий Давыдов", years="род. 1983",
         role="кинорежиссёр", img="p6",
         text="Школьный учитель из села Амга, который стал режиссёром. Его фильм «Пугало» получил Гран-при "
              "«Кинотавра» в 2020 году, а «Костёр на ветру» и «Ыт» показывали на фестивалях по всему миру."),
]


def person_card(p):
    has_img = bool(p.get("img")) and p["img"] in PERSON_IMG
    if has_img:
        ava = f'<img src="{PERSON_IMG[p["img"]]}" alt="{p["name"]}" loading="lazy">'
    else:
        ini = "".join(part[0] for part in p["name"].split()[:2]).upper()
        ava = f'<b>{ini}</b>'
    real = p["real"] if p["real"] != p["name"] else ""
    meta = " · ".join(x for x in [real, p["years"], p["role"]] if x)
    return f'''<article class="person">
            <div class="person-ava{' mono' if not has_img else ''}">{ava}</div>
            <div class="person-body">
              <h4>{p['name']}</h4>
              <div class="person-meta">{meta}</div>
              <p>{p['text']}</p>
            </div>
          </article>'''


DICT = [
    ("Приветствия", [
        ("привет", "дорообо"), ("добрый день", "үтүө күн"), ("спасибо", "баһыыба"),
        ("пожалуйста", "көрдөһөбүн"), ("извините", "бырастыы гыныҥ"),
        ("до свидания", "көрсүһүөххэ диэри"), ("да", "сөп"), ("нет", "суох"),
        ("хорошо", "үчүгэй"), ("плохо", "куһаҕан"), ("как тебя зовут?", "аатыҥ кимий?"),
        ("как поживаете?", "хайдах олороҕут?"),
    ]),
    ("Люди и семья", [
        ("человек", "киһи"), ("люди", "дьон"), ("ребёнок", "оҕо"), ("мальчик", "уол"),
        ("девочка", "кыыс"), ("мужчина", "эр киһи"), ("женщина", "дьахтар"),
        ("отец", "аҕа"), ("мать", "ийэ"), ("дедушка", "эһэ"), ("бабушка", "эбэ"),
        ("старший брат", "убай"), ("старшая сестра", "эдьиий"), ("друг", "доҕор"),
        ("учитель", "учуутал"), ("ученик", "үөрэнээччи"),
    ]),
    ("Местоимения и вопросы", [
        ("я", "мин"), ("ты", "эн"), ("он, она", "кини"), ("мы", "биһиги"), ("вы", "эһиги"),
        ("они", "кинилэр"), ("это", "бу"), ("кто?", "ким?"), ("что?", "туох?"),
        ("сколько?", "хас?"), ("где?", "ханна?"), ("когда?", "хаһан?"),
    ]),
    ("Числа", [
        ("один", "биир"), ("два", "икки"), ("три", "үс"), ("четыре", "түөрт"),
        ("пять", "биэс"), ("шесть", "алта"), ("семь", "сэттэ"), ("восемь", "аҕыс"),
        ("девять", "тоҕус"), ("десять", "уон"), ("двадцать", "сүүрбэ"), ("сто", "сүүс"),
        ("тысяча", "тыһыынча"),
    ]),
    ("Цвета", [
        ("белый", "маҥан"), ("чёрный", "хара"), ("красный", "кыһыл"), ("жёлтый", "араҕас"),
        ("зелёный", "от күөх"), ("синий", "халлаан күөх"), ("серый", "бороҥ"),
    ]),
    ("Природа", [
        ("небо", "халлаан"), ("земля", "сир"), ("вода", "уу"), ("лес", "тыа"),
        ("река", "өрүс"), ("озеро", "күөл"), ("гора", "хайа"), ("море", "муора"),
        ("дерево", "мас"), ("трава", "от"), ("цветок", "сибэкки"), ("снег", "хаар"),
        ("дождь", "самыыр"), ("ветер", "тыал"), ("солнце", "күн"), ("луна", "ый"),
        ("звезда", "чолбон"), ("огонь", "уот"), ("лёд", "муус"),
    ]),
    ("Животные", [
        ("лошадь", "ат"), ("корова", "ынах"), ("олень", "таба"), ("собака", "ыт"),
        ("птица", "көтөр"), ("рыба", "балык"), ("зверь", "кыыл"), ("утка", "кус"),
        ("медведь", "эһэ"), ("лиса", "саһыл"), ("волк", "бөрө"),
    ]),
    ("Еда", [
        ("еда", "ас"), ("мясо", "эт"), ("молоко", "үүт"), ("чай", "чэй"),
        ("хлеб", "килиэп"), ("соль", "туус"), ("сахар", "саахар"), ("масло", "арыы"),
        ("кумыс", "кымыс"), ("саламат", "саламат"), ("оладьи", "алаадьы"),
    ]),
    ("Дом и город", [
        ("дом", "дьиэ"), ("дверь", "аан"), ("окно", "түннүк"), ("стол", "остуол"),
        ("стул", "олоппос"), ("кровать", "орон"), ("книга", "кинигэ"), ("деньги", "харчы"),
        ("дорога", "суол"), ("город", "куорат"), ("село", "сэлиэнньэ"), ("школа", "оскуола"),
        ("работа", "үлэ"),
    ]),
    ("Действия", [
        ("идти", "бар"), ("приходить", "кэл"), ("кушать", "аһаа"), ("пить", "ис"),
        ("спать", "утуй"), ("сидеть", "олор"), ("вставать", "тур"), ("говорить", "саҥар"),
        ("учиться", "үөрэн"), ("работать", "үлэлээ"), ("читать", "аах"), ("писать", "суруй"),
        ("видеть", "көр"), ("слышать", "исти"), ("знать", "бил"), ("любить", "таптаа"),
        ("думать", "санаа"), ("давать", "биэр"), ("брать", "ыл"),
    ]),
    ("Признаки", [
        ("большой", "улахан"), ("маленький", "кыра"), ("новый", "саҥа"), ("старый", "эргэ"),
        ("тёплый", "сылаас"), ("холодный", "тымныы"), ("вкусный", "амтаннаах"),
        ("красивый", "кыраһыабай"), ("быстрый", "түргэн"), ("медленный", "бытаан"),
    ]),
    ("Время", [
        ("сегодня", "бүгүн"), ("вчера", "бэҕэһээ"), ("завтра", "сарсын"),
        ("сейчас", "билигин"), ("потом", "кэлин"), ("день", "күн"), ("ночь", "түүн"),
        ("утро", "сарсыарда"), ("вечер", "киэһэ"), ("год", "дьыл"),
        ("неделя", "нэдиэлэ"), ("месяц", "ый"),
    ]),
]


def dict_group(title, rows):
    items = "\n              ".join(
        f'''<div class="drow" data-search="{ru} {y}">
                <b data-say="{y}" data-tr="{ru}" data-lang="sah">{ru}</b><em data-say="{y}" data-tr="{ru}" data-lang="sah">{y}</em>
                <button class="speak" data-speak="{y}" data-lang="sah" aria-label="Слушать «{y}»"><svg><use href="#i-sound"/></svg></button>
              </div>''' for ru, y in rows)
    return f'''<div class="dgroup">
            <h4>{title}</h4>
            <div class="drows">
              {items}
            </div>
          </div>'''


def clock_svg():
    return '<svg class="clock"><use href="#i-clock"/></svg>'


def go_svg():
    return '<svg><use href="#i-arrow"/></svg>'


def home_lesson_card(l):
    if l.get("play"):
        attrs = f'data-lesson="{l["n"]}"'
        soon = ""
    else:
        attrs = f'data-toast="Урок {l["n"]} · «{l["title"]}» — скоро"'
        soon = '<span class="soon">скоро</span>'
    return f'''<button class="lesson{' locked' if not l.get('play') else ''}" data-search="{l['title']} урок {l['n']} {l['tags']}" {attrs}>
                <div class="thumb">
                  <img src="{IMG[l['img']]}" alt=""{(' style="' + l['style'] + '"') if l.get('style') else ''}>
                  <span class="chip">Урок {l['n']}</span>{soon}
                </div>
                <h4>{l['title']}</h4>
                <div class="meta">
                  <span>{clock_svg()}{l['time']}</span>
                  <span class="go">{go_svg()}</span>
                </div>
              </button>'''


def full_lesson_card(l):
    done = l["done"]
    if l.get("play"):
        attrs = f'data-lesson="{l["n"]}"'
        mark = '<span data-mark>Не начат</span>'
    else:
        attrs = f'data-toast="Урок {l["n"]} · «{l["title"]}» — скоро"'
        mark = '<span>Скоро</span>'
    return f'''<button class="lesson lesson-card{' locked' if not l.get('play') else ''}" data-tags="{l['tags']}" {attrs}>
                <div class="thumb">
                  <img src="{IMG[l['img']]}" alt=""{(' style="' + l['style'] + '"') if l.get('style') else ''}>
                  <span class="chip">Урок {l['n']}</span>
                </div>
                <h4>{l['title']}</h4>
                <div class="meta">
                  <span>{clock_svg()}{l['time']}</span>
                  {mark}
                </div>
                <div class="pbar"><i style="width:{done}%"></i></div>
              </button>'''


def word_row(w, tr):
    return f'''<div class="word" data-search="{w} {tr}">
                    <b>{w}</b><em>{tr}</em>
                    <button class="speak" data-speak="{w}" aria-label="Слушать «{w}»"><svg><use href="#i-sound"/></svg></button>
                  </div>'''


def fav_row(w, tr):
    return f'''<div class="fav-row" data-search="{w} {tr}">
                <b>{w}</b><em>{tr}</em>
                <button class="speak" data-speak="{w}" aria-label="Слушать «{w}»"><svg><use href="#i-sound"/></svg></button>
                <button class="speak fav-del" data-toast="Убрали «{w}» из избранного" aria-label="Убрать из избранного"><svg viewBox="0 0 24 24" style="width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:1.9"><use href="#i-star"/></svg></button>
              </div>'''


def build():
    html = (ROOT / "src" / "template.html").read_text(encoding="utf-8")

    repl = dict(IMG)
    repl["FONT_CYR"] = b64(ROOT / "assets" / "fonts" / "mont-cyr.woff2")
    repl["FONT_LAT"] = b64(ROOT / "assets" / "fonts" / "mont-lat.woff2")
    repl["LESSON_CARDS"] = "\n              ".join(home_lesson_card(l) for l in LESSONS[:4])
    repl["ALL_LESSON_CARDS"] = "\n        ".join(full_lesson_card(l) for l in LESSONS)
    repl["WORD_ROWS"] = "\n                  ".join(word_row(w, t) for w, t in WORDS)
    repl["FACT_CARDS"] = "\n        ".join(fact_card(f) for f in FACTS)
    repl["DICT_GROUPS"] = "\n          ".join(dict_group(t, rows) for t, rows in DICT)
    repl["PEOPLE_CARDS"] = "\n          ".join(person_card(p) for p in PEOPLE)
    repl["HISTORY_ROWS"] = "\n          ".join(history_row(i, y, t) for i, (y, t) in enumerate(HISTORY, 1))

    for key, val in repl.items():
        html = html.replace("{{" + key + "}}", val)

    css = (ROOT / "src" / "lesson.css").read_text(encoding="utf-8")
    js = (ROOT / "src" / "lesson.js").read_text(encoding="utf-8")
    html = html.replace("</style>", css + "\n</style>", 1)
    img_js = "window.SAKHA_IMG = {mascot: \"" + datauri(BUILD / "mascot.jpg") + "\", face: \"" + datauri(BUILD / "mascot-face.jpg") + "\", faceOpen: \"" + datauri(BUILD / "mascot-face-open.jpg") + "\"," + ",".join(
        f'"{k}": "{datauri(BUILD / (v + ".jpg"))}"' for k, v in WORD_IMG.items()
    ) + "," + ",".join(f'"{k}": "{datauri(BUILD / v)}"' for k, v in SCHOOL_IMG.items()) + "};"
    import json as _json
    au = audio_map()
    audio_js = "window.SAKHA_AUDIO = " + _json.dumps(au, ensure_ascii=False) + ";"
    html = html.replace("</body>", "<script>\n" + img_js + "\n" + audio_js + "\n" + js + "\n</script>\n</body>", 1)

    left = re.findall(r"\{\{[A-Z_]+\}\}", html)
    if left:
        print("!! незаполненные плейсхолдеры:", set(left))

    OUT.write_text(html, encoding="utf-8")
    print(f"index.html: {OUT.stat().st_size/1024:.0f} KB")

    # ---------- отдельный файл виджета (для «На экран Домой») ----------
    import json
    wt = (ROOT / "src" / "widget.template.html").read_text(encoding="utf-8")
    words_json = json.dumps([{"y": y, "ru": r, "l": l} for y, r, l in WIDGET_WORDS], ensure_ascii=False)
    wt = wt.replace("{{FONT_CYR}}", b64(ROOT / "assets" / "fonts" / "mont-cyr.woff2"))
    wt = wt.replace("{{FONT_LAT}}", b64(ROOT / "assets" / "fonts" / "mont-lat.woff2"))
    wt = wt.replace("{{WORDS_JSON}}", words_json)
    wt = wt.replace("{{AUDIO_JSON}}", _json.dumps(audio_map(), ensure_ascii=False))
    wout = ROOT / "widget.html"
    wout.write_text(wt, encoding="utf-8")
    print(f"widget.html: {wout.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    build()
