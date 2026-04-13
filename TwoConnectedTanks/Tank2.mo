within NonInteractingTanks;

model Tank2
  parameter Real A = 1, V = 10;
  Real h(start = 1), Q1, T;
  FlowConnect flowConnect annotation(
    Placement(visible = true, transformation(origin = {-42, 42}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-36, 34}, extent = {{-10, -10}, {10, 10}}, rotation = 0))
  );
equation
  Q1 = flowConnect.F;
  der(h) = Q1 / A;
  T = V / max(abs(Q1), 1e-6);
end Tank2;