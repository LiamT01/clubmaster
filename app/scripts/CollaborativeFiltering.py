from math import sqrt

class ItemBasedCF:
    def __init__(self):
        self.read_data()

    # 读取文件，并生成usr-club评分映射
    def read_data(self):
        self.train = dict()
        #遍历用户建立映射
        #users 是所有的用户id列表
        #item_id 是user参加的社团id
        for user_id in users:
            self.train.setdefault(user_id, {})
            for item_id in user_id.joined_clubs.all():
                self.train[user_id][item_id] = 1
                
    # 建立club-club的共现矩阵
    def item_sim(self):
        C = dict()  #club-club的共现矩阵
        N = dict()  #club中有多少不同用户
        for user, items in self.train.items():
            for i in items.keys():
                N.setdefault(i, 0)
                N[i] += 1
                C.setdefault(i, {})
                for j in items.keys():
                    if i == j :
                        continue
                    if j not in C[i].keys():
                        C[i].setdefault(j, 0)
                    C[i][j] += 1

        #计算相似度矩阵
        self.W = dict()
        for i,related_items in C.items():
            self.W.setdefault(i,{})
            for j,cij in related_items.items():
                # 余弦相似度
                self.W[i][j] = cij / (sqrt(N[i] * N[j]))

        return self.W

   #给定特定usr的活动轨迹(指其参与的club)，根据club相似度及rating计算评分，给出未参与的club中前N个
    def recommend(self,K=3,N=10):
        users = list(self.train.keys())

        rank = dict()
        result = []
        for user in users:
            action_item = self.train[user]     #用户user产生过行为的item和评分
            for item,score in action_item.items():
                for j,wj in sorted(self.W[item].items(),key=lambda x:x[1],reverse=True):
                    if j in action_item.keys():
                        continue
                    if j not in rank.keys():
                        rank.setdefault(j,0)
                    rank[j] += score * wj
            result.append(list(dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N]).keys())[0])
        return result
if __name__ == "__main__":

    CF = ItemBasedCF()
    CF.item_sim()
    result = CF.recommend()
    
    print(result)