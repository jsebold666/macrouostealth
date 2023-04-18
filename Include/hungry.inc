procedure Hungry(NeededLevel : Integer; Container : Cardinal);
var HArray : array [0..10] of String;
    CurrentLevel : Integer;
    HasError : Boolean;
    TimeSayHungry : TDateTime;
    FoodID : Cardinal;
    i,c,difference : Integer; 
    
//    b : Byte;
begin
//b := 0;   
if Not Connected then Exit;
if (NeededLevel < 0) or (NeededLevel > 10) then Exit;
   HArray[0] := 'You are absolutely stuffed!';
   HArray[1] := 'You are stuffed';
   HArray[2] := 'hungry at all';
   HArray[3] := 'You are a little hungry';
   HArray[4] := 'You are somewhat hungry';
   HArray[5] := 'You are REALLY hungry';
   HArray[6] := 'Your stomash hurts';
   HArray[7] := 'Your stomash hurts and you feel dizzy';
   HArray[8] := 'You are starving';
   HArray[9] := 'You are almost dying of hunger';
   HArray[10] := 'You are DYING of hunger...';
HasError := true;
TimeSayHungry := Now;
UOSay('.hungry');
wait(100);
i:=0;
while i < 100 do
   begin
   for c := 0 to 10 do
   if InJournalBetweenTimes(HArray[c],TimeSayHungry,Now) >= 0 then
	begin
	CurrentLevel := c;
	HasError := false;
	i := 100;
	end;
   wait(100);
   i := i + 1;
   end;
if HasError then
   begin
   AddToSystemJournal('Error with Hungry: Lag? Conection error? Something else?');
   Exit;
   end;
difference := CurrentLevel - NeededLevel;
FindType($097B,Container);
if (difference > 0) and (FindCount > 0) then for i := 1 to difference do
   begin
   FoodID := FindType($097B,Container);
   if FoodID <> $00 then UseObject(FoodID);
   wait(200);
   end;
if FindType($097B,Container) = 0 then AddToSystemJournal('No Food');
end;