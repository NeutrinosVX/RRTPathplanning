class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # g值（起点到当前节点的实际代价）
        self.h = 0  # h值（当前节点到目标节点的估计代价）
        self.f = 0  # f值（g值加上h值）

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    # 创建起点和目标节点
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # 初始化开放和关闭节点集合
    open_list = []
    closed_list = []

    # 将起点加入开放节点集合
    open_list.append(start_node)

    while len(open_list) > 0:
        # 从开放节点集合中选择f值最小的节点作为当前节点
        current_node = open_list[0]
        current_index = 0
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        # 将当前节点从开放节点集合中移除，并加入到关闭节点集合中
        open_list.pop(current_index)
        closed_list.append(current_node)

        # 如果当前节点是目标节点，返回路径
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        # 生成当前节点的相邻节点
        neighbors = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # 确保节点在迷宫范围内
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # 确保节点不是墙
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # 创建新节点
            new_node = Node(current_node, node_position)

            # 加入相邻节点集合
            neighbors.append(new_node)

        # 处理相邻节点
        for neighbor in neighbors:
            # 如果相邻节点已在关闭节点集合中，忽略
            if neighbor in closed_list:
                continue

            # 计算相邻节点的g值、h值和f值
            neighbor.g = current_node.g + 1
            neighbor.h = ((neighbor.position[0] - end_node.position[0]) ** 2) + (
                        (neighbor.position[1] - end_node.position[1]) ** 2)
            neighbor.f = neighbor.g + neighbor.h

            # 如果相邻节点已在开放节点集合中且g值更大，忽略
            if any((neighbor == node and neighbor.g >= node.g) for node in open_list):
                continue

            # 将相邻节点加入开放节点集合
            open_list.append(neighbor)

    # 如果找不到路径，返回空
    return None


# 测试示例
maze = [[0,0,0,0,3,3,0,0,0], [0,0,3,0,0,0,0,0,0], [0, 0, 3, 3, 3, 0, 0, 3, 0],
              [0, 3, 3, 0, 0, 0, 0, 3, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 3, 3, 3, 0, 0],
              [0, 0, 0, 3, 0, 0, 0, 0, 3], [0, 1, 0, 0, 0, 3, 0, 0, 3], [0, 0, 0, 3, 3, 3, 3, 0, 0]];

start = (7, 1)
end = (4, 4)

path = astar(maze, start, end)
print(path)
