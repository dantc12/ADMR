function a = linprogMatlab()
b = str2num(char(strrep(cell2mat(importdata('input_b')),"L","")));
f = str2num(cell2mat(importdata('input_c')));
[x,numOfEquations]= size(b);
input_A = str2num(cell2mat(importdata('input_A')));
[m,n] = size(input_A);
A=[];
for i = 1 : numOfEquations
    row = input_A(:,(i-1)*n/numOfEquations + 1 : i*n/numOfEquations);
    A = [A;row];
end

bounds = cell2mat(importdata('input_bounds'));
bounds = strrep(bounds, "'", "");
bounds = str2num(char(bounds));
[a,doubledNumOfBounds] = size(bounds);
lb = [];
ub = [];
count = 0;
for i = 1 : doubledNumOfBounds 
    if mod(count,2) == 0
       lb(int16(i/2)) = bounds(i);
    else
       ub(int16(i/2)) = bounds(i);
    end
    count = count + 1;
end

linopt = optimset('TolFun',1e-10, 'Display', 'none');
[x,fval] = linprog(f,A,b,[],[],lb,ub,[],linopt)
a = x;
end

%fileID = fopen('x.txt','w');
%fprintf(fileID,'%12.8f ',x);
%fclose(fileID);

%fileID = fopen('fval.txt','w');
%fprintf(fileID,'%12.8f ',fval);
%fclose(fileID);
