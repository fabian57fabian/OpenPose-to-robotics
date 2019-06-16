import cv2
import sys
from sys import *
import os
import time
import shutil
from pathlib import Path

#importo openpose, codice preso dal tutorial
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e


#settaggio parametri op
params = dict()
params["model_folder"] = "../../../models/"
params["number_people_max"] = 1
params["body"] = 1
params["alpha_pose"] = 1

#salvo i risultati della posizione dello scheletro in formato json, abilitndo questa flag
#params["write_json"] = "IVA_pose_estimation_results"

#hand detection. NB: la frame rate si abbassa dimezzandosi
#params["hand"] = True
#params["hand_scale_number"] = 6
#params["hand_scale_range"] = 0.4

#stampa dei parametri
#print(params)
try:
    #verifico se esiste la cartella degli output in Json del detecting; se esiste,
    # la sovrascrivo nel corso del nuovo detecting (solo se salvo output Json)
    path = Path('C:/Users/loren/OneDrive/Documenti/GitHub/openpose/build/examples/tutorial_api_python/IVA_pose_estimation_results')
    if(path.exists()):
        #elimino il contenuto della cartella dei risultati json ogni volta che provo a fare il detecting
        shutil.rmtree('C:/Users/loren/OneDrive/Documenti/GitHub/openpose/build/examples/tutorial_api_python/IVA_pose_estimation_results')

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    #alloco arrays dove memorizzo i keypoints che mi servono per i gesti, per cui ho previsto solo i polsi
    RightWirst_x = []
    RightWirst_y = []
    LeftWirst_x = []
    LeftWirst_y = []

    #avvio la webcam con opencv con il metodo VideoCapture. Il paametro 0 indica che verrà aperta la webcam installata
    #nel laptop; con il flag WINDOWS_NORMAL posso fare resize 'dinamico' della finestra durante l'esecuzione del programma
    cv2.namedWindow('DETECTED KEYPOINTS', cv2.WINDOW_NORMAL)
    #con resizeWindow indico la dimensione di partenza della finestra dell'output della webcam. RISOLUZIONE SCELTA-> 4:3
    cv2.resizeWindow('DETECTED KEYPOINTS', 800, 600)
    stream = cv2.VideoCapture(0)

    #Counter dei frame; mi serve per indicizzare i frame prodotti durante la computazione e calcolare frame rate
    counter = 0
    #Conteggio del tempo di esecuzione dello script
    start = time.time()

    while True:
        # leggo i frame ottenuti dalla webcam e salvo frame per frame (frame.png viene processato con openpose)
        ret, img = stream.read()
        #flip output dell'immagine catturata dalla webcam
        cv2.flip(img, 1, img)
        #disegno linea al di sotto della quale la macchina è in stop
        cv2.line(img, (0, 380), (640, 380), (0, 0, 255), thickness=3)
        #cattura del frame i-esimo
        cv2.imwrite("frame.png", img)

        #processo i frame, utilizzando la classe datum, che serve per leggere e scrivere con gli oggetti openpose
        #e openCV
        datum = op.Datum()
        imageToProcess = cv2.imread("frame.png")
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop([datum])

        #print dei vari keypoints
        #print("Body keypoints: \n" + str(datum.poseKeypoints))

        #Controllo se trovo correttamente una persona con la webcam
        if(str(datum.poseKeypoints) == str(2.0) or str(datum.poseKeypoints) == str(0.0)
                or str(datum.poseKeypoints) == str(1e-45) ):
            print('NO DETECTED PEOPLE, YOU SHOULD GO IN FRONT OF YOUR WEBCAM')
            time.sleep(2)

            RightWirst_x.append(0.0)
            RightWirst_y.append(0.0)

            LeftWirst_x.append(0.0)
            LeftWirst_y.append(0.0)

        else:
            RightWirst_x.append(datum.poseKeypoints[0][7][0])
            RightWirst_y.append(datum.poseKeypoints[0][7][1])
            LeftWirst_x.append(datum.poseKeypoints[0][4][0])
            LeftWirst_y.append(datum.poseKeypoints[0][4][1])

        #TODO: retromarcia, geasto con 'hand' per fermare l'applicazione(?)
        #gestione dei vari gesti: stop, accelerazione, svolta a dx e sx
        if( (LeftWirst_y[counter] > 380.0 and RightWirst_y[counter] > 380.0) or (LeftWirst_y[counter] == 0.0
            and RightWirst_y[counter] == 0.0) or (LeftWirst_y[counter] == 0.0 and RightWirst_y[counter] > 380.0)
                                                or (LeftWirst_y[counter] > 380.0 and RightWirst_y[counter] == 0.0)):
            print('STOP')
        else:
            if (RightWirst_y[counter] < 380.0 and LeftWirst_y[counter] < 380.0
                    and (abs(RightWirst_y[counter] - LeftWirst_y[counter]) <= 20)):
                print('ACCELERA di una quantità pari a: ', RightWirst_y[counter])
            else:
                if ((RightWirst_y[counter] < 380.0 and LeftWirst_y[counter] < 380.0)
                    and (abs(RightWirst_y[counter] - LeftWirst_y[counter]) > 20)
                        and RightWirst_y[counter] > LeftWirst_y[counter]):
                    print('SVOLTA A SINISTRA di una quantità pari a: ', RightWirst_y[counter])
                else:
                    if ((RightWirst_y[counter] < 380.0 and LeftWirst_y[counter] < 380.0)
                            and (abs(RightWirst_y[counter] - LeftWirst_y[counter]) > 20)
                            and RightWirst_y[counter] < LeftWirst_y[counter]):
                        print('SVOLTA A DESTRA di una quantità pari a: ', LeftWirst_y[counter])


        #mostro graficamente sull'output della webcam lo skeleton di openpose
        cv2.imshow('DETECTED KEYPOINTS', datum.cvOutputData)
        counter = counter + 1

        # con il tasto q, Q == quit, interrompo il programma; NB: waitKey deve essere SEMPRE a 1
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            break

    end = time.time()
    #rilascio le risorse di cv2
    stream.release()
    cv2.destroyAllWindows()
    total_time = end - start

    #tempo e fps
    print('--------------------')
    print('Tempo totale di esecuzionde dello script : ', total_time)
    print('FPS: ', counter / total_time)

#errore nell'allocazione di oggetto openpose
except Exception as e:
    # print(e)
    sys.exit(-1)

