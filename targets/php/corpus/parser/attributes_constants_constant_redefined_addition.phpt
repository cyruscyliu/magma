<?php

const MY_CONST = "No attributes";

#[\MyAttribute]
const MY_CONST = "Has attributes";

echo MY_CONST . "\n";

$reflection = new ReflectionConstant('MY_CONST');
var_dump($reflection->getAttributes())

?>