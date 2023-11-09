function [s, s_dot, s_dotdot]=trap_profile(t_i ,t_f, f_s, p_i, p_f, t_trj, descr, delta_via_point)
    arguments % default argument
        t_i = 0.0
        t_f = 0.0
        f_s = 1000
        p_i = 0.0
        p_f = 0.0
        t_trj = 0.0
        descr = "rect";
        delta_via_point = 0.1;
    end

s_i = 0;
if descr == "circular"
    s_f = p_f - p_i;
else
    s_f = norm(p_f-p_i);
end
delta_t = t_f-t_i;

s_c_dot = 1.5*abs(s_f-s_i) / delta_t;
tc = (s_i-s_f+s_c_dot*delta_t) / s_c_dot;
s_c_dotdot = s_c_dot/tc;

if descr == "via_point_inizio" || descr == "via_point_fine"
    numero_campioni = f_s*(delta_t+delta_via_point);
else
    numero_campioni = f_s*delta_t;
end

t = linspace(0, delta_t, numero_campioni);
s_primo = zeros(1, numero_campioni);
s_dot_primo = zeros(1, numero_campioni);
s_dotdot_primo = zeros(1, numero_campioni);

for k = 1:numero_campioni
    if t(k) <= tc
        s_primo(k) = s_i+(1/2)*s_c_dotdot*t(k).^2;
        s_dot_primo(k) = s_c_dotdot*t(k);
        s_dotdot_primo(k) = s_c_dotdot;
    elseif ( t(k)>tc && t(k) <= delta_t-tc)
            s_primo(k) = s_i+s_c_dotdot*tc*(t(k)-tc/2);
            s_dot_primo(k) = s_c_dotdot*tc;
            s_dotdot_primo(k) = 0;
    elseif ( t(k) > delta_t-tc && t(k) <= delta_t)
            s_primo(k)=s_f-(1/2)*s_c_dotdot*(delta_t-t(k)).^2;
            s_dot_primo(k)=s_c_dotdot*(delta_t-t(k));
            s_dotdot_primo(k)=-s_c_dotdot;
    end
end

if descr == "via_point_fine"
    inizio_s = t_i*f_s - f_s*delta_via_point;
    fine_s = t_f*f_s;
elseif descr == "via_point_inizio"
    inizio_s = t_i*f_s;
    fine_s = t_f*f_s + f_s*delta_via_point;
else
    inizio_s = t_i*f_s;
    fine_s = t_f*f_s;  
end

fine_traj = f_s*t_trj;

s(1 : inizio_s) = 0;
s(inizio_s + 1 : fine_s) = s_primo;
s(fine_s + 1 : fine_traj) = norm(p_f-p_i);

s_dot(1 : inizio_s) = 0;
s_dot(inizio_s + 1 : fine_s) = s_dot_primo;
s_dot(fine_s + 1 : fine_traj) = 0;

s_dotdot(1 : inizio_s) = 0;
s_dotdot(inizio_s + 1 : fine_s) = s_dotdot_primo;
s_dotdot(fine_s + 1 : fine_traj) = 0;

end