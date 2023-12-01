function [P, P_dot, P_dotdot]=traj_x(start_pos, centro_x, r, f_s, tempo_traj)
%% Plan the trajectory along a path characterized by at least 11 points within the workspace, in which there are at least one straight
%  portion and one circular portion and also the passage for at least 4 via points.

altosin_x = centro_x + [r -r 0];
bassosin_x = centro_x + [r r 0];
altodestra_x = centro_x + [-r -r 0];
bassodestra_x = centro_x + [-r r 0];
%viapoint_bdx_adx=(bassodestra_x +altodestra_x)/2 +[0,0,0.07];

t_tr = tempo_traj/12;
trasl_alto = [0,0,0.05];

 path_descr = struct("inizio", [start_pos; altosin_x+trasl_alto; altosin_x; bassodestra_x; bassodestra_x+trasl_alto; altodestra_x+trasl_alto;altodestra_x; bassosin_x; bassosin_x+trasl_alto;], ...
                "fine", [altosin_x+trasl_alto; altosin_x; bassodestra_x; bassodestra_x+trasl_alto; altodestra_x+trasl_alto; altodestra_x; bassosin_x; bassosin_x+trasl_alto; start_pos;]);

[s_1,s_1_dot,s_1_dotdot] = trap_profile(0, t_tr,   f_s, start_pos, altosin_x+trasl_alto, tempo_traj, "rect");
[s_2,s_2_dot,s_2_dotdot] = trap_profile(t_tr, 2*t_tr, f_s, altosin_x+trasl_alto, altosin_x, tempo_traj, "rect");
[s_3,s_3_dot,s_3_dotdot] = trap_profile(2*t_tr, 4*t_tr, f_s, altosin_x, bassodestra_x,tempo_traj, "via_point_inizio");
[s_4,s_4_dot,s_4_dotdot] = trap_profile(4*t_tr, 5*t_tr, f_s, bassodestra_x,  bassodestra_x+trasl_alto,tempo_traj, "via_point_fine");
[s_5,s_5_dot,s_5_dotdot] = trap_profile(5*t_tr ,6*t_tr, f_s,bassodestra_x+trasl_alto, altodestra_x+trasl_alto,tempo_traj, "rect");
[s_6,s_6_dot,s_6_dotdot] = trap_profile(7*t_tr, 8*t_tr, f_s, altodestra_x+trasl_alto, altodestra_x,tempo_traj, "rect");
[s_7,s_7_dot,s_7_dotdot] = trap_profile(8*t_tr, 10*t_tr, f_s, altodestra_x, bassosin_x,tempo_traj, "via_point_inizio");
[s_8,s_8_dot,s_8_dotdot] = trap_profile(10*t_tr, 11*t_tr, f_s, bassosin_x, bassosin_x+trasl_alto,tempo_traj, "via_point_fine");
[s_9,s_9_dot,s_9_dotdot] = trap_profile(11*t_tr ,12*t_tr ,  f_s, bassosin_x+trasl_alto, start_pos, tempo_traj, "rect");

S = [s_1; s_2; s_3; s_4; s_5; s_6; s_7; s_8; s_9];
S_dot = [s_1_dot; s_2_dot; s_3_dot; s_4_dot; s_5_dot; s_6_dot; s_7_dot; s_8_dot; s_9_dot];
S_dotdot = [s_1_dotdot;s_2_dotdot;s_3_dotdot;s_4_dotdot;s_5_dotdot;s_6_dotdot;s_7_dotdot;s_8_dotdot; s_9_dotdot];

P = start_pos;
P_dot = [0 0 0];
P_dotdot= [0 0 0];

for k = 1:size(path_descr.inizio, 1)
    [P, P_dot, P_dotdot] = lin_traj(P, P_dot, P_dotdot, S(k,:), S_dot(k,:), S_dotdot(k,:), path_descr.inizio(k,:), path_descr.fine(k,:));
end

 % [P, P_dot, P_dotdot]=lin_traj(P, P_dot, P_dotdot, s_2_5, s_2_5_dot, s_2_5_dotdot, altosin_x, altosin_x);
 % [P, P_dot, P_dotdot]=lin_traj(P, P_dot, P_dotdot, s_3_5, s_3_5_dot, s_3_5_dotdot, bassodestra_x, bassodestra_x);
 % [P, P_dot, P_dotdot]=lin_traj(P, P_dot, P_dotdot, s_6_5, s_6_5_dot, s_6_5_dotdot, altodestra_x, altodestra_x);
 % [P, P_dot, P_dotdot]=lin_traj(P, P_dot, P_dotdot, s_7_5, s_7_5_dot, s_7_5_dotdot, bassosin_x, bassosin_x);
 % 
end