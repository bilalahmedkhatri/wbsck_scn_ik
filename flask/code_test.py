import uuid


def user_ID():
    u_ui = uuid.uuid4()

    for _ in range(5):
        print(u_ui)



user_ID()
