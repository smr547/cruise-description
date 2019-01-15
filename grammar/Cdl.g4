grammar Cdl;

/*
A cruise is named and consists of a series of locations
Locations may be common names (as defined by Google) or explicitly defined locations
 */
 
cruise              : (location_definition)+ cruise_definition EOF ;
 
location_definition : location NEWLINE ;

location            : LOCATION WS identifier WS (AT WS position WS)?  IS WS placename ;


lng: number;
lat: number;

number
 : INT
 | REAL
 ;
position            : lng WS lat;
placename           : (WORD | WS)+ ;

identifier          : WORD ;
duration_units	    : NIGHT | NIGHTS ; 
stay_duration       : INT ; 
stay_duration_spec  : FOR WS stay_duration WS duration_units ;
cruise_definition   : CRUISE WS title NEWLINE (destination_line)+ ;
destination_line    : WS identifier (WS stay_duration_spec)? NEWLINE ;
title               : TEXT ;

/*
 * Lexer Rules
 */

fragment L	: ('L'|'l');
fragment O	: ('O'|'o');
fragment C	: ('C'|'c');
fragment A	: ('A'|'a');
fragment T	: ('T'|'t');
fragment I	: ('I'|'i');
fragment N	: ('N'|'n');
fragment R	: ('R'|'r');
fragment S	: ('S'|'s');
fragment U	: ('U'|'u');
fragment E	: ('E'|'e');
fragment F	: ('F'|'f');
fragment G	: ('G'|'g');
fragment H	: ('H'|'h');

fragment LOWERCASE  : [a-z] ;
fragment UPPERCASE  : [A-Z] ;

LOCATION        : L O C A T I O N ;
CRUISE          : C R U I S E ;
AT		: A T;
FOR		: F O R;
NIGHT           : N I G H T;
NIGHTS          : N I G H T S;

IS              : I S ;

WORD            : (LOWERCASE | UPPERCASE | '_')+ ;



PLUS: '+';
MINUS: '-';


INT
 : '0'
 | [1-9] [0-9]*
 | PLUS [1-9] [0-9]*
 | MINUS [1-9] [0-9]*
 ;

REAL
 : [0-9]* '.' [0-9]+
 | PLUS [0-9]* '.' [0-9]+
 | MINUS [0-9]* '.' [0-9]+
 ;


WS      : (' ' | '\t')+ ;

TEXT            : ('['|'(') ~[\]]+ (']'|')');

NEWLINE             : ('\r'? '\n' | '\r')+ ;
