function A = transf_mat(q_i)
    A = zeros(4,4);
    A = [cos(q_i(4))    -sin(q_i(4))*cos(q_i(2))    sin(q_i(4))*sin(q_i(2))     q_i(1)*cos(q_i(4))
         sin(q_i(4))    cos(q_i(4))*cos(q_i(2))     cos(q_i(4))*sin(q_i(2))     q_i(1)*sin(q_i(4))
         0              sin(q_i(2))                 cos(q_i(2))                 q_i(3)
         0              0                           0                           1                   ];
end