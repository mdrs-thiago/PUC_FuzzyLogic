close all;
clear all;
clc;

a = newfis('fuzzy_controller');
% level
val_a1 = [-2, -1, 0]
a = addvar(a, 'input', 'level', [-1,1]);
a = addmf(a, 'input', 1, 'neg', 'trimf', val_a1)
a = addmf(a, 'input', 1, 'ok', 'trimf', [-1, 0, 1])
a = addmf(a, 'input', 1, 'pos', 'trimf', -1*fliplr(val_a1))

% rate
a = addvar(a, 'input', 'rate', [-1,1]/10);
a = addmf(a, 'input', 2, 'neg', 'trimf', val_a1/10)
a = addmf(a, 'input', 2, 'none', 'trimf', [-1, 0, 1]/10)
a = addmf(a, 'input', 2, 'pos', 'trimf', -1*fliplr(val_a1)/10)

% valve
a = addvar(a, 'output', 'valve', [-1,1]);
close_fast_val = [-1.5, -1, -0.5]
close_small_val = [-1, -0.5, 0]
a = addmf(a, 'output', 1, 'close_fast', 'trimf', close_fast_val)
a = addmf(a, 'output', 1, 'close_small', 'trimf', close_small_val)
a = addmf(a, 'output', 1, 'nothing', 'trimf', [-0.5, 0, 0.5])
a = addmf(a, 'output', 1, 'open_small', 'trimf', -1*fliplr(close_small_val))
a = addmf(a, 'output', 1, 'open_fast', 'trimf', -1*fliplr(close_fast_val))

rules = [
    [2, 0, 3, 1, 1];
    [1, 0, 1, 1, 1];
    [3, 0, 5, 1, 1];
];

a = addrule(a, rules);

figure()
for i=1:2
  subplot(3,1,i)
  plotmf(a, 'input', i)
end

subplot(3,1,3)
plotmf(a, 'output', 1)