from time import time
import gym
from numpy.lib.function_base import angle
from AgentAI.connect.BusConnect import BusConnect
from aiframework.AIFrameWork import ENV_STATE_OVER, ENV_STATE_PLAYING  
from actionmanager import ActionOpenAIController
from util import util
import numpy as np
from AgentAPI import AgentAPIMgr

from .GameEnv import GameEnv
from gym import spaces
import os
import time
import cv2
import collections
import math
from protocol import common_pb2

ACTION_CFG_FILE = 'cfg/task/agent/OpenAIPPOAction.json'
LEARNING_CFG_FILE = 'cfg/task/agent/OpenAIPPOLearning.json'
TASK_CFG_FILE = 'cfg/task/gameReg/Task.json'
REG_GROUP_ID = 1
GAME_STATE_INVALID = 0
GAME_STATE_RUN = 1
GAME_STATE_WIN = 2
GAME_STATE_LOSE = 3
GAME_STATE_DIE = 4
POSSIBLE_TIME_COOLDOWN = 90#Thoi gian hoi chieu dai nhat co the


class OpenAIEnv(gym.Env,GameEnv):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(OpenAIEnv, self).__init__()
        self._LoadCfgFilePath()
        self._LoadEnvParams()
        self.__gameState = None
        self._msgid = -1
        self.__actionController = ActionOpenAIController.ActionOpenAIController()
        self.__actionController.Initialize(self.__actionCfgFile)
        self.action_in_config = self.__actionController.get_action_dict()
        # self.Reset()#gym auto call reset() func
        self.__agentAPI = AgentAPIMgr.AgentAPIMgr()

        # self.logger.debug("Init action space %d", self.GetActionSpace())
        #Accepts multiple discrete or box,
        #Because the joytick is circular, get the upper and lower bounds based on the length and width of the square
        self.action_space = self.GetActionSpace()
        #hardcode HSV detect map object 
        #full map 
        # H 0,180
        # S 135,255
        # V 114,255
        self._low_H = 0
        self._high_H = 180
        self._low_S = 135
        self._high_S = 255
        self._low_V = 114
        self._high_V = 255
        self._timeout_ha_tru = 0
        

    def step(self, action):
        #decode action
        self.DoAction(action)
        img, reward, is_done = self.GetState()
        game_info = self._GetGameInfo()
        
        if self._msgid == common_pb2.MSG_UI_GAME_OVER and is_done == False:
            is_done = True
        if is_done == True:
            self.UpdateEnvState(ENV_STATE_OVER, 'Episode over')#use callback to send sate
        return img, reward, is_done, game_info
    #reset function openai
    def reset(self):
        self.Reset()
        
        img, reward, is_done = self.GetState()
        return img  # reward, done, info can't be included


    def render(self, mode='human'):
        pass
    def close (self):
        pass

    def Init(self):
        """
        Initialize game env object, create recognize task use AgentAPI
        """
        ret = self.__agentAPI.Initialize(self.__recognizeCfgFile)
        if not ret:
            self.logger.error('Agent API Init Failed')
            return False

        ret = self.__agentAPI.SendCmd(AgentAPIMgr.MSG_SEND_GROUP_ID, REG_GROUP_ID)
        if not ret:
            self.logger.error('send message failed')
            return False
        
        ###
        # Example for using image as input:
        # Chi su dung map tren hinh anh
        # Nó đã bao gồm
        # - Vị trí tướng ta, tướng địch
        # - Mau dich, mau ta
        # - Vị Trí lính, quái
        # - Máu trụ, vị trí trự
        # xác đinh size của bản đồ làm observer space
        # hardcode TaskID của bản đồ trong SDK UI là: 6 at index 2
        taskConfigs = self.__agentAPI.getTaskInConfig()
        # tim taskid 6
        for i in taskConfigs:
            if i['taskID'] == 6:
                # taskConfig[2] 'ROI': {'x': 0, 'y': 0, 'w': 231, 'h': 237}
                map_ROI = i['elements'][0]['ROI']
                self._map_ROI_w =  map_ROI['w']
                self._map_ROI_h =  map_ROI['h']
                self._map_ROI_x =  map_ROI['x']
                self._map_ROI_y =  map_ROI['y']
                full_path_to_mask = util.ConvertToSDKFilePath(i['elements'][0]['templates'][0]['path'])
                self._map_mask = cv2.imread(full_path_to_mask,cv2.IMREAD_GRAYSCALE)
                # self.observation_space = spaces.Box(low=0, high=255,
                #                                     shape=(self._map_ROI_h, self._map_ROI_w), dtype=np.uint8)
                self.observation_space = spaces.Box(low=0, high=255,
                                                    shape=(128, 128), dtype=np.uint8)

        return True

    def Finish(self):
        """
        Exit game env after object used, release AgentAPI
        """
        self.__agentAPI.Release()

    def GetActionSpace(self):
        """
        Return to gym space
        Action dict like:
        {4: {'id': 4, 'name': 'dichuyen', 'contact': 0, 'sceneTask': '', 'type': 'joystick', 'actionRegion': {'path': 'data/images/snapshot_1629207134.jpg', 'quantizeNumber': 1, 'center': {'x': 155, 'y': 590}, 'inner': {'x': 120, 'y': 558, 'w': 74, 'h': 69}, 'outer': {'x': 0, 'y': 442, 'w': 301, 'h': 277}}, 'durationMS': 0}, 1: {'id': 1, 'name': 'c1', 'contact': 0, 'sceneTask': '', 'type': 'click', 'actionRegion': {'path': 'data/images/daymau.jpg', 'region': {'x': 923, 'y': 592, 'w': 71, 'h': 75}}, 'durationMS': 0}, 2: {'id': 2, 'name': 'c2', 'contact': 0, 'sceneTask': '', 'type': 'click', 'actionRegion': {'path': 'data/images/daymau.jpg', 'region': {'x': 1007, 'y': 476, 'w': 52, 'h': 48}}, 'durationMS': 20}, 3: {'id': 3, 'name': 'danhthuong', 'contact': 0, 'sceneTask': '', 'type': 'click', 'actionRegion': {'path': 'data/images/snapshot_1629207134.jpg', 'region': {'x': 1167, 'y': 601, 'w': 50, 'h': 46}}, 'durationMS': 0}, 0: {'id': 0, 'name': 'none', 'type': 'none'}}
        """
        
        self._actions = []
        di_chuyen_id = 4
        duong_tron_dos = []
        for d in range(60):
            duong_tron_dos.append(d*6)

        for n in duong_tron_dos:
            self._actions.append([di_chuyen_id,n,0,0])#chi duy chuyen khong nhan nut
        
        for rdichuyen1 in duong_tron_dos:#di chuyen c1, ID 1 trong giao dien
            self._actions.append([di_chuyen_id,rdichuyen1,1])

        for rdichuyen2 in duong_tron_dos:#di chuyen c2, ID 2 trong giao dien
            self._actions.append([di_chuyen_id,rdichuyen2,2])

        for rdichuyen3 in duong_tron_dos:#di chuyen c2, ID 5 trong giao dien
            self._actions.append([di_chuyen_id,rdichuyen3,5])

        for rdichuyen3 in duong_tron_dos:# danh thuong va di chuyen
            self._actions.append([di_chuyen_id,rdichuyen3,3])  
        
        #cai dat cac nut binh thuong 
        self._actions.append([0,0,0,0])#khong di chuyen
        # self._actions.append([0,0,3,0])#danh thuong
        self._actions.append([0,0,6,0])#nang chieu 1
        self._actions.append([0,0,7,0])#nang chieu 2
        self._actions.append([0,0,8,0])#nang chieu 3

        self._actions.append([0,0,9,0])#boc pha id 9
        self._actions.append([0,0,10,0])#goi mau id 10

        self._actions.append([0,0,11,0])#bien ve nha 11
        self._actions.append([0,0,12,0])#mua do 12


        # spaces.MultiDiscrete([3,270,270,100])
        return spaces.Discrete(len(self._actions))

    def DoAction(self, actions, *args, **kwargs):
        """
        Output game action use ActionAPI
        action: one hot vector [x,y,z...]
        """

        acts = self._actions[actions]
        right_action = acts[2]
        left_action = acts[0]
        if right_action == 0 and left_action == 0:
            self.__actionController.DoAction(0, frameSeq=self.__frameIndex)#0 is none action
        elif right_action == 0 and left_action != 0:
            self.__actionController.DoAction(right_action, frameSeq=self.__frameIndex)#once action
        elif right_action != 0 and left_action != 0:
            self.__actionController.DoAction(left_action, angle=acts[1])#chay hanh dong ben trai action
            self.__actionController.DoAction(right_action,angle=acts[1],frameSeq=self.__frameIndex,joystick_like_swipe=True)#once action

        

    def ResetAction(self):
        """
        Reset game action use ActionAPI
        """
        self.__actionController.Reset()

    def StopAction(self):
        """1
        Stop game action when receive special msg or signal
        """
        self.__actionController.Reset()

    def RestartAction(self):
        """
        Restart output game action when receive special msg or signal
        """
        self.__actionController.Reset()

    def GetState(self):
        """
        Return (s, r, t): game image, reward, terminal
        [result] {"1": [{"flag": true, "ROI": {"x": 541, "y": 240, "w": 193, "h": 64}, "boxes": [{"tmplName": "", "score": 0.8268243074417114, "scale": 1.0, "classID": 0, "x": 594, "y": 270, "w": 101, "h": 11}]}], "2": [{"flag": false, "ROI": {"x": 447, "y": 594, "w": 387, "h": 101}, "boxes": []}], "3": [{"flag": false, "ROI": {"x": 221, "y": 216, "w": 771, "h": 256}, "boxes": []}], "4": [{"flag": false, "ROI": {"x": 293, "y": 230, "w": 679, "h": 258}, "boxes": []}], "5": [{"flag": true, "num": 352.0, "x": 5, "y": 306, "w": 88, "h": 35}], "6": [{"flag": true, "ROI": {"x": 0, "y": 0, "w": 231, "h": 237}, "boxes": [{"tmplName": "", "score": 0.8643749952316284, "scale": 1.3571428060531616, "classID": 0, "x": 73, "y": 129, "w": 19, "h": 19}, {"tmplName": "", "score": 0.8487499952316284, "scale": 1.3717105388641357, "classID": 0, "x": 13, "y": 177, "w": 26, "h": 33}, {"tmplName": "", "score": 0.8487499952316284, "scale": 1.3571428060531616, "classID": 0, "x": 61, "y": 145, "w": 19, "h": 19}, {"tmplName": "", "score": 0.8331249952316284, "scale": 1.3717105388641357, "classID": 0, "x": 109, "y": 89, "w": 26, "h": 33}]}], "7": [{"flag": true, "percent": 100.0, "ROI": {"x": 558, "y": 257, "w": 164, "h": 36}, "box": {"x": 596, "y": 272, "w": 120, "h": 8}}]}
        """
        is_done = False
        game_info = self._GetGameInfo()
        ressults = game_info['result']
        data = ressults.get(self.__scoreTaskID)[0]['num']
        image = game_info['image']
        self.__frameIndex = game_info['frameSeq']
        state = self.__gameState

        img_height = image.shape[0]
        img_width = image.shape[1]

        self.logger.debug("the width %d and the height %d of real image", img_width, img_height)
        self.__actionController.SetSolution(img_width, img_height)

        #crop only map image
        # Use therhold by HSV to locate objects like houses, enemy champions, our champions, health etc 

        #full map 
        # H 0,180
        # S 135,255
        # V 114,255
        img = image[self._map_ROI_y:self._map_ROI_y+self._map_ROI_h, self._map_ROI_x:self._map_ROI_x+self._map_ROI_w]
        
        frame_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(frame_HSV, (self._low_H, self._low_S, self._low_V), (self._high_H, self._high_S, self._high_V))
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = img[self.__beginRow:self.__endRow, self.__beginColumn:self.__endColumn]
        # if img_width < img_height:
        #     img = cv2.transpose(img)
        #     img = cv2.flip(img, 1)
        
        # Them maunv idstask 7 vao obs
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        
        # mask rececure
        # H 0,180
        # S 0,93
        # V 0,43
        
        re_mask = cv2.inRange(frame_HSV, (0, 0, 0), (180, 93, 43))
        # cv2.add(re_mask,gray_img,dst=frame_threshold)
        # add to mask 
        cv2.add(gray_img,self._map_mask,dst=frame_threshold)
        
        #dilaton
        dilatation_size = 1
        dilation_shape = cv2.MORPH_RECT
        element_dilatatio = cv2.getStructuringElement(dilation_shape, (2 * dilatation_size + 1, 2 * dilatation_size + 1),
                                        (dilatation_size, dilatation_size))
        frame_threshold = cv2.dilate(frame_threshold, element_dilatatio)
        frame_threshold = cv2.resize(frame_threshold,(128, 128))

        tgian_hoi_chieu_1 = util.get_number_dict(ressults,8)
        tgian_hoi_chieu_2 = util.get_number_dict(ressults,9)
        tgian_hoi_chieu_3 = util.get_number_dict(ressults,10)

        #lay thong tin mau, toa do dich
        # taskID 7 su dung yolo do tim mau nhan vat
        # "7": [{"flag": true, "ROI": {"x": 0, "y": 1, "w": 1280, "h": 720}, "bloods": [{"level": 0, "score": 0.9458652138710022, "percent": 60.0, "classID": 1, "name": "GreenBlood", "x": 567, "y": 260, "w": 161, "h": 34}]}]
        # max 4 blue
        # max 5 red co the la rong
        # Mỗi nhân vật sẽ có. khoảng cách(px), góc 360ĐỘ, phần trăm(0-100) máu từ nhân vật chính đến nhân vật được dò tìm.
        # Tinh từ GreenBlood  nhân vật chính


        #scale to 255
        # frame_threshold[0][1] = int(util.get_number_percent(ressults,7)*255/100)#phan tram mau nhan vat
        mau_nv = ressults.get(7)
        frame_threshold[2][1] = int((tgian_hoi_chieu_1 / POSSIBLE_TIME_COOLDOWN *100)*255/100)
        frame_threshold[3][1] = int((tgian_hoi_chieu_2 / POSSIBLE_TIME_COOLDOWN *100)*255/100)
        frame_threshold[4][1] = int((tgian_hoi_chieu_3 / POSSIBLE_TIME_COOLDOWN *100)*255/100)

        # Xem obs
        cv2.imshow("Openai LQ obs space", frame_threshold)
        cv2.waitKey(1)
        # img = cv2.resize(img, (self._inputImgWidth, self._inputImgHeight),interpolation=cv2.INTER_AREA)
        reward = self._CaculateReward(data)

        #Nếu trụ bị phá thì +maxreward
        state_ha_tru,px, py =  util.get_button_state(ressults,11)
        if state_ha_tru:
            if self._timeout_ha_tru == 0:
                if reward < self.__maxRunningReward:
                    reward == self.__maxRunningReward
            self._timeout_ha_tru = 1
        else:
            self._timeout_ha_tru = 0
        ##################################
        #han che cach hanhg dong khong can thiet
        

        self.__isTerminal = True
        if state == GAME_STATE_LOSE:
            is_done = True
            reward = self.__loseReward
        elif state == GAME_STATE_WIN:
            is_done = True
            reward = self.__winReward
        elif state == GAME_STATE_RUN:
            self.__isTerminal = False
        else:
            self.logger.error('error game state: %d', state)

        if data == -1 and self.__isTerminal is not True:
            self.logger.debug('detect data -1, set 0 reward')
            reward = 0

        self.logger.debug('data: {0} reward: {1}'.format(data, reward))
        if is_done == True:
            print("goi loi ne ")
        return frame_threshold, reward, is_done


    def Reset(self):
        """
        Reset date, action or state in game env
        """
        self.__lastScore = self.__initScore
        self.__lastRewardScore = self.__initScore
        self.__scoreRepeatedTimes = 0
        self.__isTerminal = True
        self.__gameState = GAME_STATE_INVALID
        self.__actionController.Reset()
        while self.IsEpisodeStart() == False:
            pass#do nothing waiting for game start
        self.UpdateEnvState(ENV_STATE_PLAYING, 'Episode start, ai playing')


    def IsTrainable(self):
        """
        Check whether the game state can used for training DQN model or not
        """
        return True

    def IsEpisodeStart(self):
        """
        Check whether episode start or not, according to recognize resulet
        """
        self._GetGameInfo()
        if self.__gameState == GAME_STATE_RUN:
            self.__isTerminal = False
            return True
        # if self.__gameState == GAME_STATE_WIN or self.__gameState == GAME_STATE_LOSE:
        #     self.__isTerminal = True
        #     return False
        return False

    def IsEpisodeOver(self):
        """
        Check whether episode over or not, according to recognize resulet
        """
        return self.__isTerminal


    def _GetGameInfo(self):

        while True:
            gameInfo = self.__agentAPI.GetInfo(AgentAPIMgr.GAME_RESULT_INFO)
            if gameInfo is None:
                time.sleep(0.002)
                continue

            result = gameInfo['result']
            self.logger.debug('The result of game reg is {0}'.format(result))
            if result is None:
                time.sleep(0.002)
                continue

            flag, _, _ = util.get_button_state(result, self.__startTaskID)
            if flag is True:
                self.__gameState = GAME_STATE_RUN
                self.logger.debug('frameindex = %d, detect begin', gameInfo['frameSeq'])

            flag, _, _ = util.get_button_state(result, self.__winTaskID)
            if flag is True:
                self.__gameState = GAME_STATE_WIN
                self.logger.debug('frameindex = %d, detect win', gameInfo['frameSeq'])

            flag, _, _ = util.get_button_state(result, self.__loseTaskID)
            if flag is True:
                self.__gameState = GAME_STATE_LOSE
                self.logger.debug('frameindex = %d, detect lose', gameInfo['frameSeq'])

            data = None
            if result.get(self.__scoreTaskID) is not None:
                data = result.get(self.__scoreTaskID)[0]

            if data is None:
                time.sleep(0.002)
                continue
            else:
                break

        self.update_scene_task(result, self.__actionController.get_action_dict(), self.__agentAPI)
        return gameInfo

    def _LoadEnvParams(self):
        if os.path.exists(self.__envCfgFile):
            config = util.get_configure(self.__envCfgFile)
            #config from UI
            self.__beginColumn = config['roiRegion']['region']['x']
            self.__beginRow = config['roiRegion']['region']['y']
            self.__cutWidth = config['roiRegion']['region']['w']
            self.__cutHeight = config['roiRegion']['region']['h']
            self.__endColumn = self.__beginColumn + self.__cutWidth
            self.__endRow = self.__beginRow + self.__cutHeight
            self._inputImgWidth = config['network']['inputImgWidth']
            self._inputImgHeight = config['network']['inputImgHeight']

            self.__initScore = config['excitationFunction']['initScore']
            self.__maxScoreRepeatedTimes = config['excitationFunction']['maxScoreRepeatedTimes']
            self.__rewardOverRepeated = config['excitationFunction']['rewardOverRepeatedTimes']

            self.__winReward = config['excitationFunction']['winReward']
            self.__loseReward = config['excitationFunction']['loseReward']

            self.__maxRunningReward = config['excitationFunction']['maxRunningReward']
            self.__minRunningReward = config['excitationFunction']['minRunningReward']
            self.__rewardPerPostive = config['excitationFunction']['rewardPerPostiveSection']
            self.__rewardPerNegtive = config['excitationFunction']['rewardPerNegtiveSection']
            self.__scorePerSection = config['excitationFunction']['scorePerSection']
            self.__scoreTaskID = config['excitationFunction']['scoreTaskID']
            self.__winTaskID = config['excitationFunction']['winTaskID']
            self.__loseTaskID = config['excitationFunction']['loseTaskID']
            self.__startTaskID = config['excitationFunction']['startTaskID']

            # self.logger.debug("__beginColumn is %d", self.__beginColumn)
            # self.logger.debug("__beginRow is %d", self.__beginRow)
            # self.logger.debug("__cutWidth is %d", self.__cutWidth)
            # self.logger.debug("__cutHeight is %d", self.__cutHeight)
            # self.logger.debug("__endColumn is %d", self.__endColumn)
            # self.logger.debug("__endRow is %d", self.__endRow)

            # self.logger.debug("__initScore is %s", str(self.__initScore))
            # self.logger.debug("__maxScoreRepeatedTimes is %s", str(self.__maxScoreRepeatedTimes))
            # self.logger.debug("__rewardOverRepeated is %s", str(self.__rewardOverRepeated))
            # self.logger.debug("__winReward is %s", str(self.__winReward))
            # self.logger.debug("__loseReward is %s", str(self.__loseReward))
            # self.logger.debug("__maxRunningReward is %s", str(self.__maxRunningReward))
            # self.logger.debug("__minRunningReward is %s", str(self.__minRunningReward))
            # self.logger.debug("__rewardPerPostive is %s", str(self.__rewardPerPostive))
            # self.logger.debug("__rewardPerNegtive is %s", str(self.__rewardPerNegtive))
            # self.logger.debug("__scorePerSection is %s", str(self.__scorePerSection))
            # self.logger.debug("__scoreTaskID is %s", str(self.__scoreTaskID))
            # self.logger.debug("__winTaskID is %s", str(self.__winTaskID))
            # self.logger.debug("__loseTaskID is %s", str(self.__loseTaskID))
            # self.logger.debug("__startTaskID is %s", str(self.__startTaskID))
        else:
            self.logger.error('dqn_env cfg file not exist.')

    def _CaculateReward(self, curScore):
        reward = 0
        self.logger.debug("the curScore is %s and lastRewardScore is %s", str(curScore), str(self.__lastRewardScore))
        if abs(curScore - self.__lastRewardScore) >= self.__scorePerSection:
            if curScore > self.__lastRewardScore:
                sections = int((curScore - self.__lastRewardScore)/self.__scorePerSection)
                reward = sections * self.__rewardPerPostive
            else:
                sections = int((self.__lastRewardScore - curScore)/self.__scorePerSection)
                reward = sections * self.__rewardPerNegtive

            self.__lastRewardScore = curScore

            if reward > self.__maxRunningReward:
                reward = self.__maxRunningReward
            elif reward < self.__minRunningReward:
                reward = self.__minRunningReward

        if self.__lastScore == curScore:
            self.__scoreRepeatedTimes += 1
            if self.__scoreRepeatedTimes >= self.__maxScoreRepeatedTimes:
                reward = self.__rewardOverRepeated
        else:
            self.__scoreRepeatedTimes = 0

        self.__lastScore = curScore

        self.logger.debug("the reward is %s", str(reward))
        return reward

    def _LoadCfgFilePath(self): 
        self.__actionCfgFile = util.ConvertToProjectFilePath(ACTION_CFG_FILE)
        self.__envCfgFile = util.ConvertToProjectFilePath(LEARNING_CFG_FILE)
        self.__recognizeCfgFile = util.ConvertToProjectFilePath(TASK_CFG_FILE)
    
    def setMSGID(self,msgid):
        self._msgid = msgid
    
    def nhanVatDetect(self,results_dict):
        # bloods: [{"level": 0, "score": 0.9458652138710022, "percent": 60.0, "classID": 1, "name": "GreenBlood", "x": 567, "y": 260, "w": 161, "h": 34}]}]
        # Tim  GreenBlood 
        bloods_lists = results_dict[0]['bloods']
        {k: v for k, v in sorted(bloods_lists.items(), key=lambda item: item[1])}
        greemBlood = {}
        for bl in  bloods_lists:
            if bl['name'] == 'GreenBlood':
                greemBlood = bl
                break
        
        # for i in range(4):#4 tuong ta
            

    def _angle_between(p1, p2):
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return np.rad2deg((ang1 - ang2) % (2 * np.pi))

    def distance_2_object(self, rect_obj1, rect_obj2):
        x1, y1 = self._calulator_center_point(rect_obj1)
        x2, y2 = self._calulator_center_point(rect_obj2)
        #tinh khoan cach
        distance  = math.sqrt(pow(x2 -x1) + pow(y2-y1))
        point1 = (x1,y1)
        point2 = (x2, y2)
        angle = self._angle_between(point1,point2)
        return distance,angle

    def _calulator_center_point(self,rect):
        return int(rect['x']+(rect['w']/2)), int(rect['y']-(rect['h']/2))
