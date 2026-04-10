<?php

#[\MyAttribute]
const MY_CONST = "Has attributes";

const MY_CONST = "No attributes";

echo MY_CONST . "\n";

$reflection = new ReflectionConstant('MY_CONST');
var_dump($reflection->getAttributes())

?>