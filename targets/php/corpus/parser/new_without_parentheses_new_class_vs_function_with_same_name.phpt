<?php

function Something(): string
{
    return 'Another';
}

class Something {}

class Another {}

echo Something() . PHP_EOL;
var_dump(new Something());
var_dump(new (Something()));

?>