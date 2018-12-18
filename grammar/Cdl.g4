grammar Cdl;

/*
A cruise is named and consists of a series of locations
Locations may be common names (as defined by Google) or explicitly defined locations
 */
 
cruise              : (location_definition)+ cruise_definition EOF ;
 
location_definition : location NEWLINE ;

location            : LOCATION WHITESPACE id WHITESPACE IS WHITESPACE placename ;

placename           : (WORD | WHITESPACE)+ ;

id                  : WORD ;

cruise_definition   : CRUISE WHITESPACE title NEWLINE (destination_line)+ ;
destination_line    : WHITESPACE id NEWLINE ;
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

IS              : I S ;

WORD            : (LOWERCASE | UPPERCASE | '_')+ ;

ID              : WORD ;

WHITESPACE      : (' ' | '\t')+ ;

TEXT            : ('['|'(') ~[\]]+ (']'|')');

NEWLINE             : ('\r'? '\n' | '\r')+ ;
