from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image

root = Path(__file__).resolve().parent
photos = {
    "yin-qiao.jpg": "https://www.sciencearts.com/shop/image/catalog/300s%20Capsules/300s%20Yinqiao-01.jpg",
    "huoxiang-zhengqi.jpg": "https://www.sciencearts.com/shop/image/catalog/2000s%20black%20bottle/2000s%20HuoXiang%20Zhengqi%20Wan.jpg",
}
for name, url in photos.items():
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
        data = response.read()
    path = root / name
    path.write_bytes(data)
    with Image.open(path) as image:
        print(name, image.size, image.format)
