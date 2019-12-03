# -*- coding=utf-8 -*-
import requests
import os
import json
from tqdm import tqdm

label_id_name_dict = \
        {
            "0": "工艺品/仿唐三彩",
            "1": "工艺品/仿宋木叶盏",
            "2": "工艺品/布贴绣",
            "3": "工艺品/景泰蓝",
            "4": "工艺品/木马勺脸谱",
            "5": "工艺品/柳编",
            "6": "工艺品/葡萄花鸟纹银香囊",
            "7": "工艺品/西安剪纸",
            "8": "工艺品/陕历博唐妞系列",
            "9": "景点/关中书院",
            "10": "景点/兵马俑",
            "11": "景点/南五台",
            "12": "景点/大兴善寺",
            "13": "景点/大观楼",
            "14": "景点/大雁塔",
            "15": "景点/小雁塔",
            "16": "景点/未央宫城墙遗址",
            "17": "景点/水陆庵壁塑",
            "18": "景点/汉长安城遗址",
            "19": "景点/西安城墙",
            "20": "景点/钟楼",
            "21": "景点/长安华严寺",
            "22": "景点/阿房宫遗址",
            "23": "民俗/唢呐",
            "24": "民俗/皮影",
            "25": "特产/临潼火晶柿子",
            "26": "特产/山茱萸",
            "27": "特产/玉器",
            "28": "特产/阎良甜瓜",
            "29": "特产/陕北红小豆",
            "30": "特产/高陵冬枣",
            "31": "美食/八宝玫瑰镜糕",
            "32": "美食/凉皮",
            "33": "美食/凉鱼",
            "34": "美食/德懋恭水晶饼",
            "35": "美食/搅团",
            "36": "美食/枸杞炖银耳",
            "37": "美食/柿子饼",
            "38": "美食/浆水面",
            "39": "美食/灌汤包",
            "40": "美食/烧肘子",
            "41": "美食/石子饼",
            "42": "美食/神仙粉",
            "43": "美食/粉汤羊血",
            "44": "美食/羊肉泡馍",
            "45": "美食/肉夹馍",
            "46": "美食/荞面饸饹",
            "47": "美食/菠菜面",
            "48": "美食/蜂蜜凉粽子",
            "49": "美食/蜜饯张口酥饺",
            "50": "美食/西安油茶",
            "51": "美食/贵妃鸡翅",
            "52": "美食/醪糟",
            "53": "美食/金线油塔"
        }

def getManyPages(keyword, pages):
    params = []
    for i in range(30, 30 * pages + 30, 30):
        params.append({
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'ct': 201326592,
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': 2,
            'lm': -1,
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': -1,
            'z': '',
            'ic': 0,
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': 0,
            'istype': 2,
            'qc': '',
            'nc': 1,
            'fr': '',
            'pn': i,
            'rn': 30,
            'gsm': '1e',
            '1488942260214': ''
        })
    url = 'https://image.baidu.com/search/acjson'
    urls = []
    for i in params:
        lists = requests.get(url, params=i)
        lists = lists.json()
        # lists = json.loads(lists, strict=False)
        lists = lists.get('data')
        urls.append(lists)

    return urls


def getImg(dataList, localPath):
    if not os.path.exists(localPath):  # 新建文件夹
        os.mkdir(localPath)
        print('make dir {}'.format(localPath))

    x = 0
    for list in dataList:
        for i in list:
            if i.get('thumbURL') != None:
                print('正在下载中：%s' % i.get('thumbURL'))
                ir = requests.get(i.get('thumbURL'))
                open(os.path.join(localPath, 'aug_img_%d.jpg' % x), 'wb').write(ir.content)
                x += 1
            else:
                print('该图片链接不存在')


if __name__ == '__main__':
    for k, v in label_id_name_dict.items():
        if os.path.exists('E:\deeplearning\HUAWEIAI\data_augmentation\{}'.format(k)):
            print('skipping {} {} ...'.format(k, v))
            continue
        # try:
        dataList = getManyPages(v.split('/')[1], 100)  # 参数1:关键字，参数2:要下载的页数
        getImg(dataList, 'E:\deeplearning\HUAWEIAI\data_augmentation\{}'.format(k))  # 参数2:指定保存的路径
        # except:
        #     print('get {} failed...'.format(v))