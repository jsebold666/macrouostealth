procedure WaitConnection(WaitTime : Integer);
begin
if Connected then Exit;
while not Connected do Wait(1000);
{WaitTime - Waiting After Connected}
wait(WaitTime);
end;