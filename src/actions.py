
def forward(rob,v=10, milliseconds=2500):
    rob.move(v, v, milliseconds)


def softRight(rob):
    rob.move(20, -20, 1250)


def hardRight(rob):
    rob.move(20, -20, 2250)


def softLeft(rob):
    rob.move(-20, 20, 1250)


def hardLeft(rob):
    rob.move(-20, 20, 2250)


def backward(rob,v=10, milliseconds=2500):
    rob.move(-v, -v, milliseconds)

action_dict = {0: forward, 1:backward, 2:hardRight, 3:softRight, 4:hardLeft, 5:softLeft}

def selectMove(rob, action):
    action_dict[action](rob)