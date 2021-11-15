import grpc

from user_srv.proto import user_pb2_grpc, user_pb2

class UserTest:
    def __init__(self):
        channel = grpc.insecure_channel("127.0.0.1:50051")
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo(pn=1, pSize=2))
        print(rsp.total)
        for user in rsp.data:
            print(user.mobile, user.birthDay)


if __name__ == '__main__':
    user = UserTest()
    user.user_list()