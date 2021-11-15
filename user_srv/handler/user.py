import time

import grpc

from ..model.models import User
from ..proto import user_pb2, user_pb2_grpc


class UserServicer(user_pb2_grpc.UserServicer):
    def GetUserList(self, request: user_pb2.PageInfo, context):
        # 获取用户的列表
        rsp = user_pb2.UserListResponse()

        users = User.select()
        rsp.total = users.count()

        start = 0
        page = 1
        per_page_nums = 10
        if request.pSize:
            per_page_nums = request.pSize
        if request.pn:
            start = per_page_nums * (page - 1)

        users = users.limit(per_page_nums).offset(start)

        for user in users:
            user_info_rsp = user_pb2.UserInfoResponse()

            user_info_rsp.id = user.id
            user_info_rsp.passWord = user.password
            user_info_rsp.mobile = user.mobile
            user_info_rsp.role = user.role

            if user.nick_name:
                user_info_rsp.nickName = user.nick_name

            if user.gender:
                user_info_rsp.gender = user.gender

            if user.birthday:
                user_info_rsp.birthDay = int(time.mktime(user.birthday.timetuple()))

            rsp.data.append(user_info_rsp)
        return rsp