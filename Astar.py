import Config
import Map
import Method

class Astar:
    """利用 A* 算法为怪物计算最短路径"""
    def __init__(self, Spos: tuple, Tpos: tuple) -> None: # 从 S 走到 T 给出一个最短路径
        self.s_pos_xy = Spos
        self.t_pos_xy = Tpos # 地图坐标

        self.s_pos = Method.get_block_xy(*Spos) # 网格坐标
        self.t_pos = Method.get_block_xy(*Tpos)
        self.node_list = [] # 记录一个结点序列，然后每次在这个节点序列上进行启发式拓展
        self.pre_map = {} # 为每个结点记录
    
    def __find_min_index(self):
        """在 node_list 中找到 c_hat 最小的数据"""
        c_hat_now = Map.get_maxlen() * 3 # 一个很大的最大距离
        pos = -1
        for i in range(0, len(self.node_list)):
            x, y, c_hat, dep = self.node_list[i] # c_hat 是距离的一个下界
            if c_hat < c_hat_now:
                c_hat_now = c_hat
                pos = i # 记录当前的 id
        return pos

    def __push_into_queue(self, x, y, c_hat, dep, pre_node):
        if self.pre_map.get((x, y)) == None: # 当前结点还没有被访问到了
            self.pre_map[(x, y)] = pre_node
            self.node_list.append((x, y, c_hat, dep)) # node_map 记录已经被访问的结点, node_list 记录当前所有活结点

    def __is_t(self, idx):
        """判断当前是否找到了目标位置"""
        x, y, c_hat, dep = self.node_list[idx]
        return (x, y) == self.t_pos # 检查是不是终点

    def __expand(self, idx):
        """对下标为 idx 的位置进行拓展"""
        x, y, c_hat, dep = self.node_list[idx]
        if(dep < Config.MAX_SEARCH_DEPTH):
            dir_xy = [(1, 0), (-1, 0), (0, -1), (0, 1)]
            for dx, dy in dir_xy: # 计算各个方向的拓展
                nx = x + dx
                ny = y + dy
                if(Map.map_of_objects.get((nx, ny)) == None or
                    Map.map_of_objects[(nx, ny)] in Config.PASSABLE): # 判断目标点是否没有真该五
                    ndep = dep + 1
                    n_c_hat = ndep + Method.L1_dis((nx, ny), self.t_pos)
                    self.__push_into_queue(nx, ny, n_c_hat, ndep, (x, y)) # 推入队列
                    pass

    def __get_dir_path(self): # 找到一条可行路径
        nx, ny = self.t_pos
        path = []
        while (nx, ny) != (None, None):
            path.append((nx, ny))
            nx, ny = self.pre_map[(nx ,ny)] # 得到前驱结点
        mid_of_next = Method.get_mid_of_block(path[-2])
        return Method.normalize(Method.vec_sub(mid_of_next, self.s_pos_xy)) # 走向下一个格子的中心点

    def solve(self):
        """计算最短路径的初始朝向"""
        if Method.L1_dis(self.s_pos, self.t_pos) <= Config.MAX_SEARCH_DEPTH:
            if self.s_pos == self.t_pos: # 在同一个格子，还不能互相看见，那就别走了
                return (0, 0)
            self.__push_into_queue(*self.s_pos, Method.L1_dis(self.s_pos, self.t_pos), 0, (None, None))
            while len(self.node_list) > 0:
                idx = self.__find_min_index() # 找到 c_hat 最小的元素的下标
                if self.__is_t(idx):
                    return self.__get_dir_path() # 找到了一条路径
                self.__expand(idx)
                del self.node_list[idx] # 删掉对应的节点
                pass
            return (0, 0) # MAX_SEARCH_PATH 步内走不到，那就别走了
        else:
            bmx, bmy = Method.get_mid_of_block(self.s_pos)
            return (bmx, bmy) # 返回目标位置