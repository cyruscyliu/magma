<?php
$r = new ReflectionClass('DemoTrait');
echo $r . "\n";
$attributes = $r->getAttributes();
var_dump($attributes);
try {
	$attributes[1]->newInstance();
} catch (Error $e) {
	echo get_class($e) . ": " . $e->getMessage() . "\n";
}

?>