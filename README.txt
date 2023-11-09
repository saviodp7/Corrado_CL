Per l'utilizzo di alcuni file è necessario il RigidBodyTree di Corrado, importatelo da rbt_corrado.mat oppure per aggiornarlo runnare
$ importrobot("Corrado_simscape_<dispositivo>.xls")
dopo aver effettuato una simulazione

Corrado_simscape_*
Schema simulink contentente la struttura di Corrado per la simulazione, copiare il file per lavorare sul proprio dispositivo dato che i percorsi assoluti dei modelli CAD cambiano per ogni dispositivo

IK_corrado
Schema simulink per la risoluzione della cinematica inversa, prende in ingresso la traiettoria x_d e restituisce in uscita la traiettoria nello spazio dei giunti
