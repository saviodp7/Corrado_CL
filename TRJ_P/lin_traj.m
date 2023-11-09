function [P, P_dot, P_dotdot] = lin_traj(P, P_dot, P_dotdot, S, S_dot, S_dotdot, pnt_in, pnt_fin)
    P=P+S'.*(pnt_fin-pnt_in)/norm(pnt_fin-pnt_in);
    P_dot = P_dot + S_dot'.*(pnt_fin-pnt_in)/norm(pnt_fin-pnt_in);
    P_dotdot = P_dotdot + S_dotdot'.*(pnt_fin-pnt_in)/norm(pnt_fin-pnt_in);
end