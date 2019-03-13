grammar Cdl;

/*
A CDL file specifies the cruising plan for one or more vessels. A single file can contain

 - specification for all vessels of interest (the fleet)
 - locations of interest (that may be visited during a cruise)
 - details of people that may serve as crew or guests
 - season plans for selected (or all) vessel(s)
 */

cdl_file            : fleet_spec location_list person_list (vessel_season_spec)+ EOF;

vessel_spec         : VESSEL identifier NAME COLON name FLAG COLON flag REGO COLON rego SPEED COLON speed NEWLINE ;

person_spec         : PERSON identifier NAME COLON name NEWLINE ;

fleet_spec          : (vessel_spec)+ ;

location_list       : (location)+ ;

location            : LOCATION identifier (AT position)? IS placename NEWLINE;

person_list         : (person_spec)* ;

vessel_season_spec  : SEASON season_identifier VESSEL vessel_identifier BEGINS IN location_identifier NEWLINE (cruise)+;

/*
cruise              : CRUISE title NEWLINE (crew_movement)* origin (event_line)* destination (crew_movement)* ;
*/

cruise              : CRUISE title DEPARTS location_identifier ON date AT time  NEWLINE (event_line)+ ;
/*
origin              : visitation_spec NEWLINE ;
destination         : visitation_spec NEWLINE ;

crew_movement       : (joining_spec | leaving_spec) NEWLINE  ;
*/

event_line          : (visitation_spec | via_waypoints | joining_spec | leaving_spec) NEWLINE ;

/*
specify a list of waypoints (zero stay-length visitations) along the route taking vessel to next destination
*/
via_waypoints       : VIA (location_identifier | COMMA)+ ;

lng: (dec_deg | long_deg_min);
lat: (dec_deg | lat_deg_min);

speed               : number ;
dec_deg             : number ;

long_deg_min        : degrees decimal_minutes ew_hemisphere ;
lat_deg_min         : degrees decimal_minutes ns_hemisphere ;

degrees             : UNSIGNED_INT ;
decimal_minutes     : UNSIGNED_INT APOSTROPHIE (UNSIGNED_REAL)? ;
ew_hemisphere       : 'E' | 'W' ;
ns_hemisphere       : 'N' | 'S' ;

number
 : UNSIGNED_INT
 | SIGNED_INT
 | UNSIGNED_REAL
 | SIGNED_REAL
 ;
position            : lng lat;
placename           : PHRASE ;


identifier          : WORD ;
duration_units      : NIGHT | NIGHTS | HOURS ;
visitation_spec     : location_identifier (stay_spec)? ;
stay_duration       : UNSIGNED_INT ;
stay_spec           : FOR stay_duration duration_units ;
location_identifier : WORD ;
vessel_identifier   : WORD ;
season_identifier   : WORD ;
joining_spec        : (CREW | GUEST) identifier JOINS (ON date)? (AS role_spec)? (IN location_identifier)?;
leaving_spec        : (CREW | GUEST) identifier LEAVES (ON date)?  (IN location_identifier)?;
role_spec           : SKIPPER | MATE ;
title               : PHRASE ;
name                : PHRASE ;
flag                : PHRASE ;
rego                : UNSIGNED_INT ;
date                : DATE ;
time                : TIME ;

/*
 * Lexer Rules
 */

fragment L      : ('L'|'l');
fragment O      : ('O'|'o');
fragment C      : ('C'|'c');
fragment A      : ('A'|'a');
fragment T      : ('T'|'t');
fragment I      : ('I'|'i');
fragment N      : ('N'|'n');
fragment R      : ('R'|'r');
fragment S      : ('S'|'s');
fragment U      : ('U'|'u');
fragment E      : ('E'|'e');
fragment F      : ('F'|'f');
fragment G      : ('G'|'g');
fragment H      : ('H'|'h');
fragment V      : ('V'|'v');
fragment M      : ('M'|'m');
fragment P      : ('P'|'p');
fragment W      : ('W'|'w');
fragment J      : ('J'|'j');
fragment K      : ('K'|'k');
fragment B      : ('B'|'b');
fragment D      : ('D'|'d');

fragment LOWERCASE  : [a-z] ;
fragment UPPERCASE  : [A-Z] ;

VESSEL          : V E S S E L;
SEASON          : S E A S O N;
LOCATION        : L O C A T I O N ;
PERSON          : P E R S O N;
CRUISE          : C R U I S E ;
AT              : A T;
AS              : A S;
ON              : O N;
IN              : I N;
FOR             : F O R;
NIGHT           : N I G H T;
NIGHTS          : N I G H T S;
HOURS           : H O U R S;
DEPARTS   	: D E P A R T S;
NAME            : N A M E;
COLON           : ':';
FLAG            : F L A G;
REGO            : R E G O;
CREW            : C R E W;
GUEST           : G U E S T;
JOINS           : J O I N S;
LEAVES          : L E A V E S;
BEGINS          : B E G I N S;
VIA             : V I A;
SPEED           : S P E E D ;

/* Roles */

SKIPPER         : S K I P P E R;
MATE            : M A T E;


IS              : I S ;

WORD            : (LOWERCASE | UPPERCASE) (LOWERCASE | UPPERCASE | [0-9] | '_')* ;


/* Dates and times */
DATE            : [0-9] ([0-9])? SLASH [0-9] ([0-9])? SLASH [0-9] [0-9] ;
TIME            : [0-2] [0-3] [0-5] [0-9] ;

PLUS: '+';
MINUS: '-';
SLASH: '/';
QUOTE: '"';
COMMA: ',';
POINT: '.';
APOSTROPHIE: '\'';


UNSIGNED_INT
 : '0'
 | [0-9] [0-9]*
 ;

SIGNED_INT
 : PLUS [1-9] [0-9]*
 | MINUS [1-9] [0-9]*
 ;

UNSIGNED_REAL
 : [0-9]* '.' [0-9]+
 ;

SIGNED_REAL
 : PLUS [0-9]* '.' [0-9]+
 | MINUS [0-9]* '.' [0-9]+
 ;

PHRASE
   : QUOTE (WORD | ' ' | ';' | ',' | '-')* QUOTE ;

WS      : (' ' | '\t')+  -> skip;

NEWLINE             : ('\r'? '\n' | '\r')+ ;
