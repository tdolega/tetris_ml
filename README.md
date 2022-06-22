# tetris_ml

requires a game to run: https://github.com/marcinsobecki2408/SFML_TETRIS

You need to download both repositories. Compile the game using cmake. In globalSetting.py, correctly set the path TETRIS_GAME_RUN_PATH to the game's root folder and TETRIS_GAME_EXE_PATH to the compiled game executable. Train using python ./mainTrain.py and run the presentation mode via python ./mainPlay.py after first setting the name of the trained model in the MODEL_FILENAME variable.
