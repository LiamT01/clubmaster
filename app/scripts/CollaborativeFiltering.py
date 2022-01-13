from math import sqrt


class ItemBasedCF:
    def __init__(self):
        self.W = None
        self.train = None

    def setup(self, users):
        self.read_data(users)
        self.item_sim()

    # 读取文件，并生成usr-club评分映射
    def read_data(self, users):
        self.train = dict()
        # 遍历用户建立映射
        # users 是所有的用户对象
        # item_id 是user参加的社团id
        for user in users:
            self.train.setdefault(user.id, {})
            clubs = []
            clubs.extend(user.joined_clubs.all())
            clubs.extend(user.created_clubs.all())
            for club in clubs:
                self.train[user.id][club.name] = 1
                
    # 建立club-club的共现矩阵
    def item_sim(self):
        C = dict()  # club-club的共现矩阵
        N = dict()  # club中有多少不同用户
        for user, items in self.train.items():
            for club in items.keys():
                N.setdefault(club, 0)
                N[club] += 1
                C.setdefault(club, {})
                for another_club in items.keys():
                    if club == another_club:
                        continue
                    if another_club not in C[club].keys():
                        C[club].setdefault(another_club, 0)
                    C[club][another_club] += 1

        # 计算相似度矩阵
        self.W = dict()
        for club, related_items in C.items():
            self.W.setdefault(club, {})
            for another_club, cij in related_items.items():
                # 余弦相似度
                self.W[club][another_club] = cij / (sqrt(N[club] * N[another_club]))

    # 给定特定usr的活动轨迹(指其参与的club)，根据club相似度及rating计算评分，给出未参与的club中前N个
    def recommend(self, user, K=3, N=10):
        users = list(self.train.keys())

        rank = dict()
        # result = []
        # for user in users:
        action_item = self.train[user]  # 用户user产生过行为的item和评分
        for item, score in action_item.items():
            for j, wj in sorted(self.W[item].items(), key=lambda x: x[1], reverse=True):
                if j in action_item.keys():
                    continue
                if j not in rank.keys():
                    rank.setdefault(j, 0)
                rank[j] += score * wj
        result = list(dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]).keys())
        return None if result == [] else result


if __name__ == "__main__":
    CF = ItemBasedCF()
    CF.item_sim()
    result = CF.recommend()
    
    print(result)
    