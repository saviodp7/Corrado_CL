function [P, P_dot, P_dotdot, vertici_traiettoria]=traj_calibration(start_pos, punto, side, f_s, tempo_traj)
%% Plan the trajectory along a path characterized by at least 11 points within the worktraj_xspace, in which there are at least one straight
%  portion and one circular portion and also the passage for at least 4 via points.
% 
c_altosin = punto + [side -side 0];
c_bassosin = punto + [side side 0];
c_altodestra = punto + [-side -side 0];
c_bassodestra = punto + [-side side 0];

t_tr=tempo_traj/16;
trasl_alto =[0,0,0.05];

path_descr = struct("inizio", [start_pos; punto+trasl_alto; punto; punto+trasl_alto; c_altosin+trasl_alto; c_altosin; c_altosin+trasl_alto; c_altodestra+trasl_alto; c_altodestra; c_altodestra+trasl_alto; c_bassodestra+trasl_alto; c_bassodestra; c_bassodestra+trasl_alto; c_bassosin+trasl_alto; c_bassosin; c_bassosin+trasl_alto;], ...
                "fine",[punto+trasl_alto; punto; punto+trasl_alto; c_altosin+trasl_alto; c_altosin; c_altosin+trasl_alto; c_altodestra+trasl_alto; c_altodestra; c_altodestra+trasl_alto; c_bassodestra+trasl_alto; c_bassodestra; c_bassodestra+trasl_alto; c_bassosin+trasl_alto; c_bassosin; c_bassosin+trasl_alto; start_pos;]);

[s_1,s_1_dot,s_1_dotdot] = trap_profile(0, t_tr, f_s, start_pos, punto+trasl_alto, tempo_traj, "rect");
[s_2,s_2_dot,s_2_dotdot] = trap_profile(t_tr, 2*t_tr, f_s, punto+trasl_alto, punto, tempo_traj, "rect");
[s_3,s_3_dot,s_3_dotdot] = trap_profile(2*t_tr, 3*t_tr, f_s, punto, punto+trasl_alto,tempo_traj, "rect");

[s_4,s_4_dot,s_4_dotdot] = trap_profile(3*t_tr, 4*t_tr,   f_s,punto+trasl_alto,c_altosin+trasl_alto, tempo_traj, "rect");
[s_5,s_5_dot,s_5_dotdot] = trap_profile(4*t_tr, 5*t_tr, f_s, c_altosin+trasl_alto,c_altosin, tempo_traj, "rect");
[s_6,s_6_dot,s_6_dotdot] = trap_profile(5*t_tr, 6*t_tr, f_s, c_altosin, c_altosin+trasl_alto,tempo_traj, "rect");
 
[s_7,s_7_dot,s_7_dotdot] = trap_profile(6*t_tr, 7*t_tr,  f_s,c_altosin+trasl_alto,c_altodestra+trasl_alto, tempo_traj, "rect");
[s_8,s_8_dot,s_8_dotdot] = trap_profile(7*t_tr, 8*t_tr, f_s, c_altodestra+trasl_alto,c_altodestra, tempo_traj, "rect");
[s_9,s_9_dot,s_9_dotdot] = trap_profile(8*t_tr, 9*t_tr, f_s, c_altodestra, c_altodestra+trasl_alto,tempo_traj, "rect");

[s_10,s_10_dot,s_10_dotdot] = trap_profile(9*t_tr, 10*t_tr,   f_s,c_altodestra+trasl_alto,c_bassodestra+trasl_alto, tempo_traj, "rect");
[s_11,s_11_dot,s_11_dotdot] = trap_profile(10*t_tr, 11*t_tr, f_s, c_bassodestra+trasl_alto,c_bassodestra, tempo_traj, "rect");
[s_12,s_12_dot,s_12_dotdot] = trap_profile(11*t_tr, 12*t_tr, f_s, c_bassodestra, c_bassodestra+trasl_alto,tempo_traj, "rect");

[s_13,s_13_dot,s_13_dotdot] = trap_profile(12*t_tr, 13*t_tr,   f_s,c_bassodestra+trasl_alto,c_bassosin+trasl_alto, tempo_traj, "rect");
[s_14,s_14_dot,s_14_dotdot] = trap_profile(13*t_tr, 14*t_tr, f_s, c_bassosin+trasl_alto,c_bassosin, tempo_traj, "rect");
[s_15,s_15_dot,s_15_dotdot] = trap_profile(14*t_tr, 15*t_tr, f_s, c_bassosin, c_bassosin+trasl_alto,tempo_traj, "rect");
[s_16,s_16_dot,s_16_dotdot] = trap_profile(15*t_tr, 16*t_tr, f_s, c_bassosin+trasl_alto, start_pos,tempo_traj, "rect");

S = [s_1; s_2; s_3; s_4; s_5; s_6; s_7; s_8; s_9; s_10; s_11; s_12; s_13; s_14; s_15; s_16];
S_dot = [s_1_dot; s_2_dot; s_3_dot; s_4_dot; s_5_dot; s_6_dot; s_7_dot; s_8_dot; s_9_dot; s_10_dot; s_11_dot; s_12_dot; s_13_dot; s_14_dot; s_15_dot; s_16_dot];
S_dotdot = [s_1_dotdot;s_2_dotdot;s_3_dotdot;s_4_dotdot; s_5_dotdot; s_6_dotdot; s_7_dotdot; s_8_dotdot; s_9_dotdot; s_10_dotdot; s_11_dotdot; s_12_dotdot; s_13_dotdot; s_14_dotdot; s_15_dotdot; s_16_dotdot];

P = start_pos;
P_dot = [0 0 0];
P_dotdot= [0 0 0];

for k = 1:size(path_descr.inizio, 1)
    [P, P_dot, P_dotdot] = lin_traj(P, P_dot, P_dotdot, S(k,:), S_dot(k,:), S_dotdot(k,:), path_descr.inizio(k,:), path_descr.fine(k,:));
end


verticeSuperioreSinistro = punto + [3/2*side -3/2*side 0];
verticeSuperioreDestro = punto + [3/2*side 3/2*side 0];
verticeInferioreSinistro = punto + [-3/2*side -3/2*side 0];
verticeInferioreDestro = punto + [-3/2*side 3/2*side 0];

vertici_traiettoria = [verticeSuperioreSinistro;
               verticeSuperioreDestro;
               verticeInferioreSinistro;
               verticeInferioreDestro];

end

