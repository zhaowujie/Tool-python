import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os

num = 0
numPicture = 0
file = ''
List = []


def Find(url):
    global List
    print('正在检测图片总数，请稍等.....')
    t = 0
    i = 1
    s = 0
    while t < 1000:
        Url = url + str(t)
        try:
            Result = requests.get(Url, timeout=7)
        except BaseException:
            t = t + 60
            continue
        else:
            result = Result.text
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)  # 先利用正则表达式找到图片url
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s


def recommend(url):
    Re = []
    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    Re.append(i.get_text())
        return Re


def dowmloadPicture(localPath, html, keyword):
    global num
    # t =0
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 先利用正则表达式找到图片url
    print('找到关键词:' + keyword + '的图片，即将开始下载图片...')
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片，图片地址:' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载')
            continue
        else:
            string = os.path.join(localPath, 'aug_img_%d.jpg' % num)
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return


if __name__ == '__main__':  # 主函数入口
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
    # word = input("请输入搜索关键词(可以是人名，地名等): ")
    for k, v in label_id_name_dict.items():
        sub_dir = 'E:\deeplearning\HUAWEIAI\data_augmentation\{}'.format(k)
        if os.path.exists(sub_dir):
            print('skipping {} {} ...'.format(k, v))
            continue
        else:
            os.mkdir(sub_dir)
            print('make dir {}'.format(sub_dir))
        # add = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E5%BC%A0%E5%A4%A9%E7%88%B1&pn=120'
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + v.split('/')[1] + '&pn='
        tot = Find(url)
        Recommend = recommend(url)  # 记录相关推荐
        print('经过检测%s类图片共有%d张' % (v.split('/')[1], tot))
        numPicture = 1000

        t = 0
        tmp = url
        while t < numPicture:
            try:
                url = tmp + str(t)
                result = requests.get(url, timeout=10)
                print(url)
            except error.HTTPError as e:
                print('网络错误，请调整网络后重试')
                t = t + 60
            else:
                dowmloadPicture(sub_dir, result.text, v.split('/')[1])
                t = t + 60

    print('当前搜索结束，感谢使用')
    # print('猜你喜欢')
    # for re in Recommend:
    #     print(re, end='  ')