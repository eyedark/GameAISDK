/*
  * Tencent is pleased to support the open source community by making GameAISDK available.

  * This source code file is licensed under the GNU General Public License Version 3.
  * For full details, please refer to the file "LICENSE.txt" which is provided as part of this source code package.

  * Copyright (C) 2020 THL A29 Limited, a Tencent company.  All rights reserved.
*/

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "Comm/ImgReg/Recognizer/CLocationReg.h"
#include "Comm/Utils/Base64.h"
#include "Comm/Utils/IniConfig.h"
#include "Comm/Utils/TqcLog.h"
#include "UI/Src/Action/Action.h"
#include "UI/Src/Communicate/PBMsgManager.h"

extern char          *g_rootDataPath;
extern char *g_userCfgPath;
extern CPBMsgManager g_pbMsgMgr;
extern cv::Mat       g_uiFrame;

bool CAction::DoAction(const tagFrameContext &stFrameCtx, tagUIRegResult &stUIRegRst,
    UIStateArray &state, const enGameState eGameState) {
    tagUIState stUIState;
    int        nIndex = -1;

    // find index with nID
    for (int i = 0; i < state.size(); i++) {
        if (state[i].nId == stUIRegRst.nID) {
            stUIState = state.at(i);
            nIndex = i;
            break;
        }
    }

    // package with protobuf and send it
    bool bRst = DoAction(stFrameCtx, stUIState, eGameState);
    if (bRst) {
        LOGI("state %d, send frameSeq %d success", eGameState, stFrameCtx.nFrameSeq);
        if (-1 != nIndex) {
            // value of stUIState may be changed, such as scirpt execut number
            state[nIndex] = stUIState;
        }

        return true;
    } else {
        LOGE("state %d, send frameSeq %d failed", eGameState, stFrameCtx.nFrameSeq);
        return false;
    }

    return true;
}

CAction::CAction() {
    m_bShowResult = false;
    m_nDragCount = 0;
    m_eGameState = GAME_REG_STATE_NONE;
    m_eTestMode = SDK_TEST;
    m_preActionType = UI_ACTION_NONE;

    // initialize python, this should be called before using any other Python/C API functions
    Py_Initialize();
}

CAction::~CAction() {
    Py_Finalize();
}

bool CAction::Initialize(ETestMode eTestMode, const char* pszUserCfgPath) {
    m_eTestMode = eTestMode;
    m_oSendAction.SetTestMode(eTestMode);

    // read DEBUG|ResultShow configure
    CIniConfig oPlatformCfg;
    char szPath[256];
    sprintf(szPath, "%s/%s", pszUserCfgPath, UI_PLATFORM_CFG);
    int        nRst = oPlatformCfg.loadFile(szPath);
    if (nRst != 0) {
        LOGE("load file %s failed", szPath);
        return false;
    }

    m_bShowResult = oPlatformCfg.getPrivateBool("DEBUG", "ResultShow", 0);
    oPlatformCfg.closeFile();
    LOGI("result show flag is %d", m_bShowResult);
    m_oSendAction.SetShowResult(m_bShowResult);
    return true;
}


bool CAction::DoAction(const tagFrameContext &stFramectx, tagUIState &stSrcUIState,
    enGameState eGameState) {
    int nID = stSrcUIState.nId;

    // check parameters
    if (stFramectx.oFrame.empty()) {
        LOGE("process UID %d failed: input frame is empty, please check", nID);
        return false;
    }

    m_oSendAction.SetGameState(eGameState);
    m_eGameState = eGameState;
    /*UI_ACTION_CLICK|UI_ACTION_DRAG|UI_ACTION_TEXT|UI_ACTION_DRAG_AND_CHECK|UI_ACTION_SCRIPT*/
    tagActionState stDstActionState1;
    tagActionState stDstActionState2;

    bool bRst = false;
    bool bActionResult = true;
    bool bNeedNoNone = false;

    // save previous action type and UIState (drag check)
    switch (stSrcUIState.actionType) {
    case UI_ACTION_CLICK:
        bActionResult = DoClickAction(stFramectx, stSrcUIState, stDstActionState1);
        m_preActionType = UI_ACTION_CLICK;
        m_prestSrcUIState = stSrcUIState;
        LOGI("do click action");
        break;

    case UI_ACTION_DRAG:
        bActionResult = DoDragAction(stFramectx, stSrcUIState, stDstActionState1,
            stDstActionState2);
        m_preActionType = UI_ACTION_DRAG;
        m_prestSrcUIState = stSrcUIState;
        LOGI("do drag action");
        break;

    case UI_ACTION_DRAG_AND_CHECK:
        bActionResult = DoDragCheckAction(stFramectx, stSrcUIState, stDstActionState1);
        m_preActionType = UI_ACTION_DRAG_AND_CHECK;
        m_prestSrcUIState = stSrcUIState;
        LOGI("do drag and check action");
        break;

    case UI_ACTION_SCRIPT:
        bActionResult = DoScript(stFramectx, stSrcUIState);
        m_preActionType = UI_ACTION_SCRIPT;
        m_prestSrcUIState = stSrcUIState;
        LOGI("do script action");
        break;

    default:
        // if pre action is drag and check, current frame may be need drag and check action
        if (UI_ACTION_DRAG_AND_CHECK == m_preActionType) {
            bActionResult = DoDragCheckAction(stFramectx, m_prestSrcUIState, stDstActionState1);
            LOGI("do drag and check action");
        } else {
            m_preActionType = UI_ACTION_NONE;
            bNeedNoNone = true;
        }

        break;
    }

    bool bNoneActionResult = true;
    if (bNeedNoNone || !bActionResult) {
        bNoneActionResult = DoNoneAction(stFramectx);
        LOGI("do none action, result is %d", bNoneActionResult);
    }

    return bNoneActionResult && bActionResult;
}

bool CAction::DoClickAction(const tagFrameContext &stFramectx, const tagUIState &stSrcUIState,
    tagActionState &stDstActionState) {
    // stDstUAction = stSrcUIState;
    int            nID = stSrcUIState.nId;
    cv::Mat        oTmplImg = stSrcUIState.sampleImg;
    tagActionState oSrcPoint = stSrcUIState.stAction1;

    // detect source click point in current image(stFramectx.oFrame)
    stDstActionState = oSrcPoint;
    cv::Point outPoint;
    int       nRes = DetectPoint(nID, stFramectx.oFrame, oTmplImg, oSrcPoint, &outPoint);
    if (1 != nRes) {
        LOGE("UI %d find click point failed", nID);
        return false;
    }
    if (outPoint.x == 0 && outPoint.y == 0) {
        LOGE("UI %d find click point failed", nID);
        return false;
    }

    stDstActionState.nActionX = outPoint.x;
    stDstActionState.nActionY = outPoint.y;

    // package and send click action
    return m_oSendAction.SendClickAction(stFramectx, stSrcUIState, stDstActionState);
}

bool CAction::DoDragAction(const tagFrameContext &stFramectx, const tagUIState &stSrcUIState,
    tagActionState &stDstActionState1, tagActionState &stDstActionState2) {
    int            nID = stSrcUIState.nId;
    tagActionState oActionSt1 = stSrcUIState.stAction1;

    stDstActionState1 = oActionSt1;
    tagActionState oActionSt2 = stSrcUIState.stAction2;
    stDstActionState2 = oActionSt2;

    // detect source begin drag point in current image(stFramectx.oFrame)
    cv::Mat   frame = stFramectx.oFrame;
    cv::Point StartPt;
    cv::Point EndPt;
    int       nRst = DetectPoint(nID, frame, stSrcUIState.sampleImg, oActionSt1, &StartPt);
    if (1 != nRst) {
        LOGE("UI %d, find start drag point failed", nID);
        return false;
    }

    if (StartPt.x == 0 && StartPt.y == 0) {
        LOGE("UI %d, find start drag point failed", nID);
        return false;
    }
    stDstActionState1.nActionX = StartPt.x;
    stDstActionState1.nActionY = StartPt.y;

    // detect source end drag point in current image(stFramectx.oFrame)
    nRst = DetectPoint(nID, frame, stSrcUIState.sampleImg, oActionSt2, &EndPt);
    if (1 != nRst) {
        LOGE("UI %d, find end drag point failed", nID);
        return false;
    }

    if (EndPt.x == 0 && EndPt.y == 0) {
        LOGE("UI %d, find end drag point failed", nID);
        return false;
    }

    stDstActionState2.nActionX = EndPt.x;
    stDstActionState2.nActionY = EndPt.y;

    // package and send click action
    return m_oSendAction.SendDragAction(stFramectx, stSrcUIState, stDstActionState1,
        stDstActionState2);
}

bool CAction::DoDragCheckAction(const tagFrameContext &stFramectx, const tagUIState &stSrcUIState,
    tagActionState &stDstActionState) {
    cv::Mat  oFrame = stFramectx.oFrame;
    cv::Rect rcROI = cv::Rect(0, 0, oFrame.cols, oFrame.rows);
    double   dVal = 0;
    double   dMinVal = 0;
    bool     bFound = false;
    int      nStartX = -1;  // Drag start x of position
    int      nStartY = -1;  // Drag start y of position
    int      nEndX = -1;   // Drag end y of position
    int      nEndY = -1;   // Drag end y of position
    int      nIndex = -1;

    // Compare current frame with the target image.
    // If matched, we will stop drag and change game state to
    // the last state.
    cv::Mat  oTmplFrame = stSrcUIState.stDragCheckState.targetImg[0];
    cv::Rect oTmplRect = cv::Rect(stSrcUIState.stDragCheckState.stTargetRect.nPointX,
        stSrcUIState.stDragCheckState.stTargetRect.nPointY,
        stSrcUIState.stDragCheckState.stTargetRect.nWidth,
        stSrcUIState.stDragCheckState.stTargetRect.nHeight);

    float    fThreshold = stSrcUIState.stDragCheckState.fDragThreshold;
    cv::Rect oRect;
    float    fScore;
    // detect rect with multi-process
    int nRst = DetectRect(stSrcUIState.nId, oFrame, oTmplFrame, oTmplRect, fThreshold,
        &oRect, &fScore);

    if (oRect.width != 0 && oRect.height != 0) {
        LOGI("find target, and finish drag and check");
        m_preActionType = UI_ACTION_NONE;
        return DoNoneAction(stFramectx);
    }

    // up to max drag count, and not matched, stop.
    if (m_nDragCount > stSrcUIState.stDragCheckState.dragCount) {
        m_nDragCount = 0;   // clear count of drag actions.
        LOGW("Exceeds the max count of drag actions");
        m_preActionType = UI_ACTION_NONE;
        // package and send none action
        return DoNoneAction(stFramectx);;
    }

    // Based on drag direction to send action.
    // 0 for none, 1 for down, 2 for up, 3 for left, 4 for right
    if (stSrcUIState.stDragCheckState.dragAction == 1) {
        // down
        nStartX = stSrcUIState.stDragCheckState.stDragPt.nPointX;
        nStartY = stSrcUIState.stDragCheckState.stDragPt.nPointY;
        nEndX = stSrcUIState.stDragCheckState.stDragPt.nPointX;
        nEndY = stSrcUIState.stDragCheckState.stDragPt.nPointY
            - stSrcUIState.stDragCheckState.dragLen;
    } else if (stSrcUIState.stDragCheckState.dragAction == 2) {
        // up
        nStartX = stSrcUIState.stDragCheckState.stDragPt.nPointX;
        nStartY = stSrcUIState.stDragCheckState.stDragPt.nPointY;
        nEndX = stSrcUIState.stDragCheckState.stDragPt.nPointX;
        nEndY = stSrcUIState.stDragCheckState.stDragPt.nPointY
            + stSrcUIState.stDragCheckState.dragLen;
    } else if (stSrcUIState.stDragCheckState.dragAction == 3) {
        // left
        nStartX = stSrcUIState.stDragCheckState.stDragPt.nPointX;
        nStartY = stSrcUIState.stDragCheckState.stDragPt.nPointY;
        nEndX = stSrcUIState.stDragCheckState.stDragPt.nPointX
            - stSrcUIState.stDragCheckState.dragLen;
        nEndY = stSrcUIState.stDragCheckState.stDragPt.nPointY;
    } else if (stSrcUIState.stDragCheckState.dragAction == 4) {
        // right
        nStartX = stSrcUIState.stDragCheckState.stDragPt.nPointX;
        nStartY = stSrcUIState.stDragCheckState.stDragPt.nPointY;
        nEndX = stSrcUIState.stDragCheckState.stDragPt.nPointX
            + stSrcUIState.stDragCheckState.dragLen;
        nEndY = stSrcUIState.stDragCheckState.stDragPt.nPointY;
    }

    tagActionState stDstActionState1;
    stDstActionState1.nActionX = nStartX;
    stDstActionState1.nActionY = nStartY;
    tagActionState stDstActionState2;
    stDstActionState2.nActionX = nEndX;
    stDstActionState2.nActionY = nEndY;

    m_nDragCount++;
    LOGI("drag check current count %d, max count %d", m_nDragCount,
        stSrcUIState.stDragCheckState.dragCount);
    m_preActionType = UI_ACTION_DRAG_AND_CHECK;

    // package and send click action
    return m_oSendAction.SendDragAction(stFramectx, stSrcUIState, stDstActionState1,
        stDstActionState2);
}

bool CAction::DoScript(const tagFrameContext &stFramectx, tagUIState &stSrcUIState) {
    try {
        cv::Mat  oFrame = stFramectx.oFrame;
        PyObject *pModule = nullptr;
        PyObject *pFunc = nullptr;

        const unsigned int unMaxScriptLength = 1024;
        char szScriptPath[TQC_PATH_STR_LEN] = { 0 };
        SNPRINTF(szScriptPath, TQC_PATH_STR_LEN, "%s/%s", g_userCfgPath,
            stSrcUIState.strScriptPath);
        LOGI("scriptPath %s", szScriptPath);

        std::string strPath(szScriptPath);
        std::replace(strPath.begin(), strPath.end(), '\\', '/');
        // find fold name and path
        std::string::size_type idx = strPath.rfind('/', strPath.length());
        std::string            folder = strPath.substr(0, idx);

        // run "import sys" in python
        PyObject* pyMainModule = PyImport_AddModule("__main__");
        PyRun_SimpleString("import sys");

        char szInsertUserScriptPathScript[unMaxScriptLength] = { 0 };
        SNPRINTF(szInsertUserScriptPathScript, unMaxScriptLength,
            "'%s' not in sys.path and sys.path.insert(0, '%s')", folder.c_str(), folder.c_str());

        // run "sys.path.insert(0, {path to script})" in python
        LOGI("add path: %s", szInsertUserScriptPathScript);
        PyRun_SimpleString(szInsertUserScriptPathScript);

        // get current module, such as ".../bin/UIRecognize.exe (for windows)"
        char szModulePath[TQC_PATH_STR_LEN] = { 0 };
        bool flag = TqcOsGetCWD(szModulePath, sizeof(szModulePath));
        if (!flag) {
            LOGE("get cwd path failed");
            return false;
        }
        std::string module_folder(szModulePath);
        std::replace(module_folder.begin(), module_folder.end(), '\\', '/');

        // run "sys.path.insert(0, {path to UIAPI folder})"
        char szUIAPIPath[TQC_PATH_STR_LEN] = { 0 };
        SNPRINTF(szUIAPIPath, TQC_PATH_STR_LEN, "%s/API/UIAPI", module_folder.c_str());

        char szInsertUIAPIPathScript[unMaxScriptLength] = { 0 };
        SNPRINTF(szInsertUIAPIPathScript, unMaxScriptLength,
            "'%s' not in sys.path and sys.path.insert(0, '%s')", szUIAPIPath, szUIAPIPath);
        LOGI("add path: %s", szInsertUIAPIPathScript);
        PyRun_SimpleString(szInsertUIAPIPathScript);

        // see sys.path
        PyRun_SimpleString("import json");
        PyRun_SimpleString("sys_path = json.dumps(sys.path)");
        PyObject* pyVarSysPath = PyObject_GetAttrString(pyMainModule, "sys_path");
        if (PyUnicode_Check(pyVarSysPath)) {
            PyObject *pTempBytes2 = PyUnicode_AsEncodedString(pyVarSysPath, "UTF-8", "strict");
            if (pTempBytes2 != nullptr) {
                char szVarSysPath[unMaxScriptLength] = { 0 };
                SNPRINTF(szVarSysPath, unMaxScriptLength, "%s", PyBytes_AS_STRING(pTempBytes2));
                std::string strVarSysPath(szVarSysPath);
                if (strVarSysPath.length() > 255) {
                    int j = 255;
                    int i = 0;
                    while (j < strVarSysPath.length()) {
                        std::string strLog = strVarSysPath.substr(i, j);
                        LOGI("sys path: %s", strLog.c_str());
                        i = j;
                        j = j + 255;
                    }
                    if (i < strVarSysPath.length()) {
                        std::string strLogEnd = strVarSysPath.substr(i, strVarSysPath.length());
                        LOGI("sys path: %s", strLogEnd.c_str());
                    }
                } else {
                    LOGI("sys path: %s", szVarSysPath);
                }
            }
        }

        // get module name
        std::string::size_type modelidx = strPath.rfind('.', strPath.length());
        std::string            strModel = strPath.substr(idx + 1, modelidx - 1 - idx);
        LOGI("import module: %s", strModel.c_str());
        pModule = PyImport_ImportModule(strModel.c_str());
        if (NULL == pModule) {
            LOGE("import model %s failed", strModel.c_str());
            return false;
        }

        // load mode
        pFunc = PyObject_GetAttrString(pModule, "Run");
        if (NULL == pFunc) {
            LOGE("Get Function Run failed");
            return false;
        }

        Json::Value jsonScriptParams = stSrcUIState.jsonScriptParams;
        jsonScriptParams["frameSeq"] = Json::Value(stFramectx.nFrameSeq);

        char szPath[TQC_PATH_STR_LEN] = { 0 };
        SNPRINTF(szPath, TQC_PATH_STR_LEN, "%s", stSrcUIState.strSampleFile);

        jsonScriptParams["samplePath"] = Json::Value(szPath);
        jsonScriptParams["stateID"] = stSrcUIState.nId;
        jsonScriptParams["extNum"] = stSrcUIState.nScrpitExtNum;

        int  nSize = oFrame.total() * oFrame.elemSize();
        char *szBuff = new char[nSize + 1];
        memset(szBuff, 0, nSize + 1);
        memcpy(szBuff, oFrame.data, nSize);
        jsonScriptParams["image"] = base64_encode(szBuff, nSize);
        jsonScriptParams["width"] = oFrame.cols;
        jsonScriptParams["height"] = oFrame.rows;
        delete[]szBuff;
        szBuff = nullptr;

        Json::FastWriter writer;
        std::string      strScriptParams = writer.write(jsonScriptParams);

        PyObject *pArgs = PyTuple_New(1);
        PyTuple_SetItem(pArgs, 0, Py_BuildValue("s", strScriptParams.c_str()));

        PyObject *pResult = nullptr;
        char     *pszResult = nullptr;

        // call python function and get result
        pResult = PyEval_CallObject(pFunc, pArgs);
        if (NULL == pResult) {
            LOGE("Py CallObject Failed");
            return false;
        }

        if (PyUnicode_Check(pResult)) {
            PyObject *pTempBytes = PyUnicode_AsEncodedString(pResult, "UTF-8", "strict");
            if (pTempBytes != nullptr) {
                pszResult = PyBytes_AS_STRING(pTempBytes);
                pszResult = strdup(pszResult);
                Py_DECREF(pTempBytes);
                Json::Reader reader;
                Json::Value  root;
                if (reader.parse(pszResult, root)) {
                    stSrcUIState.nScrpitExtNum = root["extNum"].asInt();
                    LOGI("script ext num is %d", stSrcUIState.nScrpitExtNum);
                }

                free(pszResult);
                pszResult = nullptr;
            } else {
                LOGE("run script failed %s", stSrcUIState.strScriptPath);
            }
        }
    }
    catch (const std::exception &e) {
        LOGE("************error: %s, continue process********************* \n\n", e.what());
    }
    return true;
}

bool CAction::DoNoneAction(const tagFrameContext &stFramectx) {
    tagMessage    uiMsg;
    tagUIAction   *pUIState = uiMsg.mutable_stuiaction();
    GAMESTATEENUM uiState = PB_STATE_NONE;

    pUIState->set_nuiid(-1);
    // Check and set game state.
    pUIState->set_egamestate(PB_STATE_NONE);
    tagUIUnitAction *pUIUnitAction = pUIState->add_stuiunitaction();
    pUIUnitAction->set_euiaction(PB_UI_ACTION_NONE);

    int nImgSize = stFramectx.oFrame.total() * stFramectx.oFrame.elemSize();
    tagSrcImageInfo *pImg = pUIState->mutable_stsrcimageinfo();

    pImg->set_uframeseq(stFramectx.nFrameSeq);
    pImg->set_nwidth(stFramectx.oFrame.cols);
    pImg->set_nheight(stFramectx.oFrame.rows);
    // package and send click action
    LOGI("frameSeq %d, cols %d, rows %d", stFramectx.nFrameSeq, stFramectx.oFrame.cols,
        stFramectx.oFrame.rows);
    // 封装图像信息(帧序号，图像长，宽)，如果是SDKTool运行模式，需要封装源图像数据
    if (m_eTestMode == SDKTOOL_TEST) {
        pImg->set_byimagedata(stFramectx.oFrame.data, nImgSize);
    }

    uiMsg.set_emsgid(MSG_UI_ACTION);
    m_oSendAction.SendActionMsg(stFramectx, cv::Point(-1, -1), cv::Point(-1, -1),
        -1, uiState, uiMsg);
    return true;
}

ETestMode CAction::GetTestMode() {
    return m_eTestMode;
}

bool CAction::IsShowResult() {
    return m_bShowResult;
}

CSendAction* CAction::SendAction() {
    return &m_oSendAction;
}

enGameState CAction::GetGameState() {
    return m_eGameState;
}

// process image size is 1280 * ?, or ? * 1280source image may not equal to it.
bool RestoreAction(const cv::Mat &oFrame, const eUIActionType actionType, const int nStateId,
    cv::Point &actionPoint1, cv::Point &actionPoint2) {
    CAction *poAction = CAction::getInstance();

    switch (actionType) {
    case UI_ACTION_CLICK:
        // Cannot find click point.
        if (actionPoint1.x == -1 || actionPoint1.y == -1) {
            LOGW("Cannot find Script UI click: id: %d, x=%d y=%d", nStateId, actionPoint1.x,
                actionPoint1.y);
            return false;
        } else {
            // Resize action point based on input frame size.
            poAction->SendAction()->RestoreActionPoint(actionPoint1,
                cv::Size(oFrame.cols, oFrame.rows), cv::Size(g_uiFrame.cols, g_uiFrame.rows),
                actionPoint1);
        }

        break;

    case UI_ACTION_DRAG:
        // Cannot find drag point.
        if (actionPoint1.x == -1 || actionPoint1.y == -1 || actionPoint2.x == -1
            || actionPoint2.y == -1) {
            LOGW("Cannot find Script UI drag: id: %d, (%d, %d)->(%d, %d)",
                nStateId, actionPoint1.x, actionPoint1.y, actionPoint2.x, actionPoint2.y);
            return false;
        } else {
            // Resize action point based on input frame size.
            poAction->SendAction()->RestoreActionPoint(actionPoint1,
                cv::Size(oFrame.cols, oFrame.rows), cv::Size(g_uiFrame.cols, g_uiFrame.rows),
                actionPoint1);
            poAction->SendAction()->RestoreActionPoint(actionPoint2,
                cv::Size(oFrame.cols, oFrame.rows), cv::Size(g_uiFrame.cols, g_uiFrame.rows),
                actionPoint2);
        }

        break;

    default:
        break;
    }

    return true;
}

// detect point1 of stState1(nActionX, nActionY) in frame
bool DetectActionPoint(const int nActionID, const cv::Mat &frame, const cv::Mat &sampleImage,
    const tagActionState &stState1, cv::Point &actionPoint1) {
    // check input parameters
    if (stState1.nActionX >= 0 && stState1.nActionY >= 0) {
        // detect point with multi-process
        int nRst = DetectPoint(nActionID, frame, sampleImage, stState1, &actionPoint1);
        if (1 != nRst) {
            LOGE("UI %d, find  point failed", nActionID);
            return false;
        }
        if (actionPoint1.x == 0 && actionPoint1.y == 0) {
            LOGE("UI %d, find  point failed", nActionID);
            return false;
        }
    }

    return true;
}

// send Script UI Action, which was called by python script
bool SendScriptUIAction(char *pszPkgBuff) {
    // check parameters
    if (NULL == pszPkgBuff) {
        LOGE("recv pkg buff is NULL");
        return false;
    }

    // recv key-vale buff, and format it with json
    LOGD("script pkg buff is %s", pszPkgBuff);
    tagMessage   uiMsg;
    tagUIAction  *pUIState = uiMsg.mutable_stuiaction();
    std::string  strState;
    Json::Reader reader;
    Json::Value  root;
    // parse pkg buff with Json
    bool bResult = reader.parse(pszPkgBuff, root);
    if (!bResult) {
        LOGE("parser %s failed", pszPkgBuff);
        return false;
    }

    int         nFrameSeq = root["frameSeq"].asInt();
    int         nStateId = root["stateID"].asInt();
    std::string name = root["samplePath"].asString();
    cv::Mat     sampleImage = cv::imread(name);
    cv::Mat     frame;
    float       fResizeSrcRatio;
    ConvertImgTo720P(nStateId, g_uiFrame, frame, fResizeSrcRatio);

    LOGD("nStateId is %d", nStateId);
    CAction       *poAction = CAction::getInstance();
    enGameState   eState = poAction->GetGameState();
    GAMESTATEENUM uiState = poAction->SendAction()->MapState(eState, nStateId);
    pUIState->set_egamestate(uiState);

    // copy g_uiFrame to oDisplay, paint result to oDisplay
    cv::Mat oDisplay;
    g_uiFrame.copyTo(oDisplay);

    Json::Value scriptActions = root["scriptActions"];
    int         nSize = scriptActions.size();

    // parser every action and package it
    for (int i = 0; i < nSize; i++) {
        Json::Value action = scriptActions[i];
        int         nActionID = action["actionID"].asInt();

        int nDuringTimeMs = action["duringTimeMs"].asInt();
        int nSleepTimeMs = action["sleepTimeMs"].asInt();

        eUIActionType actionType;
        actionType = eUIActionType(action["actionType"].asInt());

        tagActionState stState1;
        tagActionState stState2;
        poAction->SendAction()->ReadActionJsonValue(action, stState1, stState2);

        // detect action point1(click|drag begin point), point2(drag end point)
        cv::Point actionPoint1;
        cv::Point actionPoint2;
        int       nRst = -1;
        // detect action point with multi-process
        bool bRst = DetectActionPoint(nActionID, frame, sampleImage, stState1, actionPoint1);
        if (!bRst) {
            continue;
        }
        // detect action point with multi-process
        bRst = DetectActionPoint(nActionID, frame, sampleImage, stState2, actionPoint2);
        if (!bRst) {
            continue;
        }
        // draw every action in result image
        if (poAction->IsShowResult()) {
            // actions may be more than one, so, paint them first, show them at final.
            poAction->SendAction()->PaintAction(oDisplay, actionPoint1, actionPoint2, nActionID,
                PB_STATE_UI);
        }
        // restore action point base on  size of process image and source image
        bRst = RestoreAction(frame, actionType, nStateId, actionPoint1, actionPoint2);
        if (!bRst) {
            continue;
        }

        switch (actionType) {
        case UI_ACTION_CLICK:
        {
            // Action click
            tagUIUnitAction *pUIUnitAction = pUIState->add_stuiunitaction();
            pUIUnitAction->set_euiaction(PB_UI_ACTION_CLICK);
            pUIUnitAction->set_nduringtimems(nDuringTimeMs);
            pUIUnitAction->set_nsleeptimems(nSleepTimeMs);
            tagUIPoint *pPoint = pUIUnitAction->mutable_stclickpoint();
            pPoint->set_nx(actionPoint1.x);
            pPoint->set_ny(actionPoint1.y);

            LOGI("UI: id: %d, x=%d y=%d, actionType=%d, during=%d", nStateId, actionPoint1.x,
                actionPoint1.y, actionType, nDuringTimeMs);
            break;
        }

        case UI_ACTION_DRAG:
        {
            // Action drag.
            tagUIUnitAction *pUIUnitAction = pUIState->add_stuiunitaction();
            pUIUnitAction->set_euiaction(PB_UI_ACTION_DRAG);
            pUIUnitAction->set_nduringtimems(nDuringTimeMs);
            pUIUnitAction->set_nsleeptimems(nSleepTimeMs);
            tagUIPoint *pPoint = pUIUnitAction->add_stdragpoints();
            pPoint->set_nx(actionPoint1.x);
            pPoint->set_ny(actionPoint1.y);

            pPoint = pUIUnitAction->add_stdragpoints();
            pPoint->set_nx(actionPoint2.x);
            pPoint->set_ny(actionPoint2.y);

            LOGI("UI: id: %d, (%d, %d)->(%d, %d), during=%d", nStateId, actionPoint1.x,
                actionPoint1.y, actionPoint2.x, actionPoint2.y, nDuringTimeMs);
            break;
        }

        default:
        {
            tagUIUnitAction *pUIUnitAction = pUIState->add_stuiunitaction();
            pUIUnitAction->set_euiaction(PB_UI_ACTION_NONE);
            break;
        }
        }
    }

    if (poAction->IsShowResult()) {
        // show UI result image and save it to folder("../result")
        cv::imshow("UI", oDisplay);
        cv::waitKey(1);
        char szRstImgName[TQC_PATH_STR_LEN] = { 0 };
        SNPRINTF(szRstImgName, TQC_PATH_STR_LEN, "../result/Script_Seq%d_ID%d.jpg",
            nFrameSeq, nStateId);
        cv::imwrite(szRstImgName, oDisplay);
    }

    // Return src image info
    int             nImgSize = g_uiFrame.total() * g_uiFrame.elemSize();
    tagSrcImageInfo *pImg = pUIState->mutable_stsrcimageinfo();

    pImg->set_uframeseq(nFrameSeq);
    pImg->set_nwidth(g_uiFrame.cols);
    pImg->set_nheight(g_uiFrame.rows);

    if (SDKTOOL_TEST == poAction->GetTestMode()) {
        pImg->set_byimagedata(g_uiFrame.data, nImgSize);
    }

    uiMsg.set_emsgid(MSG_UI_ACTION);
    uiMsg.SerializeToString(&strState);

    // Before send UI action, we should sleep 0.5s to wait UI animation.
    // TqcOsSleep(500);
    // Send game state msg to ManageCenter
    // If we need to debug with sdk tool, we should send msg to it.
    enPeerName peerAddr = PEER_MC;
    if (SDKTOOL_TEST == poAction->GetTestMode())
        peerAddr = PEER_SDK_TOOLS;

    if (SDKTOOL_TEST == poAction->GetTestMode() || SDK_TEST == poAction->GetTestMode()) {
        // SDKTool or SDK communicate with tbus
        bool bRst = g_pbMsgMgr.SendData(reinterpret_cast<void*>(
            const_cast<char*>(strState.c_str())), strState.length(), peerAddr);
        if (!bRst) {
            LOGE("Send game state failed.");
        }
    }

    LOGI("send script frame data, frameIndex=%d", nFrameSeq);
    return true;
}

// 用于脚本中DEBUG级别日志
bool PyLOGD(char *pszLogContent) {
    // 参数合法性检查
    if (NULL == pszLogContent) {
        LOGE("input params is NULL, please check");
        return false;
    }

    LOGD("scriptlog %s", pszLogContent);
    return true;
}

// 用于脚本中INFO级别日志
bool PyLOGI(char *pszLogContent) {
    // 参数合法性检查
    if (NULL == pszLogContent) {
        LOGE("input params is NULL, please check");
        return false;
    }

    LOGI("scriptlog %s", pszLogContent);
    return true;
}

// 用于脚本中WARN级别日志
bool  PyLOGW(char *pszLogContent) {
    // 参数合法性检查
    if (NULL == pszLogContent) {
        LOGE("input params is NULL, please check");
        return false;
    }

    LOGW("scriptlog %s", pszLogContent);
    return true;
}

// 用于脚本中ERROR级别日志
bool  PyLOGE(char *pszLogContent) {
    // 参数合法性检查
    if (NULL == pszLogContent) {
        LOGE("input params is NULL, please check");
        return false;
    }

    LOGE("scriptlog %s", pszLogContent);
    return true;
}
