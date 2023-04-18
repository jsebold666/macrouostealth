procedure CheckDead; 
var q: integer;
begin 
WaitConnection(3000); 
CheckSave; 
if Dead then 
begin 
SetWarMode(true);
WaitGump('1'); 
wait(5000); 
q:=0;
while (Dead) do 
begin
Wait (1000); 
q:=q+1;
if q>180 then 
begin
q:=0;
UOSay('Res me please!');
end;
end;
wait (2000); 
UOSay('Thanks!');
Hungry(1, ground); 
end; 
end;
