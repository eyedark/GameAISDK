from time import time
import gym  
from actionmanager import ActionController
from util import util
import numpy as np
from AgentAPI import AgentAPIMgr

from .GameEnv import GameEnv
from gym import spaces
import os
import time
import cv2
ACTION_CFG_FILE = 'cfg/task/agent/OpenAIPPOAction.json'
LEARNING_CFG_FILE = 'cfg/task/agent/OpenAIPPOLearning.json'
TASK_CFG_FILE = 'cfg/task/gameReg/Task.json'
REG_GROUP_ID = 1
GAME_STATE_INVALID = 0
GAME_STATE_RUN = 1
GAME_STATE_WIN = 2
GAME_STATE_LOSE = 3


class OpenAIEnv(gym.Env,GameEnv):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(OpenAIEnv, self).__init__()
        self._LoadCfgFilePath()
        self._LoadEnvParams()
        self.__gameState = None
        self.__actionController = ActionController.ActionController()
        self.__actionController.Initialize(self.__actionCfgFile)
        # self.Reset()#gym auto call reset() func
        self.__agentAPI = AgentAPIMgr.AgentAPIMgr()

        self.logger.debug("Init action space %d", self.GetActionSpace())
        self.action_space = spaces.Discrete(self.GetActionSpace())
        
        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(720, 1280,3), dtype=np.uint8)

    def step(self, action):
        self.DoAction(action)
        img, reward, is_done = self.GetState()
        game_info = self._GetGameInfo()
        return img, reward, is_done, game_info
    #reset function
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
        Return number of game action
        """
        return self.__actionController.GetActionNum()

    def DoAction(self, action, *args, **kwargs):
        """
        Output game action use ActionAPI
        action: one hot vector
        """
        self.__actionController.DoAction(action, self.__frameIndex)

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
        game_info = self._GetGameInfo()
        data = game_info['result'].get(self.__scoreTaskID)[0]['num']
        image = game_info['image']
        self.__frameIndex = game_info['frameSeq']
        state = self.__gameState

        img_height = image.shape[0]
        img_width = image.shape[1]

        self.logger.debug("the width %d and the height %d of real image", img_width, img_height)
        self.__actionController.SetSolution(img_width, img_height)

        # img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # img = img[self.__beginRow:self.__endRow, self.__beginColumn:self.__endColumn]
        # if img_width < img_height:
        #     img = cv2.transpose(img)
        #     img = cv2.flip(img, 1)

        # img = cv2.resize(img, (176, 108))
        reward = self._CaculateReward(data)

        self.__isTerminal = True
        if state == GAME_STATE_LOSE:
            reward = self.__loseReward
        elif state == GAME_STATE_WIN:
            reward = self.__winReward
        elif state == GAME_STATE_RUN:
            self.__isTerminal = False
        else:
            self.logger.error('error game state: %d', state)

        if data == -1 and self.__isTerminal is not True:
            self.logger.debug('detect data -1, set 0 reward')
            reward = 0

        self.logger.debug('data: {0} reward: {1}'.format(data, reward))

        return image, reward, self.__isTerminal

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



