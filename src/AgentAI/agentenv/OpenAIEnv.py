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
        
        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(self._inputImgHeight, self._inputImgWidth), dtype=np.uint8)
        
        

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
        for n in range(360):
            self._actions.append([di_chuyen_id,n,0,0])#chi duy chuyen khong nhan nut
        
        for rdichuyen1 in range(360):#di chuyen c1, ID 1 trong giao dien
            for lc1 in range(360):
                self._actions.append([di_chuyen_id,rdichuyen1,1,lc1])

        for rdichuyen2 in range(360):#di chuyen c2, ID 2 trong giao dien
            for lc2 in range(360):
                self._actions.append([di_chuyen_id,rdichuyen2,2,lc2])

        for rdichuyen3 in range(360):#di chuyen c2, ID 5 trong giao dien
            for lc3 in range(360):
                self._actions.append([di_chuyen_id,rdichuyen3,5,lc3])
        
        #cai dat cac nut binh thuong 
        self._actions.append([0,0,0,0])#khong di chuyen
        self._actions.append([0,0,3,0])#danh thuong
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
            self.__actionController.DoAction(right_action,angle=acts[3],frameSeq=self.__frameIndex,joystick_like_swipe=True)#once action

        

    def ResetAction(self):
        """
        Reset game action use ActionAPI
        """
        self.__actionController.Reset()

    def StopAction(self):
        """
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
        """
        is_done = False
        game_info = self._GetGameInfo()
        data = game_info['result'].get(self.__scoreTaskID)[0]['num']
        image = game_info['image']
        self.__frameIndex = game_info['frameSeq']
        state = self.__gameState

        img_height = image.shape[0]
        img_width = image.shape[1]

        self.logger.debug("the width %d and the height %d of real image", img_width, img_height)
        self.__actionController.SetSolution(img_width, img_height)

        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img = img[self.__beginRow:self.__endRow, self.__beginColumn:self.__endColumn]
        if img_width < img_height:
            img = cv2.transpose(img)
            img = cv2.flip(img, 1)

        img = cv2.resize(img, (self._inputImgWidth, self._inputImgHeight),interpolation=cv2.INTER_AREA)
        reward = self._CaculateReward(data)

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
        return img, reward, is_done


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
    
