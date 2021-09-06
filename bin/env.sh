export QT_QPA_PLATFOR=xcb
export AI_SDK_PROJECT_FULL_PATH=/home/xdien/workspace/GameAISDK/tools/SDKTool/project/LQ/
export AI_SDK_PROJECT_FILE_PATH=/home/xdien/workspace/GameAISDK/tools/SDKTool/project/LQ/cfg/task/gameReg/Task.json
export AI_SDK_PROJECT_FULL_PATH=/home/xdien/workspace/OpenAI_LQ1
export AI_SDK_PROJECT_FILE_PATH=/home/xdien/workspace/OpenAI_LQ1/cfg/task/gameReg/Task.json

mount --rbind /mnt/docker_btrfs/data_train/trained-networks /home/xdien/workspace/GameAISDK/tools/SDKTool/project/LQ/data/trained-networks
mount --rbind /mnt/docker_btrfs/data_train/result/ /home/xdien/workspace/GameAISDK/tools/SDKTool/project/LQ/result/
export AI_SDK_PROJECT_FULL_PATH=/home/xdien/workspace/GameAISDK/project/LQ3/
export AI_SDK_PROJECT_FILE_PATH=/home/xdien/workspace/GameAISDK/project/LQ3/cfg/task/gameReg/Task.json 


#run gameREG
~/workspace/GameAISDK/tools/SDKTool/project $ LD_LIBRARY_PATH='/home/xdien/workspace/GameAISDK/bin/:$LD_LIBRARY_PATH' ../../../bin/GameReg cfgpath  /home/xdien/workspace/GameAISDK/tools/SDKTool/project/LQ/LQ3.prj