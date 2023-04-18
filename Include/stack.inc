procedure stack(ObjType, Color : word); 
var PackItem, GroundItem : Cardinal; 
begin 
   PackItem := 0; 
   GroundItem := 0; 
   Findtype(ObjType,backpack);                    
   IF FindFullQuantity > 0 then PackItem := finditem; 
   Findtype(ObjType,ground);                    
   IF FindFullQuantity > 0 then IgnoreReset; 
   repeat 
      FindtypeEx(ObjType,Color,ground,false); 
      IF FindCount > 0 then 
      if FindQuantity > 55000 then Ignore(finditem) 
      else GroundItem := finditem; 
      FindtypeEx(ObjType,Color,ground,false); 
   until (FindCount = 0) or (GroundItem <> 0); 
   if (PackItem <> 0) and (GroundItem <> 0) then MoveItems(backpack,ObjType,Color,GroundItem,0,0,0,1000) 
   else DropHere(PackItem); 
end;