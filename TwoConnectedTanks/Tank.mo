within NonInteractingTanks;

model Tank
parameter Real Qin = 2, A =1;
Real h(start=1), Qo;
  FlowConnect flowConnect annotation(
    Placement(visible = true, transformation(origin = {18, -8}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {16, -6}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
flowConnect.F = Qo;
der(h) = (Qin - Qo)/A;
if time<=5 then
Qo = 0;
else
Qo = sqrt(max(h, 1e-6));
end if;
end Tank;