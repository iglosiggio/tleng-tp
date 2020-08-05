#### Notas
Este es un borrador para ir poniendo las ideas del informe

A presentar:

* Una descripción de:
  - La solución adoptada
  - El método utilizado
  - Decisiones tomadas
  - Tipo de gramática y/o parser
* Código (hecho) con comentarios (no hecho)
* Ejemplos de corrida con entradas y salidas acorde (hay ejemplos pero no esta documentado)
* Conclusiones:
  - Dificultades encontradas
  - Relevancia de los temas vistos en la materia
  - Eficiencia
  - Posibilidades adicionales
  - Descripción técnica sobre los problemas específicos que encontramos

# Presentación


# Diseño e implementación

El diseño del trabajo práctico se separó en partes distinguidas: primero
conseguir una gramática básica razonable y luego implementar los procesos
propuestos por la materia. Para esto el uso de PLY como parser generator
simplificó gratamente el proceso.

## Lexer

Si bien el lexer y el parser se desarrollaron en conjunto el enfoque fué en
tener a éste terminado primero. Dado que un conjunto de tokens suficientemente
expresivo y estable nos permitió iterar con las reglas del parser mucho más
fácilmente.

Los tokens nuestro lexer genera son los siguientes:

* `BEGIN_DESCRIPTOR`: El inicio de un descriptor, siempre es la cadena "["
* `DESCRIPTOR_VALUE`: Una cadena de texto arbitrario (excepto el caracter para
  comillas dobles) entre comillas dobles
* `END_DESCRIPTOR`: El fin de un descriptor, siempre es la cadena "]"
* `BEGIN_COMMENT`: El inicio de un comentario, siempre es la cadena "{"
* `END_COMMENT`: El fin de un comentario, siempre es la cadena "}"
* `MOVE_NUMBER`: Un número válido para un movimiento, cómo "1..." o "2."
* `MOVE`: Un movimiento válido
* `GAME_RESULT`: El resultado de una partida
* `WORD` : Cualquier otra cadena sin espacios en el medio

Una cosa a notar es que nuestro lexer aprovecha el que el motor de expresiones
regulares permite priorizar opciones ordenándolas (por ejemplo `/a|aa/` nunca
matchea `aa`). Utilizamos esto para tener una buena definición de `WORD`. Otra
cosa notable es que podríamos haber armado a los descriptores como un único
token (algo parecido a `/\[([^" \t]+)[ \t]*"([^"]*)"\]/) pero dado que
decidimos "congelar" el desarrollo del lexer ni bien sentíamos que alcanzaba
para nuestras necesidades nos quedamos con un poco de complejidad extra.

La existencia del token `WORD` es para poder tokenizar el texto arbitrario
dentro de comentarios. Una alternativa es la de "island grammars" propuesta por
ANTLR.

## Parser

# Problemas encontrados

## Manejo de errores


# Conclusiones

