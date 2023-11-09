function [P, P_dot, P_dotdot]=traj_point(start_pos, punto, f_s, tempo_traj)
%% Plan the trajectory along a path characterized by at least 11 points within the workspace, in which there are at least one straight
%  portion and one circular portion and also the passage for at least 4 via points.

t_tr=tempo_traj/10;

 path_descr = struct("inizio", [start_pos; punto+[0,0,0.05]; punto; punto+[0,0,0.05];], ...
                "fine", [punto+[0,0,0.05]; punto; punto+[0,0,0.05]; start_pos; ]);

[s_1,s_1_dot,s_1_dotdot] = trap_profile(0, 2*t_tr,   f_s, start_pos, punto+[0,0,0.05], tempo_traj, "rect");
[s_2,s_2_dot,s_2_dotdot] = trap_profile(2*t_tr, 5*t_tr, f_s, punto+[0,0,0.05], punto, tempo_traj, "rect");
[s_3,s_3_dot,s_3_dotdot] = trap_profile(5*t_tr, 8*t_tr, f_s, punto, punto+[0,0,0.05],tempo_traj, "rect");
[s_4,s_4_dot,s_4_dotdot] = trap_profile(8*t_tr, 10*t_tr, f_s, punto+[0,0,0.05], start_pos,tempo_traj, "rect");

S = [s_1; s_2; s_3; s_4];
S_dot = [s_1_dot; s_2_dot; s_3_dot; s_4_dot];
S_dotdot = [s_1_dotdot;s_2_dotdot;s_3_dotdot;s_4_dotdot];

P = start_pos;
P_dot = [0 0 0];
P_dotdot= [0 0 0];

for k = 1:size(path_descr.inizio, 1)
    [P, P_dot, P_dotdot] = lin_traj(P, P_dot, P_dotdot, S(k,:), S_dot(k,:), S_dotdot(k,:), path_descr.inizio(k,:), path_descr.fine(k,:));
end
end