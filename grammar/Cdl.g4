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

cruise_definition   : CRUISE WS title NEWLINE (destination_line)+ ;
destination_line    : WS identifier NEWLINE ;
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

fragment LOWERCASE  : [a-z] ;
fragment UPPERCASE  : [A-Z] ;

LOCATION        : L O C A T I O N ;
CRUISE          : C R U I S E ;
AT		: A T;

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
