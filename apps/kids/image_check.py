from transformers import pipeline
from PIL import Image


classifier = pipeline(
    "zero-shot-image-classification",
    model="openai/clip-vit-base-patch32"
)

NG_LABELS = [
    # お酒
    "alcohol",
    "beer",
    "wine",
    "sake",
    "whisky",
    "cocktail",
    "canned cocktail",
    "chuhai",
    "chu-hi",
    "Japanese alcoholic drink",
    "a can of alcoholic beverage",
    "a beer can",
    "a wine bottle",
    "a liquor bottle",

    # タバコ
    "cigarette",
    "smoking",
    "tobacco",
    "cigarette pack",
    "IQOS",
    "HEETS",
    "TEREA",
    "Ploom",
    "glo",

    # 武器
    "gun",
    "firearm",
    "weapon",
    "knife",

    # 薬物
    "drugs",
    "illegal drugs",

    # 暴力
    "violent scene",
    "blood",
    "fight",
]

# 表示用（日本語）
REASON_JA = {
    # お酒
    "alcohol": "お酒",
    "beer": "ビール",
    "wine": "ワイン",
    "sake": "日本酒",
    "whisky": "ウイスキー",
    "cocktail": "カクテル",
    "canned cocktail": "缶チューハイ",
    "chuhai": "チューハイ",
    "chu-hi": "チューハイ",
    "Japanese alcoholic drink": "日本のお酒",
    "a can of alcoholic beverage": "お酒の缶",
    "a beer can": "ビール缶",
    "a wine bottle": "ワインボトル",
    "a liquor bottle": "お酒のボトル",

    # タバコ
    "cigarette": "タバコ",
    "smoking": "喫煙",
    "tobacco": "タバコ製品",
    "cigarette pack": "タバコの箱",
    "IQOS": "電子タバコ（IQOS）",
    "HEETS": "加熱式タバコ（HEETS）",
    "TEREA": "加熱式タバコ（TEREA）",
    "Ploom": "電子タバコ（Ploom）",
    "glo": "電子タバコ（glo）",

    # 武器
    "gun": "銃",
    "firearm": "銃器",
    "weapon": "武器",
    "knife": "ナイフ・刃物",

    # 薬物
    "drugs": "薬物",
    "illegal drugs": "違法薬物",

    # 暴力
    "violent scene": "暴力的な場面",
    "blood": "血や流血表現",
    "fight": "暴力行為",
}

OK_LABELS = [
    "safe photo",
    "child friendly photo",
    "normal photo"
]


def check_ng_image(image_path):
    labels = NG_LABELS + OK_LABELS

    image = Image.open(image_path)
    result = classifier(
        image,
        candidate_labels=labels
    )

    top = result[0]

    label = top["label"]
    score = top["score"]

    if label in NG_LABELS:
        reason = REASON_JA.get(
            label,
            "禁止されている可能性がある画像"
        )
        return True, reason, score
    
    return False, "問題なし", score