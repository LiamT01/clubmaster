import random


def mix(qalist: list):
    random.shuffle(qalist)
    return qalist

def fill(id: int, q_dict: dict, o_dict: dict, t_dict: dict):
    t_dict.update({str(id): dict()})
    t_dict[str(id)].update({'query': q_dict[str(id)]})
    t_dict[str(id)].update({'options': o_dict[str(id)]})

class question():
    def __init__(self, id: int, query: str, options: dict):
        self.id = id
        self.query = query
        self.options = options
    def list_options(self) -> str:
        option_list = []
        for key in self.options.keys():
            option_list.append(key + ') ' + self.options[key])
        return '\n'.join(option_list)

id = 0
query_dict = dict()
opt_dict = dict()
total_dict = dict()

#     layer id = 1
# id = 1
id += 1
query_dict.update({str(id): '以下哪些是你比较感兴趣的（可多选）'})
opt_dict.update({str(id): {'a': '体育健身', 'b': '时尚', 'c': '音乐', 'd': '信息科学', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 2
id += 1
query_dict.update({str(id): '以下哪些是你比较感兴趣的（可多选）'})
opt_dict.update({str(id): {'a': '电竞', 'b': '桌游棋牌', 'c': '绘画', 'd': '舞蹈', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 3
id += 1
query_dict.update({str(id): '以下哪些是你比较感兴趣的（可多选）'})
opt_dict.update({str(id): {'a': '传媒', 'b': '工业设计', 'c': '法律/文史/哲学', 'd': '表演/影视剧作', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 4
id += 1
query_dict.update({str(id): '平时你会花一些时间在哪些软件上（可多选）'})
opt_dict.update({str(id): {'a': 'B站', 'b': '知乎', 'c': '豆瓣', 'd': '贴吧', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 5
id += 1
query_dict.update({str(id): '平时你会花一些时间在哪些软件上（可多选）'})
opt_dict.update({str(id): {'a': '微博', 'b': '抖音', 'c': '快手', 'd': '小红书', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 6
id += 1
query_dict.update({str(id): '你的性别是'})
opt_dict.update({str(id): {'a': '男', 'b': '女', 'c': 'Both', 'd': '模糊不清的', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 7
id += 1
query_dict.update({str(id): '你的性取向是'})
opt_dict.update({str(id): {'a': '同性', 'b': '异性', 'c': 'Both', 'd': '模糊不清的', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})


#     layer id = 2
# id = 8
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '乒乓球', 'b': '足球', 'c': '篮球', 'd': '羽毛球', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 9
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '水上运动', 'b': '长跑越野', 'c': '极限运动', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 10
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '日韩穿搭', 'b': '欧美时装', 'c': '潮物', 'd': '奢侈品', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 11
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': 'K歌', 'b': '合唱', 'c': '演唱会', 'd': '作曲调音', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 12
id += 1
query_dict.update({str(id): '你比较常听的音乐类型可能有（可多选）'})
opt_dict.update({str(id): {'a': '流行', 'b': '古典', 'c': '嘻哈/电子', 'd': '小众其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 13
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '硬件设计', 'b': '算法开发', 'c': '互联网应用', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 14
id += 1
query_dict.update({str(id): '你可能喜欢花时间在（可多选）'})
opt_dict.update({str(id): {'a': '英雄联盟', 'b': '绝地求生', 'c': 'Dota', 'd': '我的世界', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 15
id += 1
query_dict.update({str(id): '你可能喜欢花时间在（可多选）'})
opt_dict.update({str(id): {'a': '炉石传说', 'b': 'CS', 'c': '堡垒之夜', 'd': '使命召唤', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 16
id += 1
query_dict.update({str(id): '你可能喜欢花时间在（可多选）'})
opt_dict.update({str(id): {'a': 'Steam', 'b': 'Taptap', 'c': '腾讯游戏', 'd': '网易游戏', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 17
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '经典棋类', 'b': '桌游', 'c': '牌类游戏', 'd': '普通手游', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 18
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '素描', 'b': '插画', 'c': '速写', 'd': '油画', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 19
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '街舞', 'b': '民族舞', 'c': '古典舞', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 20
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '演讲', 'b': '相声', 'c': '话剧', 'd': '脱口秀', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 21
id += 1
query_dict.update({str(id): '你可能了解一些（可多选）'})
opt_dict.update({str(id): {'a': '波普艺术', 'b': '经典砖墙风格', 'c': '日式设计', 'd': '欧美设计', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 22
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '中国古代文学历史', 'b': '西方近现代法律/哲学', 'c': '近现代/后现代文学', 'd': '其它文史哲学', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 23
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '电影/电视剧', 'b': '西方戏剧', 'c': '中国古代戏曲', 'd': '其它影视剧', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 24
id += 1
query_dict.update({str(id): '你是否会花一些时间在这些软件上（可多选）'})
opt_dict.update({str(id): {'a': 'Twitter', 'b': 'YouTube', 'c': 'Telegram', 'd': 'Instagram', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 25
id += 1
query_dict.update({str(id): '你可能喜欢观看哪些视频（可多选）'})
opt_dict.update({str(id): {'a': '科技科普', 'b': '搞笑/鬼畜/脑洞', 'c': '生活/娱乐/职业相关', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 26
id += 1
query_dict.update({str(id): '哪些话题/帖子可能吸引你（可多选）'})
opt_dict.update({str(id): {'a': '科技科普', 'b': '搞笑/鬼畜/脑洞', 'c': '生活/娱乐/职业相关', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 27
id += 1
query_dict.update({str(id): '哪些短视频可能吸引你（可多选）'})
opt_dict.update({str(id): {'a': '科技科普', 'b': '搞笑/鬼畜/脑洞', 'c': '生活/娱乐/职业相关', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 28
id += 1
query_dict.update({str(id): '你的形象可能比较接近于（可多选）'})
opt_dict.update({str(id): {'a': '爱好吃喝睡', 'b': '技术宅', 'c': '社交狂人', 'd': '自娱自乐', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})


#    layer id = 3
# id = 29
id += 1
query_dict.update({str(id): '如果给你十亿美元，你最有可能'})
opt_dict.update({str(id): {'a': '从事慈善事业', 'b': '环游世界，坐飞船去太空', 'c': '进军华尔街', 'd': '以上做法都太平庸了，不适合我', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 30
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '高尔夫', 'b': '网球', 'c': '台球', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 31
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '潮鞋', 'b': '滑板文化', 'c': '手办潮玩', 'd': '其它潮流', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 32
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '珠宝', 'b': '腕表', 'c': '香水', 'd': '奢侈衣帽鞋裤', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 33
id += 1
query_dict.update({str(id): '你可能喜欢哪些音乐（可多选）'})
opt_dict.update({str(id): {'a': '爵士/音乐剧', 'b': '中国传统民俗', 'c': '日韩', 'd': '拉美/非洲', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 34
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '象棋', 'b': '围棋', 'c': '五子棋', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 35
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '狼人杀', 'b': '阿瓦隆', 'c': '剧本杀', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 36
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '桥牌/德州', 'b': '斗地主', 'c': '麻将', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 37
id += 1
query_dict.update({str(id): '你可能感兴趣哪些舞种（可多选）'})
opt_dict.update({str(id): {'a': 'Popping', 'b': 'Hip-hop', 'c': '甩舞', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 38
id += 1
query_dict.update({str(id): '你可能感兴趣哪些舞种（可多选）'})
opt_dict.update({str(id): {'a': '芭蕾', 'b': '拉丁', 'c': '健美操', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 39
id += 1
query_dict.update({str(id): '你可能喜欢（可多选）'})
opt_dict.update({str(id): {'a': '韩剧', 'b': '美剧', 'c': '日剧', 'd': '国产剧/其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 40
id += 1
query_dict.update({str(id): '你可能感兴趣（可多选）'})
opt_dict.update({str(id): {'a': '京剧', 'b': '黄梅戏', 'c': '豫剧', 'd': '其它传统戏剧', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 41
id += 1
query_dict.update({str(id): '如果参加团建，你最喜欢的可能是（可多选）'})
opt_dict.update({str(id): {'a': '火锅/烧烤', 'b': 'KTV/轰趴', 'c': '剧本杀/密室逃脱', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})

# id = 42
id += 1
query_dict.update({str(id): '你擅长的知识领域可能有（可多选）'})
opt_dict.update({str(id): {'a': '理科', 'b': '工程技术', 'c': '设计/创作', 'd': '其它', 'e': '跳过'}})
total_dict.update({str(id): question(id, query_dict[str(id)], opt_dict[str(id)])})


ansdict = dict()

def LaunchTotal(id: int, ansdict = dict()):
    layer_id = 0

    if id == 1:
        layer_id = id
        dict_dict = dict()
        tmplist = [1, 2, 3, 4, 5, 6, 7]
        ttlist = mix(tmplist)
        for item in ttlist:
            fill(item, query_dict, opt_dict, dict_dict)
        return layer_id, ttlist, dict_dict

    if id == 2:
        layer_id = id
        dict_dict = dict()
        if ansdict != dict():
            tmplist = []
            if 'a' in ansdict['1']:
                tmplist.append(8)
                tmplist.append(9)
            if 'b' in ansdict['1']:
                tmplist.append(10)
            if 'c' in ansdict['1']:
                tmplist.append(11)
                tmplist.append(12)
            if 'd' in ansdict['1']:
                tmplist.append(13)
            if 'a' in ansdict['2']:
                tmplist.append(14)
                tmplist.append(15)
                tmplist.append(16)
            if 'b' in ansdict['2']:
                tmplist.append(17)
            if 'c' in ansdict['2']:
                tmplist.append(18)
            if 'd' in ansdict['2']:
                tmplist.append(19)
            if 'a' in ansdict['3']:
                tmplist.append(20)
            if 'b' in ansdict['3']:
                tmplist.append(21)
            if 'c' in ansdict['3']:
                tmplist.append(22)
            if 'd' in ansdict['3']:
                tmplist.append(23)
            if len(ansdict['4']) + len(ansdict['5']) > 3:
                tmplist.append(24)
            if 'a' in ansdict['4'] or 'b' in ansdict['4'] or 'a' in ansdict['5']:
                tmplist.append(25)
            if 'b' in ansdict['4'] or 'c' in ansdict['4'] or 'd' in ansdict['4'] or 'a' in ansdict['5']:
                tmplist.append(26)
            if 'b' in ansdict['5'] or 'c' in ansdict['5']:
                tmplist.append(27)
            tmplist.append(28)
            ttlist = mix(tmplist)
            for item in ttlist:
                fill(item, query_dict, opt_dict, dict_dict)
            return layer_id, ttlist, dict_dict
        else:
            return layer_id, [], dict_dict

    if id == 3:
        layer_id = id
        dict_dict = dict()
        if ansdict != dict():
            tmplist = []
            tmplist.append(29)
            if '9' in ansdict.keys():
                if 'd' in ansdict['9']:
                    tmplist.append(30)
            if '10' in ansdict.keys():
                if 'c' in ansdict['10']:
                    tmplist.append(31)
                if 'd' in ansdict['10']:
                    tmplist.append(32)
            if '12' in ansdict.keys():
                if 'd' in ansdict['12']:
                    tmplist.append(33)
            if '17' in ansdict.keys():
                if 'a' in ansdict['17']:
                    tmplist.append(34)
                if 'b' in ansdict['17']:
                    tmplist.append(35)
                if 'c' in ansdict['17']:
                    tmplist.append(36)
            if '19' in ansdict.keys():
                if 'a' in ansdict['19']:
                    tmplist.append(37)
                if 'd' in ansdict['19']:
                    tmplist.append(38)
            if '23' in ansdict.keys():
                if 'a' in ansdict['23']:
                    tmplist.append(39)
                if 'c' in ansdict['23']:
                    tmplist.append(40)
            if '28' in ansdict.keys():
                if 'a' in ansdict['28'] or 'c' in ansdict['28']:
                    tmplist.append(41)
                if 'b' in ansdict['28']:
                    tmplist.append(42)
            ttlist = mix(tmplist)
            for item in ttlist:
                fill(item, query_dict, opt_dict, dict_dict)
            return layer_id, ttlist, dict_dict
        else:
            return layer_id, [], dict_dict

if __name__ == '__main__':
    result_1_1, result_1_2, result_1_3 = LaunchTotal(1)
    print(result_1_1)
    print(result_1_2)
    print(result_1_3)

    result_2_1, result_2_2, result_2_3 = LaunchTotal(2)
    print(result_2_1)
    print(result_2_2)
    print(result_2_3)

    result_3_1, result_3_2, result_3_3 = LaunchTotal(3)
    print(result_3_1)
    print(result_3_2)
    print(result_3_3)
