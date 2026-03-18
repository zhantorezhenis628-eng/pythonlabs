status_button := button;
if re(status_button) then
    if changing_status <3 then inc(changing_status); else changing_status := 0; end_if;
end_if;
 case changing_status of 
    0,2: set(yellow); reset(red); reset(green);
    1: set(red); reset(yellow); reset(green);
    3: set(green); reset(yellow); reset(red);
end_case;

sec1:=%s6
status_button2 := button2;
if re(status_button2) then
    if changing_status2 <3 then inc(changing_status2); else changing_status2 := 0; end_if;
end_if;
IF changing_status2 = 0 or changing_status2 = 2 then
    Yellow2 :=1;
    Green2 := 0;
    Red2 :=0;
    color2 := 'Yellow';
ELSIF changing_status2 = 1 then
    Yellow2 :=0;
    Green2 := 0;
    Red2 :=1;
    color2 := 'Red';
ELSIF changing_status2 = 3 then
    Yellow2 :=0;
    Green2 := 1;
    Red2 :=0;
    color2 := 'Green';
end_if;
if re(sec1) and changing_status2 = 1 then counter := counter + t#1s;
    if counter = t#3s then
        changing_status2 := changing_status2 + 1; counter := t#0s;
    end_if;
end if;
if re(sec1) and (changing_status2 = 0 or changing_status2=2) then counter := counter + t#1s;
        if counter = t#3s then
        changing_status2 := changing_status2 + 1; counter := t#0s;
    end_if;
end if;
if re(sec1) and changing_status2 = 3 then counter := counter + t#1s;
    if counter = t#3s then
        changing_status2 := changing_status2 + 1; counter := t#0s;
    end_if;
end if;


if alarm_but then stop:=1; end_if;
if close then direction:=1; km_on_off:=1; end_if;
if open then direction:=0; km_on_off:=0; end_if;
if not(close) and not(open) then km_on_off:=0; end_if;
copy_button:= button;
if close and RE(copy_button) then close:=0; open:=1; end_if;
if RE(copy_button) and det_open then close:=1; end_if;
if det_closed then close:=0; end_if;
if re(copy_button) and det_closed then open:=1; end_if;
if det_open then open:=0; end_if

sec1:=%S6;
if alarm_but then stop:=1; alarm:=sec1; else alarm:=0; end_if;
if (direction and km_on_off) and NOT(stop) then
    if re(sec1) then position:=position+2; end_if;
end_if;
if (not direction and km_on_off) and not stop then
    if re(sec1) then position:=position +2; end_if;
end_if;
det_open:= (position=0);
det_closed:=(position=10);
if det_open then
    close :=1; end_if;
if det_closed then
    open:=1;
end_if;

sec1:=%s6;
if button and RE(sec1) then 
position := position +2;
if position :=position +2;
if position = 10 then
bottl _counter := bottle_counter +1;
set(sensor);
position:=0;
else reset(sensor);
end_if;
for i:=0 to 11 det_open
bottle[i] :=(position = i);
end_for;
end_if;

sec1:=%s6;
if bottle[9] then
    sensor := true;
else
    sensor := false;
end_if;
if re(button) and re(sec1) then
    if bottle[9] then
        bottle_counter:=bottle_counter+1;
    end_if;
    for i:=10 to 1 by -1 do
        bottle[i]:=bottle[i-1];
    end_for;
    if bottle[3] or not (bottle[1] or bottle[2] or bottle[3] or bottle[4] or bottle[5] or bottle[6] or bottle[7] or bottle[8] or bottle[9] or bottle[10]) then
        bottle[0]:=true;
    else
        bottle[0]:=false;
    end_if;
end_if;
if not button then
    sensor := false;
end_if;


sec1:=%s6;
if re(array_1[0]) and RE(sec1) then code:= CONCAT_STR(code, '1');
elsif re(array_1[1]) and RE(sec1) then code:= CONCAT_STR(code, '2');
elsif re(array_1[2]) and RE(sec1) then code:= CONCAT_STR(code, '3');
elsif re(array_1[3]) and RE(sec1) then code:= CONCAT_STR(code, '4');
elsif re(array_1[4]) and RE(sec1) then code:= CONCAT_STR(code, '5');
end_if;
len_str := len_int(code);
if reset then code:=''; end_if;
if code = '555555' and len_str = 6 and start_button and not(stop_button) then motor:=true;
else motor:= false;
end_if;

if entry = 1 then
    if flag = 0 then
        p01:=1;
        p02:=0;
    end_if;
    if flag = 1 then
        p01:=0;
        p02:=0;
    end_if;
end_if;
if entry =2 then 
    p01:=1;
    if m_f_var then
        p02:=1;
    end_if;
end_if;

if entry = 3 then
    p01:=0;
    p02:=0;
    e_mode :=1;
end_if;
if entry = 0; then
    p01:=0;
    p02:=0;
end_if;

if user = '0' then
    change :=0;
end_if;
if user = '1' then
    change :=1;
end_if;
if user = '2' then
    change :=2;
end_if;

case change of
    0: RESET(punp1); RESET(punp2); RESET(alarm);
    1: SET(pump1); RESET(pump2); RESET(alarm);
    2: SET(pump1); SET(alarm); TON_0 (IN := alarm, PT:= T#3s);
        if TON_0.0 then
            punp2:=1;
        end_if;
end_case


