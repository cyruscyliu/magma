<?php

#[\MyAttribute]
const MY_CONST = "Has attributes (1)";

#[\MyOtherAttribute]
const MY_CONST = "Has attributes (2)";

echo MY_CONST . "\n";

$reflection = new ReflectionConstant('MY_CONST');
var_dump($reflection->getAttributes())

?>