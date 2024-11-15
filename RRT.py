import time
import math
import random
import numpy as np
import copy
import matplotlib.pyplot as plt
show_animation = True
class RRT:
    #初始化
    def __init__(self, obstacleList, randArea,
                 expandDis=2.0,  maxIter=200):
        self.start = None
        self.goal = None
        self.min_rand = randArea[0]#赋值采样范围最小值
        self.max_rand = randArea[1]#赋值采样范围最大值
        self.expand_dis = expandDis#设置采样步长，这里为2
        self.max_iter = maxIter#设置最大迭代次数为200轮
        self.obstacle_list = obstacleList
        self.node_list = None# 存储RRT树，也就是树上那些节点

    def rrt_planning(self, start, goal, animation=True):
        start_time = time.time()#计时，统计时间
        self.start = Node(start[0], start[1])#起点以Node的形式存储
        self.goal = Node(goal[0], goal[1])#终点以Node的形式存储
        self.node_list = [self.start]#起点加入node_list，作为树的根节点
        path = None

        for i in range(self.max_iter):#for循环，采样用
            #----------------------------sample----------------------------------#
            rnd = self.sample()#采样
            #--------------------------get_nearest_list_index--------------------#
            n_ind = self.get_nearest_list_index(self.node_list, rnd)#找离采样点最近的那个节点
            #------------------------node_list-----------------------------------#
            nearestNode = self.node_list[n_ind]#通过下标获得最近的节点，Xnear
            # steer
            theta = math.atan2(rnd[1] - nearestNode.y, rnd[0] - nearestNode.x)#y方向/x方向的反三角函数
            #-----------------------get_new_node---------------------------------#
            newNode = self.get_new_node(theta, n_ind, nearestNode)#从Xnear生长一段距离

            #检查新长成的这一段路径，Xnear到Xnew这一段是否有障碍物，有障碍物就抛弃这一次生长
            #-----------------------check_segment_collision----------------------#
            #检测有碰撞没
            noCollision = self.check_segment_collision(newNode.x, newNode.y, nearestNode.x, nearestNode.y)
            if noCollision:#如果没有碰撞假如rrt树
                self.node_list.append(newNode)
                if animation:
             #--------------------draw_graph-------------------------------------#
                    self.draw_graph(newNode, path)
                # 判断是否到达终点附近，即我们设置的提前停止的条件，
                if self.is_near_goal(newNode):#具体:判断我们新加入的点newNode是否和终点很接近
                    if self.check_segment_collision(newNode.x, newNode.y,
                                                    self.goal.x, self.goal.y):#连起来之后判断是否与障碍物发生碰撞
                        lastIndex = len(self.node_list) - 1#下标是从0开始的，索引我们需要从结点个数-1获得离终点最近的新加入的点的坐标
                        #------------get_final_course--------------#
                        path = self.get_final_course(lastIndex)#无碰撞就是找到了终点，就寻找这条路径，有碰撞进入下个循环
                        #----------get_path_len------------------------#
                        pathLen = self.get_path_len(path)
                        print("current path length: {}, It costs {} s".format(pathLen, time.time()-start_time))

                        if animation:
                            self.draw_graph(newNode, path)
                        return path


    def sample(self):
        rnd = [random.uniform(self.min_rand, self.max_rand), random.uniform(self.min_rand, self.max_rand)]
        return rnd

    @staticmethod
    def get_nearest_list_index(nodes, rnd):
        dList = [(node.x - rnd[0]) ** 2
                 + (node.y - rnd[1]) ** 2 for node in nodes]#for node in nodes遍历当前所有节点，然后计算节点和采样点的距离
        minIndex = dList.index(min(dList))#通过min函数获得最近的距离，通过index获得最近距离函数的下标，将下标返回
        return minIndex

    def get_new_node(self, theta, n_ind, nearestNode):  # 距离生长
        newNode = copy.deepcopy(nearestNode)  # 将最近的节点拷贝一份作为新节点

        newNode.x += self.expand_dis * math.cos(theta)  # 对新节点进行生长，x向
        newNode.y += self.expand_dis * math.sin(theta)  # y向

        newNode.cost += self.expand_dis  # 记录路径的长度，在原来cost上加上扩展的距离expand_dis
        newNode.parent = n_ind  # 记录它来自于哪个节点就是Xnear这个下标，用于最后的寻找路径
        return newNode  # 返回新节点



    def draw_graph(self, rnd=None, path=None):
        plt.clf()
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect(
            'key_release_event',
            lambda event: [exit(0) if event.key == 'escape' else None])
        if rnd is not None:
            plt.plot(rnd.x, rnd.y, "^k")

        for node in self.node_list:
            if node.parent is not None:
                if node.x or node.y is not None:
                    plt.plot([node.x, self.node_list[node.parent].x], [
                        node.y, self.node_list[node.parent].y], "-g")

        for (ox, oy, size) in self.obstacle_list:
            # self.plot_circle(ox, oy, size)
            plt.plot(ox, oy, "ok", ms=30 * size)

        plt.plot(self.start.x, self.start.y, "xr")
        plt.plot(self.goal.x, self.goal.y, "xr")

        if path is not None:
            plt.plot([x for (x, y) in path], [y for (x, y) in path], '-r')

        # plt.axis([0, 18, -2, 15])
        plt.axis([0, 50, 0, 30])
        plt.title("RRT")
        plt.grid(True)
        plt.pause(0.01)

    @staticmethod
    def line_cost(node1, node2):
        return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

    def is_near_goal(self, node):
    #-------------line_cost--------------------#
        d = self.line_cost(node, self.goal)#line_cost计算与终点的距离
        if d < self.expand_dis:#距离小于步长，直接和终点相连
            return True
        return False

    @staticmethod
    def distance_squared_point_to_segment(v, w, p):  # 计算障碍物碰撞距离的函数
        # Return minimum distance between line segment vw and point p
        if np.array_equal(v, w):
            return (p - v).dot(p - v)  # v == w case
        l2 = (w - v).dot(w - v)  # i.e. |w-v|^2 -  avoid a sqrt
        t = max(0, min(1, (p - v).dot(w - v) / l2))
        projection = v + t * (w - v)  # Projection falls on the segment
        return (p - projection).dot(p - projection)

    def check_segment_collision(self, x1, y1, x2, y2):#检查障碍物的方法，传入新生长路径的两个端点
        #我们的障碍物是用圆表示的，我们只要计算直线到圆心的距离，这个距离大于圆的半径就是无碰撞的
        for (ox, oy, size) in self.obstacle_list:#遍历所有的障碍物
            #---------------distance_squared_point_to_segment--------------------------#
            dd = self.distance_squared_point_to_segment(#distance_squared_point_to_segment具体计算距离的，传入的参数是两个点和圆心
                np.array([x1, y1]),
                np.array([x2, y2]),
                np.array([ox, oy]))
            if dd <= size ** 2:
                return False  # collision
        return True
    def get_final_course(self, lastIndex):
        path = [[self.goal.x, self.goal.y]]#存放终点
        while self.node_list[lastIndex].parent is not None:#每个结点初始化为NONE
            node = self.node_list[lastIndex]
            path.append([node.x, node.y])
            lastIndex = node.parent
        path.append([self.start.x, self.start.y])
        return path

    @staticmethod
    def get_path_len(path):
        pathLen = 0
        for i in range(1, len(path)):
            node1_x = path[i][0]
            node1_y = path[i][1]
            node2_x = path[i - 1][0]
            node2_y = path[i - 1][1]
            pathLen += math.sqrt((node1_x - node2_x)
                                 ** 2 + (node1_y - node2_y) ** 2)

        return pathLen

class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = 0.0
        self.parent = None



def main():
    print("Start rrt planning")


    obstacleList = [
        (3, 3, 1),
        (12, 2, 1),
        (3, 9, 1),
        (9, 11, 1),
        (12, 8, 1),
        (20, 12, 1),
        (40, 20, 1),
        (20, 20, 1.5),
        (30, 6, 1),
        (32, 22, 1),
        (20, 15, 1.5),
        (5, 17, 1),
        (32, 12, 2),
        (38, 28, 1),
        (35, 26, 1.5),
        (41, 26, 1),
        (40, 11, 1),
        (10, 19, 1),
        (32, 17, 1)

    ]

    #下面一行意思：RRT类里，randArea:采样范围设置，这里是0到50，obstacleList->障碍物，maxIter->迭代次数
    rrt = RRT(randArea=[0, 50], obstacleList=obstacleList, maxIter=300)
    path = rrt.rrt_planning(start=[5, 5], goal=[45, 25], animation=show_animation)#传入起点和终点

    print("Done!!!")
    print(rrt.node_list[len(rrt.node_list)-1].cost);
    if show_animation and path:
        plt.show()


if __name__ == '__main__':
    main()
