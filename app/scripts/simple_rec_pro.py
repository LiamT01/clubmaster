import numpy as np
import random
import math
from ..models import User, Club

# 最简单版本，只推荐社团内成员
# 共同活动，相同兴趣
# 或许可以设定一下社团内推荐和社团外推荐的比例


class UsersRecommend:
    def __init__(self, uuid):
        self.uuid = uuid
        self.club_id = self.get_club_id(uuid)  # 1个同学可能加入多个社团
        self.club_member = {}
        self.hobby_w = 0.5
        self.act_w = 0.5
        self.recommends, self.recommends_idx = [], []
        self.act_my = self.get_activity(uuid)['name']
        for club_id in self.club_id:
            self.club_member[club_id] = self.get_club_member(club_id)  # 返回每个社团成员id的集合

    def recommend_f(self): # n表示推荐几个
        # =================================
        for club_id in self.club_id:
            for x in self.club_member[club_id]:  # x 代表成员的id
                if x == self.uuid:
                    continue
                if x not in self.recommends_idx: # 可能x已经在其他社团的遍历中被加到recommends_idx里了
                    self.recommends_idx.append(x)
                    self.recommends.append({'uid': x, 'club': club_id, 'score': 0, 'same_hobby_num': 0,
                                            'same_act_num': 0, 'same_activity': [], 'same_hobby': []})
                same_activity = self.get_same_activity(x, self.uuid, time=1)
                num_same_act = same_activity['num']
                name_same_act = same_activity['name']
                self.recommends[self.recommends_idx.index(x)]['same_act_num'] += num_same_act
                self.recommends[self.recommends_idx.index(x)]['same_activity'].extend(name_same_act)

                hobby_u = self.get_hobby(self.uuid)  # 0,1向量
                hobby_x = self.get_hobby(x)
                same_hobby_rate, same_hobby_num, same_hobby_name = self.get_same_hobby(hobby_u, hobby_x)
                # same_hobby_rate相当于是same_hobby_num的归一化，防止有人把所有的选项都选了
                self.recommends[self.recommends_idx.index(x)]['score'] \
                    += (pow(2, num_same_act)*self.act_w+same_hobby_num*same_hobby_rate*self.hobby_w)  # 可调

    def rec_top_n(self, n): # 规定n<=5
        self.recommends.sort(key=lambda r: r['score'], reverse=True)
        random_size = min(len(self.recommends), n + 3)
        recommends = self.recommends[:random_size]
        p_rec = []
        for i in range(len(recommends)):
            p_rec.append(recommends[i]['score'])
        p_rec = p_rec/np.sum(p_rec)
        """
        index = np.array([i for i in range(n)])
        random_size = min(len(self.recommends), n+3)
        top_n = np.random.choice(index, size=random_size, p=p_rec)
        """
        index = np.array([i for i in range(len(recommends))])

        real_size = min(len(recommends), n)
        top_n = np.random.choice(index, size=real_size, p=p_rec, replace=False)
        # top_n = self.recommends[:n]
        recommend_reason = []
        recommend_person = []
        for rec_id in top_n:
            rec = recommends[rec_id]
            recommend_person.append(rec['uid'])
            reason0 = '你们都在{}中'.format(rec['club'])
            reason1, reason2 = None, None
            same_hobby_name = rec['same_hobby']
            if rec['same_hobby_num'] == 1:
                reason1 = '你们在{}上有相同的爱好'.format(same_hobby_name[0])
            if rec['same_hobby_num'] > 1:
                reason1 = '你们有{}、{}等在内的{}个爱好相同'.format(
                    same_hobby_name[0], same_hobby_name[1], rec['same_hobby_num'])
            if len(rec['same_activity']) == 1:
                reason2 = '你们一起参加过{}'.format(
                    rec['same_activity'][0])
            if len(rec['same_activity']) > 1:
                reason2 = '你们有一起参加过{}、{}等在内的{}个活动'.format(
                    rec['same_activity'][0], rec['same_activity'][1], rec['same_act_num'])
            reasons = [reason for reason in (reason0, reason1, reason2) if reason is not None]
            reason = np.random.choice(reasons, size=1).item()
            recommend_reason.append(reason)
        return recommend_person, recommend_reason

    def get_club_member(self, club_id):
        club = Club.query.get(club_id)
        members = []
        members.extend(club.members.all())
        members.append(club.creator)
        return [member.id for member in members]
        # 根据社团id, 返回社团所有成员id

    def get_club_id(self, uuid):
        user = User.query.get(uuid)
        clubs = []
        clubs.extend(user.joined_clubs.all())
        clubs.extend(user.created_clubs.all())
        return [club.name for club in clubs]
        # 1个同学加入的多个社团的id

    def get_activity(self, uid, time=10000):  # time可选项，后续可以用来限定只选离现在time时间之内的活动
        activities = User.query.get(uid).joined_activities.all()
        return {'name': [activity.name for activity in activities], 'time': [activity.time for activity in activities]}
        # 形式为{'name':[ , , ,], 'time':[, , , ]}
        # 当然，如果不考虑time，直接返回[ , , ,]

    def get_same_activity(self, target_id, my_id, time):
        act_my = self.act_my
        act_target = self.get_activity(target_id)['name']
        act_my = set(act_my)
        act_target = set(act_target)
        same = list(act_my.intersection(act_target))
        return {'name': same, 'num': len(same)}

    def get_hobby(self, uid):
        hobby = np.array([0, 0, 1, 0, 0])
        return hobby
        # 输入个人id, 返回hobby的list
        # 假定有已知hobby列表比如[篮球、音乐、扑克、王者荣耀...], 那么返回[0 1 0 1...]表示hobby有“音乐、王者荣耀”

    def get_same_hobby(self, hobby_u, hobby_x):
        same_hobby = hobby_u * hobby_x
        num_u = np.sum(hobby_u)
        num_x = np.sum(hobby_x)
        same_num = np.sum(same_hobby)
        same_rate = same_num / math.sqrt(num_u * num_x)
        index = np.nonzero(same_hobby)
        return same_rate, same_num, index[0]

# 调试
# rec = UserRecommend(1) # 1代表个人id
# rec.recommend_f() # 完成构建，之后可以多次快速调用rec_top_n函数
# rec.rec_top_n(3) # 3表示推荐3位
