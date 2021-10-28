include "globals.mzn";

int: Evaluation;
int: nTables;
set of int: tables = 1..nTables;
int: nSeats;
set of int: seats = 1..nSeats;
int: nGuests;
set of int: guests = 1..nGuests;
int: nGroups;
array[int] of set of int: Groups;
int: PrefWeight;
array[int] of set of int: Pref;
set of int: Trouble;
int: egalWelfare = 0;
int: utilWelfare = 0; 
int: welfare = 0;

array[tables] of var set of guests: SolvedSeating;
array[guests] of var tables: ReverseSeating; 

constraint int_set_channel(ReverseSeating, SolvedSeating);
  
%union together all the tables into a set 
var set of int: unioned = array_union(SolvedSeating);

%size of table <= nSeats
constraint forall(table in SolvedSeating)(
  card(table) <= nSeats);
  
%size of table >= floor(nSeats/2)
constraint forall(table in SolvedSeating)( 
  card(table) >= floor(nSeats/2)
  );
  
%all guests, 1..9, must be somewhere in the union of all the tables
constraint forall(g in guests)(
  g in unioned
  );
  
%no two guests are seated twice 
constraint all_different(SolvedSeating);

%no two troublemakers at same table
constraint forall(t in SolvedSeating)(
  forall(i,j in Trouble where i != j)(
    if ((i in t) /\ (j in t)) then false endif
    )
  );

%groups musts be seated together
constraint forall(t in SolvedSeating)(
  forall(g in Groups)(
    disjoint(g,t) xor ('subset'(g,t))
    )
  );

%impose ordering to break symmetries 
constraint increasing(SolvedSeating);

%constraint utilWelfare = sum(p in guests, t in SolvedSeating) (if p in t then abs(
%card('intersect'(Pref[p],t))*PrefWeight) else 0 endif);
  
%constraint utilWelfare = sum(g in guests, t in ReverseSeating) (card('intersect'(Pref[g], SolvedSeating[t])) * PrefWeight);

constraint egalWelfare = min(g in guests, t in ReverseSeating) (abs( card( 'intersect'(Pref[g], SolvedSeating[t]))) * PrefWeight);

constraint welfare = 
if (Evaluation == 0) then utilWelfare else egalWelfare endif;

solve maximize welfare;

% Composing if statements...
output  ["Table: Guests:\n", "   1 : ", show(SolvedSeating[1]),"\n", 
        "   2 : ", show(SolvedSeating[2]), "\n",  %show(Pref[2]), show(SolvedSeating[2])
        "   3 : ", show(SolvedSeating[3]), "\n",
        "   4 : ", show(SolvedSeating[4]), "\n",
        "   5 : ", show(SolvedSeating[5]), "\n",
        "   6 : ", show(SolvedSeating[6]), "\n",
        "Utilitarian Happiness: ", show(utilWelfare), "\n",
        "Egalitarian Happiness: ", show(egalWelfare), "\n",
        "----------"];