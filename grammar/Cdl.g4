grammar Cdl;

/*
location SCARLES is "Sant Carles de la Rapita, Spain"
 */
 
cruise              : line+ EOF ;
 
line                : location NEWLINE ;

location            : LOCATION WHITESPACE id WHITESPACE IS WHITESPACE placename ;

placename           : (WORD | WHITESPACE)+ ;

id                  : WORD ;

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
fragment S	: ('S'|'s');

fragment LOWERCASE  : [a-z] ;
fragment UPPERCASE  : [A-Z] ;

LOCATION        : L O C A T I O N ;

IS              : I S ;

WORD            : (LOWERCASE | UPPERCASE | '_')+ ;

ID              : WORD ;

WHITESPACE      : (' ' | '\t')+ ;

TEXT            : ('['|'(') ~[\]]+ (']'|')');

NEWLINE             : ('\r'? '\n' | '\r')+ ;
